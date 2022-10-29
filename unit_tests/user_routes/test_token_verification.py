import json

import pytest

from unit_tests.user_routes import test_login

def login(client):
    cred_obj = {"creds": {"email": "z@gmail.com", "password": "abcd1234"}}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data)
    token = login_data['token']
    return token


@pytest.mark.usefixtures("client")
def test_verification_success(client):
    token = login(client)
    response = client.get('/user/test', headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'OK' in data.values()

@pytest.mark.usefixtures("client")
def test_token_missing(client):
    response = client.get('/user/test', follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 401
    assert 'Token is missing!' in data.values()

@pytest.mark.usefixtures("client")
def test_token_invalid(client):
    token = 'sfsdfdf'
    response = client.get('/user/test', headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 401
    assert 'Token is invalid!' in data.values()