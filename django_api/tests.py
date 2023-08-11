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
        . Test access
            - Verify OTP
            - Dashboard
            - Logout
            - Delete account
        . Test access with restricted token
        . Test access with full token
        . Test access with blacklisted token

"""

import json
import jwt
import pytest
import requests
import unittest
import abc



main_url = 'http://127.0.0.1:8000'
user_credentials = {"email": "testemail123@gmail.com", "password": "dhn4h.,23f", "username": "new_username_test"}


# Retrieving the right codes
class TestEntryPoints(unittest.TestCase):
    def test_register_get(self):
        result = requests.get(f'{main_url}/api/register/')
        assert result.status_code == 200
    

    def test_register_post(self):
        result = requests.post(f'{main_url}/api/register/')
        assert result.status_code == 409


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
    def test_register_new_user(self):
        result = requests.post(f'{main_url}/api/register/', data=user_credentials)
        if result.status_code == 409:  # User already exists
            pass
        else:
            assert result.status_code == 201


    def get_restricted_access_token(self):
        result = requests.post(f'{main_url}/api/login/', data=user_credentials)
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


class CaseTestAccess(TestAllRight):
    @abc.abstractmethod
    def get_specific_token(self):
        pass


    def test_dashboard(self):
        self.get_specific_token()
        result = requests.get(f'{main_url}/api/dashboard/', headers=self.headers)
        assert result.status_code == self.status_code_test_dashboard
    

    def test_logout(self):
        self.get_specific_token()
        result = requests.post(f'{main_url}/api/logout/', headers=self.headers)
        assert result.status_code == self.status_code_test_logout
    

    def test_verify_otp(self):
        self.get_specific_token()
        data = {"otp": 123456}
        result = requests.post(f'{main_url}/api/verify_otp/', data=data, headers=self.headers)

        assert result.status_code == self.status_code_test_verify_otp
    

    def test_delete_user(self):
        self.get_specific_token()
        result = requests.post(f'{main_url}/api/delete/', data=user_credentials, headers=self.headers)
        assert result.status_code == self.status_code_test_delete_user


class TestAccessRestrictedToken(CaseTestAccess):
    def get_specific_token(self):
        self.test_register_new_user()
        self.get_restricted_access_token()
        self.headers = self.headers_function(self.restricted_access_token)
        self.status_code_test_delete_user = 403
        self.status_code_test_dashboard = 403
        self.status_code_test_logout = 403
        self.status_code_test_verify_otp = 400


class TestAccessFullToken(CaseTestAccess):
    def get_specific_token(self):
        self.test_register_new_user()
        self.get_all_tokens()
        self.headers = self.headers_function(self.full_access_token)
        self.status_code_test_delete_user = 205
        self.status_code_test_dashboard = 200
        self.status_code_test_logout = 204
        self.status_code_test_verify_otp = 403


class TestAccessBlacklistedToken(CaseTestAccess):
    def get_specific_token(self):
        self.test_register_new_user()
        self.get_all_tokens()
        self.headers = self.headers_function(self.full_access_token)
        result = requests.post(f'{main_url}/api/logout/', headers=self.headers)
        assert result.status_code == 204
        self.status_code_test_delete_user = 403
        self.status_code_test_dashboard = 403
        self.status_code_test_logout = 403
        self.status_code_test_verify_otp = 403
