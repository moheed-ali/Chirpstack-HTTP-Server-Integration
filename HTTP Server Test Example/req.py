import requests

url = "http://localhost:8081/?event=up"
#url = "http://127.0.0.1:8081/?event=up"
data = "Hello, ChirpStack!"
response = requests.post(url, data)

print(response.text)