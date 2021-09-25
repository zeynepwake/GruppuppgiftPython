import streamlit as st
import sqlite3
import pandas as pd
import DB_Handling
from API_interface import API_Requests


st.header('Models by Jakob, Szandra and Zeynep!')


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = ''

st.write(st.session_state['logged_in'])

page = st.sidebar.selectbox('Page', ['Register', 'Login', 'Models'])

ml_db = DB_Handling.MLModel_DB('DB_ML_History.db')
ml_db.create_db()

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
            st.write('Logged in')

if page == 'Register':
    col1, col2 = st.columns(2)
    with col1:
        first_name =st.text_input('Enter your name')
        last_name =st.text_input('Enter your last name')
    with col2:
        user_name = st.text_input('Please enter your user name')
        password = st.text_input('Choose a password', type='password')
        if st.button('Register'):
            if not ml_db.chk_account_if_exists(user_name):
                ml_db.create_user(user_name, password, first_name, last_name)
                st.write('User register. Please log in')
            else:
                st.write('Accountname already exists. Please try another one.')


if page == 'Models':
    if not st.session_state['logged_in'] == True:
        st.write('Please log in')
    else:
        st.write(f"Logged in as {st.session_state['user']}")

        model = st.selectbox('Select a model', API_Requests.models)
        if st.button('Start model'):
            API_Requests.start_model(model)
            st.write('Model started')

        if model == 'text_generator':
            user_text_input = st.text_input('Please type below')
            response = API_Requests.post_generator(user_text_input)
            st.write(response.json())

        elif model =='sentiment_analysis':
            user_text_input = st.text_input("Please type below")
            response =  API_Requests.post_sentiment(user_text_input)
            st.write(response.json())

        elif model =='qa':
            user_text_input = st.text_input("Please type below")
            question = st.text_input("What would you like to ask?")
            response =  API_Requests.post_qa(user_text_input, question)
            st.write(response.json())


        






