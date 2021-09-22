import streamlit as st
#from PIL import image

#from API_interface.py import *

st.header('Hello and Welcome!')

page = st.sidebar.selectbox('Choose', ['Register', 'Login'])

if page =='Register':
    with st.form('New User'):
    #st.write('New User')
        user_name = st.text_input('Please enter your user name')
        password= st.text_input('Chooes a password')
        finished =st.form_submit_button('Register')
    if finished:
        # call a function
        # register to db

        pass


elif page=='Login':
    with st.form('Login'):
        user_name = st.text_input('Please enter your user name')
        password= st.text_input('Enter your password')
        finished =st.form_submit_button('Login')
    if finished:
        # call a function,
        # compare to db
         st.write('Hello', user_name)


chosen_model= st.sidebar.selectbox('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'])


#user_input= st.multiselect('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'], ['Text Generator'])
st.write('You made your choice', chosen_model, '!')
if st.button('Shoot'):
    if chosen_model == 'QA':
        user_text_input = st.text_input('What say you?')
        user_question= st.text_input('.. and the question?')

    else:
        user_text_input = st.text_input('What say you?')

    st.write('lets see...')




# ml api blöa bla
# st.write('models answer')
# save save save and send to database




