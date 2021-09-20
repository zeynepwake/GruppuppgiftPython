import streamlit as st

st.write('Hello and Welcome!')
user_name = st.text_input('What shall we call you?')
st.button('Enter and Save')
st.write('Hello', user_name,'!')
#user_input= st.selectbox('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'])
user_input= st.multiselect('Please select a model', ['Text Generator', 'Sentimental Analysis', 'QA'], ['Text Generator'])

