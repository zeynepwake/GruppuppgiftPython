import sqlite3
import pandas as pd
from datetime import datetime

class MLModel_DB():

    def __init__(self, source: str):
        """This is the initializer of the Class
            Opens the database file or creates if does not exist.

        Args:
            source (str): The source file's url (filename)
        """
        self.source = source
        self.db = sqlite3.connect(source)
        self.cur = self.db.cursor()

    def create_db(self):
        """This method creates the DataBase's structure:
            Table "models" (PK id, name)
            Table "users" (PK id, account_name, pwd, first_name, last_name)
            Table "histories" (PK id, FK user_id, FK model_id, time, context, question, score, response)
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS models(
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name text UNIQUE NOT NULL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    account_name text UNIQUE NOT NULL,
                    pwd text NOT NULL,
                    first_name text NOT NULL,
                    last_name text NOT NULL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS histories(
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    user_id integer NOT NULL,
                    model_id integer NOT NULL,
                    time text NOT NULL,
                    context text NOT NULL,
                    question text,
                    score float,
                    response text NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (model_id) REFERENCES models (id))''')
        self.db.commit()

    def chk_account_if_exists(self, account_name: str) -> bool:
        """This method checks if "account_name" exists in the DataBase

        Args:
            account_name (str): User's Account Name

        Returns:
            bool: Value is True if the "account_name" exists or False otherwise
        """
        chkOK = False 
        df = pd.read_sql("SELECT account_name FROM users", self.db)
        users = df['account_name'].tolist()
        if account_name in users:
            chkOK = True
        return chkOK

    def create_user(self, account_name: str, pwd: str, first_name: str, last_name: str):
        """This method creates a User in the DataBase's "users" Table with the given arguments

        Args:
            account_name (str): User's Account Name
            pwd (str): User's Password
            first_name (str): User's First Name
            last_name (str): User's Last Name
        """
        self.cur = self.db.cursor()
        data = [(account_name, pwd, first_name, last_name)]
        self.cur.executemany("""INSERT INTO users(
                        account_name, pwd, first_name, last_name)
                        VALUES(?, ?, ?, ?)""",
                        data)
        self.db.commit()

    def create_model(self, model_name: str):
        """This method creates a Model in the DataBase's "models" Table with the given argument

        Args:
            model_name (str): Models's Name
        """
        self.cur = self.db.cursor()
        data = [(model_name)]
        self.cur.execute("""INSERT INTO models(
                        name)
                        VALUES(?)""",
                        data)
        self.db.commit()

    def login(self, user_name: str, user_pwd: str) -> pd.DataFrame:
        """This method checks if the User and the Password pair exists in the DataBase and
            returns with the appropriate row

        Args:
            user_name (str): User's Account Name
            user_pwd (str): User's Password
        
        Returns:
            pd.DataFrame: A DataRow with the User's data: Account Name, Password, First name, Last name
        """
        self.cur = self.db.cursor()
        df = pd.read_sql(f"""SELECT account_name, pwd, first_name, last_name FROM users
                        WHERE (account_name = '{user_name}') and (pwd = '{user_pwd}')""", self.db)
        return df

    def create_log(self, user_name: str, model_name: str, context: str,
                    question: str, answer: str, score: float) -> bool:
        """This method creates a Log Entry if the User and the Password pair exists in the DataBase
            and returns True if the Log is created successfully
            if the User or the Password does not exist the method returns False

        Args:
            user_name (str): User's Account Name
            user_pwd (str): User's Password
        
        Returns:
            bool: True if the Log is created, or False otherwise
        """
        self.cur = self.db.cursor()
        self.cur.execute(f"""SELECT id FROM users WHERE account_name = '{user_name}'""")
        row = self.cur.fetchone()
        if row is None:
            return False
        user_id = row[0]
        self.cur = self.db.cursor()
        self.cur.execute(f"""SELECT id FROM models WHERE name = '{model_name}'""")
        row = self.cur.fetchone()
        if row is None:
            return False
        model_id = row[0]
        time = str(datetime.now())
        data = [(user_id, model_id, time, context, question, score, answer)]
        self.cur.executemany("""INSERT INTO histories
                            (user_id, model_id, time, context, question, score, response)
                            VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
        self.db.commit()
        return True

    def log_query(self, user_name: str) -> pd.DataFrame:
        """This method returns all Log entries matching the given username.

        Args:
            user_name (str): User's Account Name
        
        Returns:
            pd.DataFrame: A joined DataSet sorted by user_name from the DataBase:
                        users.account_name, models.name, histories.context, histories.question
        """
        self.cur = self.db.cursor()
        self.cur.execute(f"""SELECT id FROM users WHERE account_name = '{user_name}'""")
        row = self.cur.fetchone()
        if row is None:
            return None
        user_id_key = row[0]
        self.cur = self.db.cursor()
        df_hist = pd.read_sql(f"""SELECT account_name, name, context, question
                    FROM users, models, histories
                    WHERE (histories.user_id = {user_id_key}) and
                    (histories.user_id = users.id) and (histories.model_id = models.id)""", self.db)
        return df_hist