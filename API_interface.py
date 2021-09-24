import requests

class API_Requests:

    url = 'http://localhost:8000'
    models = ['text_generator', 'sentiment_analysis', 'image_classifier' ]
    current_model = None

    #--------------------------------------------------------#
    #Methods for starting different models from the API
    #--------------------------------------------------------#
    def start_model(model):
            r = requests.post(API_Requests.url + '/start', json = { 'name' : model})
            API_Requests.current_model = model
            return r
    #--------------------------------------------------------#
    #--------------------------------------------------------#

    def post_qa(context: str, question: str) -> requests.models.Response:
        """Makes a post request to the API for the question/answer model

        Args:
            context (str): The context for the question to be answered
            question (str): The question

        Returns:
            requests.models.Response: An instance of the Response type, 
            containing a JSON method to extract the answer from the model
        """
        if API_Requests.current_model == None:
            print('Select a model')
            return
        data = {"context": context, "question": question}
        r = requests.post(API_Requests.url + '/qa', json=data)
        return r

    def post_generator(context: str) -> requests.models.Response:
        """Makes a post request to the API for the text generation model

        Args:
            context (str): The context for the text being generated

        Returns:
            requests.models.Response: An instance of the Response type, 
            containing a JSON method to extract the answer from the model
        """
        if API_Requests.current_model == None:
            print('Select a model')
            return
        data = {"context": context}
        r = requests.post(API_Requests.url + '/text_generation', json=data)
        return r

    def post_sentiment(context: str) -> requests.models.Response:
        """Makes a post request to the API for the sentiment analysis model

        Args:
            context (str): The context for the evaluation

        Returns:
            requests.models.Response: Response: An instance of the Response type, 
            containing a JSON method to extract the answer from the model
        """
        if API_Requests.current_model == None:
            print('Select a model')
            return
        data = {"context": context}
        r = requests.post(API_Requests.url + '/sentiment_analysis', json=data)
        return r

    def post_image(file) -> requests.models.Response:
        if API_Requests.current_model == None:
            print('Select a model')
            return
        data = {'file':file}
        r = requests.post('http://localhost:8000/classify_image', files=data)
        return r

    def change_image_class(class1: str, class2: str, class3: str) -> requests.models.Response:
        if API_Requests.current_model == None:
            print('Select a model')
            return
        data = {"class_1": class1, "class_2": class2, "class_3": class3}
        r = requests.put('http://localhost:8000/change_classes', json=data)
        return r