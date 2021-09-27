######################################        Under construction
#Imports
import os.path
import streamlit as st
#import pandas as pd

import DB_Handling
from API_interface import API_Requests

#Definitions
def intro():
    print("Hello this is StudieGrupp1's ML Model Testing Program :)")
    return

def main_program():
    st.set_page_config(layout = "wide")
    st.header('ML ModelTesting Program by Jakob, Szandra and Zeynep!')

    #Session IDs
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'user' not in st.session_state:
        st.session_state['user'] = ''

    if 'model_started' not in st.session_state:
        st.session_state['model_started'] = False

    st.write(st.session_state['logged_in'])

    #Sidebar definition
    page = st.sidebar.selectbox('Page', ['Register', 'Login', 'Model test with new input', 'Model test with reused data'])
    st.sidebar.write('Please choose a page to do a Registration or a Login first :)')
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
                st.write('Account name or password is incorrect, please try again!')
            else:
                st.session_state['logged_in'] = True
                st.session_state['user'] = username
                #Here we have the First and the last name also...
                st.write('You are logged in. Please choose one of our Model testing page on the sidebar.')

    if page == 'Register':
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
                    st.write('User registered. Please log in on the "Login" page')
                else:
                    st.write('Accountname already exists. Please try another one.')

    if page == 'Model test with new input':
        if not st.session_state['logged_in'] is True:
            st.warning('Please log in on the "Login" page')
        else:
            st.write(f"Logged in as {st.session_state['user']}")
            col1, col2 = st.columns([2,4])
            with col1:
                model = st.selectbox('Select a model', API_Requests.models)
                st.write(st.session_state['model_started'])
                if st.button('Start model'):
                    with st.spinner(text = 'Model starting...'):
                        API_Requests.start_model(model)
                        st.session_state['model_started'] = True
                        st.write('Model started')
                if not st.session_state['model_started'] is True:
                    st.warning('Please choose a model')
                else:
                    if model == 'text_generator':
                        user_text_input = st.text_input('Please give your context for testing:')
                        if st.button('Submit input'):
                            response = API_Requests.post_generator(user_text_input)
                            st.write(response.json())
                            response_data = response.json()
                            answer = response_data['generated_text']
                            ml_db.create_log(st.session_state['user'], model,
                                            user_text_input, None,
                                            answer, None)
                    elif model =='sentiment_analysis':
                        user_text_input = st.text_input("Please give your context for testing:")
                        if st.button('Submit input'):
                            response =  API_Requests.post_sentiment(user_text_input)
                            st.write(response.json())
                            response_data = response.json()
                            score = response_data['score']
                            answer = response_data['sentiment_label']
                            ml_db.create_log(st.session_state['user'], model,
                                            user_text_input, None,
                                            answer, score)
                    elif model =='question_answering':
                        user_text_input = st.text_input("Please give your context for testing:")
                        question = st.text_input("What would you like to ask?")
                        if st.button('Submit input'):
                            response = API_Requests.post_qa(user_text_input, question)
                            st.write(response.json())
                            response_data = response.json()
                            score = response_data['score']
                            answer = response_data['answer']
                            ml_db.create_log(st.session_state['user'], model,
                                            user_text_input, question,
                                            answer, score)
            with col2:
                try:
                    df_log = ml_db.log_query(st.session_state['user'])
                    if len(df_log) == 0:
                        st.write('It seams this is your first test. Cool :)')
                    else:
                        st.write(f'Your earlier MLModel Test with the chosen {model} model:')
                        df_view = df_log[df_log['name'] == model]
                        if len(df_view) == 0:
                            st.write(f'It seams this is your first test with the chosen {model} model. Cool :)')
                        else:
                            st.dataframe(df_view)
                except Exception:
                    st.warning('!!! Warning: Please choose a model first and start the API server.')

    if page == 'Model test with reused data':
        if not st.session_state['logged_in'] is True:
            st.warning('Please log in on the "Login" page')
        else:
            st.write(f"Logged in as {st.session_state['user']}")
            model = st.selectbox('Select a model', API_Requests.models)
            st.write(st.session_state['model_started'])
            if st.button('Start model'):
                API_Requests.start_model(model)
                st.session_state['model_started'] = True
                df_log = ml_db.log_query(st.session_state['user'])
                st.write('Model started')
            if not st.session_state['model_started'] is True:
                st.warning('Please choose a model')
            else:
                try:
                    df_log = ml_db.log_query(st.session_state['user'])
                    if df_log.empty:
                        st.write('It seams this is your first test with the choosen model. Cool :)')
                    else:
                        st.write(f'Your earlier MLModel Test with the chosen {model} model:')
                        df_view = df_log[df_log['name'] == model]
                        if df_view.empty:
                            st.write(f'It seams this is your first test with the chosen {model} model. Cool :)')
                        else:
                            st.dataframe(df_view[['context', 'question']])
                            selected_index = st.number_input('Select index', min_value = 0, max_value = len(df_view) - 1, step = 1)
                            df_set = df_view[['context', 'question']].iloc[int(selected_index),:]
                            st.dataframe(df_set)
                            if model == 'text_generator':
                                user_text_input = df_set['context']
                                if st.button('Submit input'):
                                    response = API_Requests.post_generator(user_text_input)
                                    st.write(response.json())
                                    response_data = response.json()
                                    answer = response_data['generated_text']
                                    ml_db.create_log(st.session_state['user'], model,
                                                    user_text_input, None,
                                                    answer, None)
                            elif model =='sentiment_analysis':
                                user_text_input = df_set['context']
                                if st.button('Submit input'):
                                    response =  API_Requests.post_sentiment(user_text_input)
                                    st.write(response.json())
                                    response_data = response.json()
                                    score = response_data['score']
                                    answer = response_data['sentiment_label']
                                    ml_db.create_log(st.session_state['user'], model,
                                                    user_text_input, None,
                                                    answer, score)
                            elif model =='question_answering':
                                user_text_input = df_set['context']
                                question = df_set['question']
                                if st.button('Submit input'):
                                    response = API_Requests.post_qa(user_text_input, question)
                                    st.write(response.json())
                                    response_data = response.json()
                                    score = response_data['score']
                                    answer = response_data['answer']
                                    ml_db.create_log(st.session_state['user'], model,
                                                    user_text_input, question,
                                                    answer, score)
                except IndexError:
                    st.write('!!! Warning: Please choose a model first and start the API server.')

#Main area :)
if __name__ == "__main__":
    #Info to User
    intro()
    #Processing the Program :)
    main_program()
