import json
import pytest


def login(client, cred_json):
    return client.post('/auth/login', data=cred_json, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_login_success(client):
    # cred_obj = {"creds": {"email": "z@gmail.com", "password": "abcd1234"}}
    cred_obj = {"email": "thu@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    print(response)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'Login Successful!' in data.values()
    assert 'token' in data.keys()

@pytest.mark.usefixtures("client")
def test_login_incomplete(client):
    # cred_obj = {"creds": {"email": "z@gmail.com"}}
    cred_obj = {"email": "thur@gmail.com"}

    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'All fields are required for logging in' in data.values()
    assert 'token' not in data.keys()

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    # cred_obj = {"creds": {"email": "z@gmail.com", "password": "abcds1234"}}
    cred_obj = {"email": "thur@gmail.com", "password": "abcds1234"}

    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'Wrong Username or Password' in data.values()
    assert 'token' not in data.keys()

@pytest.mark.usefixtures("client")
def test_login_incorrect_email(client):
    cred_obj = {"email": "thu12@gmail.com", "password": "abcds1234"}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'Wrong Username or Password' in data.values()
    assert 'token' not in data.keys()