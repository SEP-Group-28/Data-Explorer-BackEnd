import json

import pytest

# from unit_tests.user_routes import test_login
import test_login

def login(client):
    cred_obj = {"email": "thu@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data) 
    print(login_data)
    token = login_data['access_token']
    return token

#  headers: {Authorization: `Bearer ${token.getAccessToken()}`}
@pytest.mark.usefixtures("client")
def test_verification_success(client):
    token = login(client)
    response = client.get('/auth/test', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    assert response.status_code == 200
    assert 'OK' in data.values()

@pytest.mark.usefixtures("client")
def test_token_missing(client):
    response = client.get('/auth/test', follow_redirects=False)
    data =json.loads(response.data) 
    assert response.status_code == 401
    assert 'Authentication Token is missing!' in data.values()

@pytest.mark.usefixtures("client")
def test_token_invalid(client):
    token = 'sfsdfdf'
    response = client.get('/auth/test', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    assert response.status_code == 401
    assert 'Invalid Authentication token!' in data.values()