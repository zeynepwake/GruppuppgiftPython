######################################        Under construction
import streamlit as st
import requests
#from transformers import pipeline

def greet(name):
    return f'Hello {name} nice to see you here again :)'

st.write('Hello. ML-Model Testing :)')
user_name = st.text_input('What is your name?')
st.write('Which ML-Model would you like to test')
model = st.selectbox('Select en option', ['Sentimental Analysis'])
model = st.checkbox('Sentimental Analysis')
model = st.checkbox('Text Generator')
model = st.checkbox('Question Anvwer')
model = st.checkbox('Pic analys')
user_context = st.text_input('Give a context:')
if st.button('Check it out :)'):  # Boolean lesz ha lenyomod
    #print('You clicked on the button') # a PRINT csak a terminalra ir ki valamit
    welcome = greet(user_name)
    st.write(welcome)
    st.write(f'Your choose {model} Model.')

    #START our ML-model API - Example
    url = "http://localhost:8000/start" 
    body = {"name": "sentiment_analysis"} # Need to be customized based on ML-Model
    requests.post(url, json = body)
    #START one exact ML-model
    model = "http://localhost:8000/sentiment_analysis/" # Need to be customized based on ML-Model
    #Customized INPUT to the ML-model
    body = {"context": user_context} # Need to be customized based on ML-Model
    response = requests.post(model, json = body)
    print(response.json())
    st.write(f'Based on ML Model: {response.json()}')

    #INSERT to the DB



