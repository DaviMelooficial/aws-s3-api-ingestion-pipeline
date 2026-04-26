import requests
import json

def extract_data(url):

    response = requests.get(url)

    data = response.json()
    
    data_json = json.dumps(data)

    return data_json