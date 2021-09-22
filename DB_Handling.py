import sqlite3
import pandas as pd
from datetime import datetime

class MLModel_DB():

    def __init__(self, source: str):
        self.source = source
        self.db = sqlite3.connect(source)
        self.cur = self.db.cursor()

    def create_db(self):
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
        chkOK = False 
        df = pd.read_sql("SELECT account_name FROM users", self.db)
        users = df['account_name'].tolist()
        if account_name in users:
            chkOK = True
        return chkOK

    def create_user(self, account_name: str, pwd: str, first_name: str, last_name: str):
        self.cur = self.db.cursor()
        data = [(account_name, pwd, first_name, last_name)]
        self.cur.executemany("""INSERT INTO users(
                        account_name, pwd, first_name, last_name)
                        VALUES(?, ?, ?, ?)""",
                        data)
        self.db.commit()

    def create_model(self, model_name: str):
        self.cur = self.db.cursor()
        data = [(model_name)]
        self.cur.execute("""INSERT INTO models(
                        name)
                        VALUES(?)""",
                        data)
        self.db.commit()

    def login(self, user_name: str, user_pwd: str) -> pd.DataFrame:
        self.cur = self.db.cursor()
        df = pd.read_sql(f"""SELECT account_name, pwd, first_name, last_name FROM users
                        WHERE (account_name = '{user_name}') and (pwd = '{user_pwd}')""", self.db)
        return df

    def create_log(self, user_name: str, model_name: str, context: str,
                    question: str, answer: str, score: float) -> bool:
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
        self.cur = self.db.cursor()
        self.cur.execute(f"""SELECT id FROM users WHERE account_name = '{user_name}'""")
        row = self.cur.fetchone()
        if row is None:
            return None
        user_id_key = row[0]
        self.cur = self.db.cursor()
        df_hist = pd.read_sql(f"""SELECT user_id, model_id, time, context, response
                                FROM histories
                                WHERE user_id = {user_id_key}""", self.db)
        return df_hist