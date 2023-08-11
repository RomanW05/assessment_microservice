import requests
import json
import sys
data = json.dumps({"email":"testemail123@gmail.com", "username":"new_username_test", "password":"dhn4h.,23f"})
headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json",
        }
results = requests.post('http://127.0.0.1:8000/api/register/', data=data, headers=headers)
print(results.status_code)
sys.exit()
results = requests.post('http://127.0.0.1:8000/api/login/', data=data, headers=headers)
results = json.loads(results.text)
token = results['access']
otp = results['otp']


headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
data = {"otp": otp}

results = requests.post('http://127.0.0.1:8000/api/verify_otp/', data=json.dumps(data), headers=headers)
results = json.loads(results.text)
token = results['auth']
token = json.loads(token)
token = token['access']
headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }


data = json.dumps({"email":"testemail123@gmail.com", "username":"new_username_test", "password":"dhn4h.,23f"})
result = requests.post('http://127.0.0.1:8000/api/delete/', data=data, headers=headers)
print(result.status_code)
