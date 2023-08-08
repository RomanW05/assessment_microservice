import json
import pytest
import requests
import unittest

from api import authentication, views


main_url = 'http://127.0.0.1:8000'


class TestGetEntryPoints(unittest.TestCase):

    def test_login(self):
        result = requests.get(f'{main_url}/api/login')
        assert result.status_code == 200


    def test_register(self):
        result = requests.get(f'{main_url}/api/register')
        assert result.status_code == 200


    def test_logout(self):
        result = requests.get(f'{main_url}/api/logout')
        assert result.status_code == 401


    def test_dashboard(self):
        result = requests.get(f'{main_url}/api/dashboard')
        assert result.status_code == 401



def test_login():
    credentials = {'username': 'test', 'password': '123'}
    result = requests.post(f'{main_url}/api/dashboard', data=credentials)
    result = json.dumps(result)
    access_token = result["access"]
    headers = {
        "Accept-Charset: utf-8",
        "Content-Type: application/x-www-form-urlencoded",
        f"Authorization: Bearer {access_token}" 
    }
    has_restricted_access = authentication.HasRestrictedScope.has_permission(requests.post(f'{main_url}/api/dashboard', headers=headers))
    assert has_restricted_access == True, f'{has_restricted_access}'
        # {"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjY4NTI2MywianRpIjoiNDBiMDkyZWY1ZDU2NGRjY2FmYzJlNDhiYWIxNzRiNzYiLCJ1c2VyX2lkIjoyLCJzY29wZSI6InJlc3RyaWN0ZWQifQ.XNNiTx8y_WXI48HSxccuvFiiyOXGYc5PuRTjouFIzJw","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTQxMjYzLCJqdGkiOiI0Y2RmOTA1MWFlNjI0NThmOTIwNDY5MWM5ZThmYjZhNiIsInVzZXJfaWQiOjIsInNjb3BlIjoicmVzdHJpY3RlZCJ9.yXAq8X7yvJjqLAHn8jZdBLlQ6ExzMwU6jmqXBXDDVmo"}
    # print(result)