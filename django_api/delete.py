import requests
import json

data = json.dumps({"email":"testemail123@gmail.com", "username":"new_username_test", "password":"dhn4h.,23f"})
headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json",
        }
results = requests.post('http://127.0.0.1:8000/api/register/', data=data, headers=headers)
print(results.text)

results = requests.post('http://127.0.0.1:8000/api/login/', data=data, headers=headers)
print(results.text)