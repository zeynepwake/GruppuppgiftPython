import streamlit as st

#from API_interface.py import *

st.write('Hello and Welcome!')
st.button('REGISTER')
st.button('LOGIN')
user_name = st.text_input('What shall we call you?')
password= st.text_input('Please enter your password')


st.button('Enter and Save')
st.write('Hello', user_name,'!')
chosen_model= st.selectbox('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'])
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




