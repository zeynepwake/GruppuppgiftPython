import streamlit as st
import sqlite3
import pandas as pd
import DB_Handling
from API_interface import API_Requests
#import db_class_test

st.title('Models by Jakob, Szandra and Zeynep!')

page = st.sidebar.selectbox('Which page would you like to see?',
                    ['Register', 'Login'])

st.write('Please register or login :)')

#page = st.button('Register ') # add to db
#page = st.button('Login ') # compare to db
#register = st.sidebar.button('Register') # add to db
#login = st.sidebar.button('Login') # compare to db
#history = st.sidebar.button('My history') # connect to db
#st.text(register)
#st.text(login)

#if page == 'login_screen':

if page == "Register":
    ML_db = DB_Handling.MLModel_DB('DB_ML_History.db')
    st.header('You are on Registration Page')
    with st.form('Register'):
        col1, col2 = st.columns(2)
        with col1:
            first_name =st.text_input('Enter yourname')
            last_name =st.text_input('Enter your last name')
        with col2:
            user_name = st.text_input('Please enter your user name')
            password = st.text_input('Chooes a password')
        doit =st.form_submit_button('Submit')

        #finished =st.form_submit_button('Register')
        
        if doit:
            if ML_db.chk_account_if_exists(user_name):
                st.write('Accountname exists. Try another one.')
            else:
                ML_db.create_user(user_name, password, first_name, last_name)
            st.write('You are registered. Please Log In')
else:
    st.header('Please Login')
    



    #Här kommer alla kod för Sida 2
            #ML_db.create_user(user_name, password, first_name, last_name)
            
        

elif login:
    with st.form('Login'):
        user_name = st.text_input('Please enter your user name')
        password= st.text_input('Enter your password')
        finished =st.form_submit_button('Login')
    if finished:
        # call a function,
        # compare to db
        st.write('Hello', user_name)
        DB_Handling.MLModel_DB().login(user_name, password)

    

#st.title('MODEL')
chosen_model= st.sidebar.selectbox('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'])

if chosen_model == 'QA':
    user_text_input = st.text_input('Please type below')
    user_question= st.text_input('.. and the question?')
    st.button('Send')
    # to db samt to ml via api etc
else:
    user_text_input = st.text_input('Please type below')
    st.button('Send')




#st.write('lets see...')
#user_input= st.multiselect('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'], ['Text Generator'])
#st.write('You made your choice', chosen_model, '!')
#if st.button('Shoot'):


# ml api blöa bla
# st.write('models answer')
# save save save and send to database




