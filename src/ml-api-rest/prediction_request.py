import requests
import json 
import pprint

url = "http://127.0.0.1:5000/predictFeaturesFromTitle"
params = {"title": "Apple iPhone 4S Plus Smartphone with some 4 GB RAM - blue"}

response = requests.get(url, params)

pprint.pprint(response.json())
