import streamlit as st
from st_aggrid import AgGrid
from PIL import Image
import DB_Handling
from API_interface import API_Requests

st.set_page_config(layout="wide")
page = st.sidebar.selectbox('Vilken sida vill du se',
                    ['Registration', 'Login'])

if page == 'Registration':
    ML_db = DB_Handling.MLModel_DB('DB_ML_History.db')
    st.header('Du är på Registration Sida')
    with st.form('Registration form'):
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

else: #LOGIN Section
    ML_db = DB_Handling.MLModel_DB('DB_ML_History.db')
    st.header('Du är på Login Sida')
    with st.form('Login form'):
        user_name = st.text_input('Please enter your user name')
        password = st.text_input('Please give you password')
        doit = st.form_submit_button('Submit :)')        
        if doit:     
            if ML_db.chk_account_if_exists(user_name):
                df_user = ML_db.login(user_name, password)
                if df_user.empty:
                    st.write ('Try again') 
                else :
                    models = API_Requests.models
                    chosen_model= st.selectbox('Please select a model', models)
                    if not chosen_model == 'question_answering':
                        user_context = st.text_input('Please type below')
                        user_question= None
                        send_to_API = st.form_submit_button('Send')
                    else:
                        user_context = st.text_input('Please type below')
                        user_question= st.text_input('.. and the question?')
                        send_to_API = st.form_submit_button('Send')
            else:
                st.write('This account name does not exists. Tyr with another one, please')

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
