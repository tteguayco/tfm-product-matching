import requests

url = "http://127.0.0.1:5000/predictFeaturesFromTitle"
params = {"title": "Apple iPhone 4S Plus Smartphone with some 4GB RAM - Blue"}
response = requests.get(url, params)
print(response.json())
