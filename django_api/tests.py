"""
All endpoints and cases to cover:
    Endpoints:
        1. Register new user
        2. Login with credentials
        3. Verify otp
        4. Access dashboard with and without credentials
        5. Logout
        6. Access dashboard with outdated JWT

    Cases:
        . All right
            - Register success
            - Login success
            - Verify OTP success
        . Restricted access token tries access:
            - Dashboard
            - Logout
        . Full access token tries access:
            - Verify OTP
            - Dashboard
            - Logout
        . Blacklisted token tries access
            - Verify OTP
            - Dashboard
            - Logout

"""

import json
import jwt
import pytest
import requests
import unittest



main_url = 'http://127.0.0.1:8000'
user_credentials = {'username': 'test', 'password': '123'}
user_credentials = {"email": "testemail123@gmail.com", "password": "dhn4h.,23f", "username": "new_username_test"}

def create_api_call(token, method, url):
    headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    if method == 'post':
        result = requests.post(f'{main_url}/{url}/', headers=headers)
    elif method == 'get':
        result = requests.get(f'{main_url}/{url}/', headers=headers)
    elif method == 'delete':
        result = requests.delete(f'{main_url}/{url}/', headers=headers)
    elif method == 'update':
        result = requests.update(f'{main_url}/{url}/', headers=headers)
    else:
        raise TypeError

    return result



def headers(token):
    headers = {
            "Accept-Charset": "utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}"
        }
    return headers


# Retrieving the right codes
class TestEntryPoints(unittest.TestCase):
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
    

    def test_delete_get(self):
        result = requests.get(f'{main_url}/api/delete')
        assert result.status_code == 401
    

    def test_delete_post(self):
        result = requests.get(f'{main_url}/api/delete')
        assert result.status_code == 401





class TestAllRight():
    def test_delete_user(self):
        self.get_restricted_access_token()
        self.get_full_access_token()
        old_user = json.dumps(user_credentials)

        result = requests.post(f'{main_url}/api/delete/', data=old_user)
        assert result.status_code == 205

    def test_register_new_user(self):
        new_user = json.dumps(user_credentials)
        result = requests.post(f'{main_url}/api/register/', data=new_user)
        if result.status_code == 415:
            self.test_delete_user()
            result = requests.post(f'{main_url}/api/register/', data=new_user)
        assert result.status_code == 201


    def get_restricted_access_token(self):
        result = requests.post(f'{main_url}/api/login/', data={"username":user_credentials["username"], "password":user_credentials["password"]})
        assert result.status_code == 202
        result = result.json()
        self.restricted_access_token = result["access"]
        self.otp = result["otp"]
        decoded_token = jwt.decode(self.restricted_access_token, options={"verify_signature": False})
        assert decoded_token['scope'] == 'restricted'
        

    def get_full_access_token(self):
        self.get_restricted_access_token()
        data = {"otp": self.otp}
        headers = self.headers_function(self.restricted_access_token)
        result = requests.post(f'{main_url}/api/verify_otp/', data=data, headers=headers)
        assert result.status_code == 202, result.status_code
        result = result.json()
        tokens = result["auth"]
        tokens = json.loads(tokens)
        self.full_access_token = tokens["access"]
        decoded_token = jwt.decode(self.full_access_token, options={"verify_signature": False})
        assert decoded_token['scope'] == 'full'


    def test_dashboard(self):
        self.get_full_access_token()
        headers = self.headers_function(self.full_access_token)
        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 200, result.status_code
    

    def test_logout(self):
        self.test_dashboard()
        headers = self.headers_function(self.full_access_token)
        result = requests.post(f'{main_url}/api/logout/', headers=headers)
        assert result.status_code == 204
    

    def get_all_tokens(self):
        self.get_restricted_access_token()
        self.get_full_access_token()

    
    @classmethod
    def headers_function(cls, token):
        headers = {
                "Accept-Charset": "utf-8",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {token}"
            }
        return headers


class TestRestrictedAccess(TestAllRight):
    def test_dashboard(self):
        self.get_restricted_access_token()
        headers = self.headers_function(self.restricted_access_token)
        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 403, result.status_code


class TestWrongCredentials(TestAllRight):
    def test_dashboard_restricted_access(self):
        self.get_full_access_token()
        headers = self.headers_function(self.restricted_access_token)
        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 403, result.status_code

        headers = self.headers_function(self.full_access_token)
        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 200, result.status_code
    

    def test_logout_blacklist_token(self):
        self.get_full_access_token()
        self.test_logout()

        headers = self.headers_function(self.full_access_token)
        result = requests.post(f'{main_url}/api/logout/', headers=headers)
        assert result.status_code == 403

        result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
        assert result.status_code == 403



