import os.path
import requests
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

page = st.sidebar.selectbox('Page', ['Register', 'Login', 'Models'])
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
                    user_text_input = st.text_input("Please type below")
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
            df_log = ml_db.log_query(st.session_state['user'])
            df_view = df_log[df_log['name'] == model]
            if df_view.empty:
                st.write('It seams this is your first test. Cool :)... Do not forget to start the model')
            else:
                st.dataframe(df_view[['context', 'question']])
                selected_index = st.selectbox('Select index',list(df_view.index))
                selected_element = df_view.loc[int(selected_index),:]
                st.write(selected_element.loc['context'])
                if st.button('Submit old input'):
                    if model == 'sentiment_analysis':
                        response = API_Requests.post_sentiment(selected_element.loc['context'])
                        st.write(response.json())
                    if model == 'question_answering':
                        response = API_Requests.post_qa(selected_element.loc['context'],
                                                                selected_element.loc['question'])
                        st.write(response.json())
                    if model == 'text_generator':
                        response = API_Requests.post_generator(selected_element.loc['context'])
                        st.write(response.json())
