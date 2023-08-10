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