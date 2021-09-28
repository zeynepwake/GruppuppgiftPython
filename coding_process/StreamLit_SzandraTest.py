import os.path
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder

import DB_Handling
from API_interface import API_Requests

st.set_page_config(layout="wide")
st.header('ML ModelTesting Program by Jakob, Szandra and Zeynep!')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = ''

if 'model_started' not in st.session_state:
    st.session_state['model_started'] = False

st.write(st.session_state['logged_in'])

page = st.sidebar.selectbox('Select a Page:', ['Register', 'Login', 'Models'])
st.sidebar.write('Please choose a page to do a Registration or a Login first :)')

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
            st.write('You are logged in. Please choose a Model on the "Models" page.')

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

if page == 'Models':
    if not st.session_state['logged_in'] is True:
        st.write('Please log in on the "Login" page')
    else:
        st.write(f"Logged in as {st.session_state['user']}")
        col1, col2 = st.columns([2,4])
        with col1:
            model = st.selectbox('Select a model', API_Requests.models)
            st.write(st.session_state['model_started'])
            if st.button('Start model'):
                API_Requests.start_model(model)
                st.session_state['model_started'] = True
                st.write('Model started')
            if not st.session_state['model_started'] is True:
                st.write('Please choose a model')
            else:
                if model == 'text_generator':
                    user_text_input = st.text_input('Please type below')
                    response = API_Requests.post_generator(user_text_input)
                    st.write(response.json())
                    response_data = response.json()
                    answer = response_data['generated_text']
                    ml_db.create_log(st.session_state['user'], model,
                                    user_text_input, None,
                                    answer, None)

                elif model =='sentiment_analysis':
                    user_text_input = st.text_input("Please give your context for testing:")
                    response =  API_Requests.post_sentiment(user_text_input)
                    st.write(response.json())
                    response_data = response.json()
                    score = response_data['score']
                    answer = response_data['sentiment_label']
                    ml_db.create_log(st.session_state['user'], model,
                                    user_text_input, None,
                                    answer, score)

                elif model =='question_answering':
                    user_text_input = st.text_input("Please type below")
                    question = st.text_input("What would you like to ask?")
                    response = API_Requests.post_qa(user_text_input, question)
                    st.write(response.json())
                    response_data = response.json()
                    score = response_data['score']
                    answer = response_data['answer']
                    ml_db.create_log(st.session_state['user'], model,
                                    user_text_input, question,
                                    answer, score)
        with col2:
            df_log = ml_db.log_query(st.session_state['user'])
            if df_log.empty:
                st.write(':) It seams this is your first test. Cool :)')
            else:
                st.write('Your earlier MLModel tests')
                st.dataframe(df_log)
                tested_models = df_log['name'].unique()
                model_for_testing = st.selectbox('Select a model', tested_models)
                df_log = df_log[(df_log['name'] == model_for_testing)]
                st.dataframe(df_log)
                tested_context = df_log['context'].unique()
                context_for_testing = st.selectbox('Select a context', tested_context)
                df_log = df_log[(df_log['context'] == context_for_testing)]
                st.dataframe(df_log)

        with col2:
            df_log = ml_db.log_query(st.session_state['user'])
            if df_log.empty:
                st.write('It seams this is your first test with the choosen model. Cool :)')
            else:
                st.write(f'Your earlier MLModel Test with the chosen {model} model tests')
                df_view = df_log[df_log['name'] == model]
                st.dataframe(df_view[['context', 'question']])
                selected_index = st.number_input('Select index', min_value=0, max_value=len(df_log)-1, step=1)
                df_set = df_view[['context', 'question']].iloc[int(selected_index),:]
                st.dataframe(df_set)
                if st.button('Use this again for Testing'):
                    if (model == 'text_generator') or (model =='sentiment_analysis'):
                        user_text_input = df_set['context']
                    else:
                        user_text_input = df_set['context']
                        question = df_set['question']

#MOdul Section - DataFrame
#gridoption = GridOptionsBuilder()
#grid_op = gridoption.configure_selection(selection_mode="single")
#grid_response = AgGrid(df_log, width='100%', height=300,
#                        fit_columns_on_grid_load=True,
#                        gridOptions=grid_op ,data_return_mode='as_input')
#st.write(grid_response)
#selected = grid_response['selected_rows']
#selected_df = pd.DataFrame(selected)
#st.dataframe(selected_df) # CHK This with AgGrid
#send_to_API = st.button('Test API')
