######################################        Under construction
#Imports
import requests
import pandas as pd

#Definitions
def intro():
    print("Hello this is StudieGrupp1's (JSzZ) Program :)")
    return

def start_API(model_name):
    pass

def main_program ():
    pass
    
#Main area :)
if __name__ == "__main__":
    """    
    #Inicialization - API per ML-Model, StreamLit, SQLite
    DB = 'http://localhost:8000'
    WebApp = 'http://localhost:5000'
    AI_modell = 'http://localhost:8080'
    endpoint = AI_modell + '/data' #Here we have to define the "DB" source

    r = requests.get(url=endpoint)
    data = r.json()
    r.status_code
    """

    #START our ML-model API
    url = "http://localhost:8000/start" 
    body = {"name": "sentimen_analysis"} # Need to be customized based on ML-Model
    requests.post(url, json = body)
    #START one exact ML-model
    model = "http://localhost:8000/sentiment_analysis/" # Need to be customized based on ML-Model
    #Customized INPUT to the ML-model
    body = {"context": "I hate it"} # Need to be customized based on ML-Model
    response = requests.post(model, json = body)
    print(response.json())
    #INSERT to the DB


    #Argparse inputs if it is necessary :)

    #Info to User
    intro()
    #Processing the Program :)
    main_program()

    print("That's all folks :D")