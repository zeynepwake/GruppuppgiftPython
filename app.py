import streamlit as st
import sqlite3
import pandas as pd
import DB_Handling
from API_interface import API_Requests
import os.path


st.header('Models by Jakob, Szandra and Zeynep!')


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = ''

if 'model_started' not in st.session_state:
    st.session_state['model_started'] = False

st.write(st.session_state['logged_in'])

page = st.sidebar.selectbox('Page', ['Register', 'Login', 'Models'])


if os.path.isfile('DB_ML_History.db'):
    ml_db = DB_Handling.MLModel_DB('DB_ML_History.db')
else: #If DB not exist: Create a DB struktur and initialize the DB.models with existing models from API
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
    if not st.session_state['logged_in'] == True:
        st.write('Please log in on the "Login" page')
    else:
        st.write(f"Logged in as {st.session_state['user']}")
        model = st.selectbox('Select a model', API_Requests.models)
        st.write(st.session_state['model_started'])
        if st.button('Start model'):
            API_Requests.start_model(model)
            st.session_state['model_started'] = True
            st.write('Model started')
        if not st.session_state['model_started'] == True:
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







