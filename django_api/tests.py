"""
All endpoints and cases to cover:
    1. Register new user
    2. Login with credentials
    3. Verify otp
    4. Access dashboard with and without credentials
    5. Logout
    6. Access dashboard with outdated JWT

Retrieving the right codes:
    1. Register
    2. Login
    3. Verify otp
    4. Dashboard
    5. Logout
"""

import json
import jwt
import pytest
import requests
import unittest



main_url = 'http://127.0.0.1:8000'
user_credentials = {'username': 'test', 'password': '123'}


# Retrieving the right codes
class TestGetEntryPoints(unittest.TestCase):
    def test_register_get(self):
        result = requests.get(f'{main_url}/api/register/')
        assert result.status_code == 200
    

    def test_register_post(self):
        result = requests.post(f'{main_url}/api/register/')
        assert result.status_code == 400


    def test_login_get(self):
        result = requests.get(f'{main_url}/api/login/')
        assert result.status_code == 200


    def test_login_post(self):
        result = requests.post(f'{main_url}/api/login/')
        assert result.status_code == 400
    

    # Has no credentials so 401
    def test_verify_otp_get(self):
        result = requests.get(f'{main_url}/api/verify_otp/')
        assert result.status_code == 401


    # Has no credentials so 401
    def test_logout_post(self):
        result = requests.post(f'{main_url}/api/logout/')
        assert result.status_code == 401


    def test_dashboard(self):
        result = requests.get(f'{main_url}/api/dashboard')
        assert result.status_code == 401






class TestCredentials():
    # def __init__(self) -> None:
    #     self.get_restricted_access_token_login()
    #     self.get_full_access_token_verify_otp()
    #     self.test_dashboard_with_credentials()

    def get_restricted_access_token_login(self):
        result = requests.post(f'{main_url}/api/login/', data=user_credentials)
        assert result.status_code == 202
        result = result.json()
        self.restricted_access_token = result["access"]
        self.otp = result["otp"]
        decoded_token = jwt.decode(self.restricted_access_token, options={"verify_signature": False})
        assert decoded_token['scope'] == 'restricted'
        
        # return restricted_access_token, otp


    def get_full_access_token_verify_otp(self):
        # restricted_access_token, otp = self.get_restricted_access_token_login()
        data = {"otp": self.otp}

        headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.restricted_access_token}"
        }
        result = requests.post(f'{main_url}/api/verify_otp/', data=data, headers=headers)
        # print(result.text)
        assert result.status_code == 202, result.status_code
        result = result.json()
        tokens = result["auth"]
        tokens = json.loads(tokens)
        self.full_access_token = tokens["access"]
        decoded_token = jwt.decode(self.full_access_token, options={"verify_signature": False})
        assert decoded_token['scope'] == 'full'

        
        # return full_access_token


    def test_dashboard_with_credentials(self):
        self.get_restricted_access_token_login()
        self.get_full_access_token_verify_otp()
        # full_access_token = self.get_full_access_token_verify_otp()
        headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.full_access_token}"
        }
        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 200, result.status_code



# credentials_testing = TestCredentials()
# assert credentials_testing.full_access_token