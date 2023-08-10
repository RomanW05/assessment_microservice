import requests
import json
import jwt

main_url = 'http://127.0.0.1:8000'
user_credentials = {'username': 'test', 'password': '123'}


def get_restricted_access_token_login():
    result = requests.post(f'{main_url}/api/login/', data=user_credentials)
    assert result.status_code == 202
    result = result.json()
    restricted_access_token = result["access"]
    otp = result["otp"]
    return restricted_access_token, otp


def get_full_access_token_verify_otp():
    restricted_access_token, otp = get_restricted_access_token_login()
    data = {"otp": otp}

    headers = {
        "Accept-Charset": "utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {restricted_access_token}"
    }
    result = requests.post(f'{main_url}/api/verify_otp/', data=data, headers=headers)
    # print(result.text)
    assert result.status_code == 202, result.status_code
    result = result.json()
    tokens = result["auth"]
    tokens = json.loads(tokens)
    full_access_token = tokens["access"]
    
    return full_access_token


def test_dashboard_with_credentials():
    full_access_token = get_full_access_token_verify_otp()
    headers = {
        "Accept-Charset": "utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {full_access_token}"
    }
    result = requests.get(f'{main_url}/api/dashboard/', headers=headers)
    assert result.status_code == 200, result.status_code
    decoded_token = jwt.decode(full_access_token, options={"verify_signature": False})
    print(decoded_token)
    assert 'scope' in decoded_token





test_dashboard_with_credentials()