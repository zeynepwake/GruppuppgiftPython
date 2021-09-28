#Imports
import os.path
import streamlit as st
import DB_Handling
from API_interface import API_Requests

#Definitions
def intro():
    print("Hello this is StudieGrupp1's ML Model Testing Program :)")

def main_program():
    """
    Summary: this model interagerar med en maskininlärningsmodell via ett API
    i fil-namn API_interface i repot. Datan sedan sparas i en databas med
    hjälp av sqlite3 DB_Handling. Datan som användaren anger kan vid ett senare
    tillfälle väljas och återanvändas för test.

    Vi har valt att använda 3 av 4 modeller, Text Generator, Sentiment Analysis och
    Question & Answering.

    Navigera mellan  registrera, login och model testing sidor att använda vår app.

    Vi ställer några krav på användaren:
    - Användaren behöver registrera sig och logga in inför val av testmodel.
    - Inför varje test eller vid ändring av test model bör vald model omstartas.
    - I fall användaren lämnas ett fält tomt visas felmeddelande,
        användaren måste mata in text för att kunna använda modellerna.

    """
    st.set_page_config(layout = "wide")
    st.header('ML ModelTesting Program by Jakob, Szandra and Zeynep!')

    #Session IDs
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'user' not in st.session_state:
        st.session_state['user'] = ''

    if 'model_started' not in st.session_state:
        st.session_state['model_started'] = False

    if 'current_model' not in st.session_state:
        st.session_state['current_model'] = None

    #Sidebar definition
    page = st.sidebar.selectbox('Page', ['Register', 'Login', 'Models'])
    if st.sidebar.button('Log out and Close'):
        st.session_state['logged_in'] = False
        st.write("That's all folks :) Thanks for now.")
        st.write("Please close the window and terminate the StreamLit Server in you Terminal.")
        st.stop()
        #Please respekt: "Streamlit effectively spins up a server, and
        # we do not envision a use case to shut down the server
        # due to a UI interaction in the script."

    #DB Connection
    if os.path.isfile('DB_ML_History.db'):
        ml_db = DB_Handling.MLModel_DB('DB_ML_History.db')
    else:
        #If DB not exist: Create a DB struktur
        #and initialize the DB.models with existing models from API
        ml_db = DB_Handling.MLModel_DB('DB_ML_History.db')
        ml_db.create_db()
        models = API_Requests.models
        for modelname in models:
            ml_db.create_model(modelname)

    #Page definitions
    if page == 'Login':
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            df = ml_db.login(username, password)
            if df.empty:
                st.warning('Account name or password is incorrect, please try again!')
            else:
                st.session_state['logged_in'] = True
                st.session_state['user'] = username
                #Here we have the First and the last name also...
                st.success(f"""You are logged in. Please test your model
                            on "Models" page, check the sidebar.""")

    if page == 'Register':
        # user register page, controll if the user-id is taken, if not register.
        col1, col2 = st.columns(2)
        with col1:
            first_name =st.text_input('Enter your first name')
            last_name =st.text_input('Enter your last name')
        with col2:
            user_name = st.text_input('Please enter your user name')
            password = st.text_input('Choose a password', type='password')
            if st.button('Register'):
                if not ml_db.chk_account_if_exists(user_name):
                    ml_db.create_user(user_name, password, first_name, last_name)
                    st.success('User registered. Please log in on the "Login" page')
                else:
                    st.warning('Accountname already exists. Please try another one.')

    if page == 'Models':
        # model-page. After the user logs in can she choose and start a model.
        if not st.session_state['logged_in'] is True:
            st.warning('Please log in on the "Login" page')
        else:
            st.write(f"Logged in as {st.session_state['user']}")
            st.write(f"Current model: {st.session_state['current_model']}")
            col1, col2 = st.columns([2,4])
            with col1:
                model = st.selectbox('Select a model', API_Requests.models)
                #st.write(st.session_state['model_started'])
                if st.button('Start model'):
                    with st.spinner(text = 'Model is starting...'):
                        API_Requests.start_model(model)
                        st.session_state['model_started'] = True
                        st.session_state['current_model'] = model
                    st.success('Model started')

                if not st.session_state['model_started'] is True:
                    st.warning('Please choose a model')
                else:
                    if model == 'text_generator' and st.session_state['current_model'] == model:
                        user_text_input = st.text_input('Please type below')
                        if st.button('Submit input'):
                            if user_text_input == '':
                                st.error('Provide input')
                            else:
                                with st.spinner(text = 'Waiting for response...'):
                                    response = API_Requests.post_generator(user_text_input)
                                st.write(response.json())
                                response_data = response.json()
                                answer = response_data['generated_text']
                                ml_db.create_log(st.session_state['user'], model,
                                                user_text_input, None,
                                                answer, None)

                    elif model =='sentiment_analysis' and st.session_state['current_model'] == model:
                        user_text_input = st.text_input("Please give your context for testing:")
                        if st.button('Submit input'):
                            if user_text_input == '':
                                st.error('Provide input')
                            else:
                                with st.spinner(text = 'Waiting for response...'):
                                    response =  API_Requests.post_sentiment(user_text_input)
                                st.write(response.json())
                                response_data = response.json()
                                score = response_data['score']
                                answer = response_data['sentiment_label']
                                ml_db.create_log(st.session_state['user'], model,
                                                user_text_input, None,
                                                answer, score)

                    elif model =='question_answering' and st.session_state['current_model'] == model:
                        user_text_input = st.text_input("Please type below")
                        question = st.text_input("What would you like to ask?")
                        if st.button('Submit input'):
                            if user_text_input == '' or question == '':
                                st.error('Provide input')
                            else:
                                with st.spinner(text = 'Waiting for response...'):
                                    response = API_Requests.post_qa(user_text_input, question)
                                st.write(response.json())
                                response_data = response.json()
                                score = response_data['score']
                                answer = response_data['answer']
                                ml_db.create_log(st.session_state['user'], model,
                                                user_text_input, question,
                                                answer, score)
            with col2:
                #history/search function.After user logs in they can reach their own search history.
                df_log = ml_db.log_query(st.session_state['user'])
                df_view = df_log[df_log['name'] == model]
                if st.session_state['current_model'] != model:
                    st.warning('Do not forget to start the model!')
                elif df_view.empty:
                    st.write('It seems like you have no history yet :) ')
                else:
                    st.dataframe(df_view[['context', 'question', 'score', 'response']])
                    selected_index = st.selectbox('Select index',list(df_view.index))
                    selected_element = df_view.loc[int(selected_index),:]

                    if st.button('Submit old input'):
                        #Sentiment anaysis block
                        if model == 'sentiment_analysis':
                            with st.spinner(text = 'Waiting for response...'):
                                response = API_Requests.post_sentiment(selected_element.loc['context'])
                            st.write(response.json())
                            response_data = response.json()
                            score = response_data['score']
                            answer = response_data['sentiment_analysis']
                            ml_db.create_log(st.session_state['user'], model,
                                            selected_element.loc['context'], None,
                                            answer, score)

                        #Q&A block
                        if model == 'question_answering':
                            with st.spinner(text = 'Waiting for response...'):
                                response = API_Requests.post_qa(selected_element.loc['context'],
                                                                selected_element.loc['question'])
                            st.write(response.json())
                            response_data = response.json()
                            score = response_data['score']
                            answer = response_data['answer']
                            ml_db.create_log(st.session_state['user'], model,
                                            selected_element.loc['context'],
                                            selected_element.loc['question'],
                                            answer, score)

                        #Text generation block
                        if model == 'text_generator':
                            with st.spinner(text = 'Waiting for response...'):
                                response = API_Requests.post_generator(selected_element.loc['context'])
                            st.write(response.json())
                            response_data = response.json()
                            answer = response_data['generated_text']
                            ml_db.create_log(st.session_state['user'], model,
                                            selected_element.loc['context'], None,
                                            answer, None)


#Main area :)
if __name__ == "__main__":
    #Info to User
    intro()
    #Processing the Program :)
    main_program()
