import requests
from pprint import pprint


BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "tweets/1633911273569284096")
pprint(response.json())