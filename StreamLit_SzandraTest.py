import streamlit as st
from PIL import Image
import DB_Handling

page = st.sidebar.selectbox('Vilken sida vill du se',
                    ['Registration', 'Login'])
if page == 'Registration':
    ML_db = DB_Handling.MLModel_DB('DB_ML_History.db')
    st.header('Du är på Registration Sida')
    #Här kommer alla kod för Sida 1
    with st.form('This is a Regform'):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input('Enter your first name')
            last_name = st.text_input('Enter your last name')
        with col2:
            user_name = st.text_input('Please enter your user name')
            password = st.text_input('Choose a password')
        
        doit = st.form_submit_button('Submit :)') # Ez csak a formon belul mukodik
    if doit:     
        if ML_db.chk_account_if_exists(user_name):
            st.write('Accountname exists. Try another one.')
        else: 
            ML_db.create_user(user_name, password, first_name, last_name)
            st.write('You are registered. Please Log In')

else:
    st.write('Du är på Login')
    #Här kommer alla kod för Sida 2