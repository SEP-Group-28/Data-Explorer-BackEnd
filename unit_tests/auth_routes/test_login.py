import json
import pytest
import logging as log

def login(client, cred_json):
    return client.post('/auth/login', data=cred_json, follow_redirects=False)


def login_success(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    assert response.status_code == 200
    assert 'Login successful' in data.values()
    assert 'access_token' in data.keys()


def login_incomplete(client,email):
    cred_obj = {"email": email}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    assert response.status_code == 400
    assert 'All fields are required for logging in' in data.values()
    assert 'access_token' not in data.keys()

# @pytest.mark.usefixtures("client")
def login_incorrect_password(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    assert response.status_code == 401
    assert 'Password is incorrect...' in data.values()
    assert 'access_token' not in data.keys()

def login_password_with_no_uppercase_letter(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    print(data)
    assert response.status_code == 400
    assert 'Password must contain at least one uppercase letter' in data['error'].values()
    assert 'access_token' not in data.keys()

def login_password_with_no_lowercase_letter(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    print(data)
    assert response.status_code == 400
    assert 'Password must contain at least one lowercase letter' in data['error'].values()
    assert 'access_token' not in data.keys()

def login_password_with_no_number(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    print(data)
    assert response.status_code == 400
    assert 'Password must contain at least one number' in data['error'].values()
    assert 'access_token' not in data.keys()

def login_password_with_no_character(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    print(data)
    assert response.status_code == 400
    assert 'Password must contain at least one special character' in data['error'].values()
    assert 'access_token' not in data.keys()

@pytest.mark.usefixtures("client")
def test_login_incorrect_email(client):
    cred_obj = {"email": "thu12@gmail.com", "password": "Abcdefgh1234#"}
    cred_json = json.dumps(cred_obj)
    response = login(client, cred_json)
    data=json.loads(response.data)
    assert response.status_code == 404
    assert 'Email does not exist...' in data.values()
    assert 'access_token' not in data.keys()

@pytest.mark.usefixtures("client")
def test_login_success(client):
    login_success(client,'thu@gmail.com','Thush123@')
    login_success(client,'thur@gmail.com','Thush123@')
    login_success(client,'thura@gmail.com','Thush123@')
    login_success(client,'thula@gmail.com','Thush123@')
    login_success(client,'janith@gmail.com','Thush123@')
    login_success(client,'damintha@gmail.com','Thush123@')
    login_success(client,'nawanjana@gmail.com','Thush123@')
    login_success(client,'thula2@gmail.com','Thush123@')
    login_success(client,'wijekon@gmail.com','Thush123@')


@pytest.mark.usefixtures("client")
def test_login_incomplete(client):
    login_incomplete(client,'thur@gmail.com')
    login_incomplete(client,'thula@gmail.com')
    login_incomplete(client,'damintha@gmail.com')
    login_incomplete(client,'nawanjana@gmail.com')
    login_incomplete(client,'thur@gmail.com')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_incorrect_password(client,'thu@gmail.com','Asaf2@')
    login_incorrect_password(client,'thur@gmail.com','Asaf2@')
    login_incorrect_password(client,'thula@gmail.com','Asaf2@')
    login_incorrect_password(client,'damintha@gmail.com','Asaf2@')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_password_with_no_uppercase_letter(client,'thu@gmail.com','ssaf2@')
    login_password_with_no_uppercase_letter(client,'thur@gmail.com','ssaf2@')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_password_with_no_lowercase_letter(client,'thu@gmail.com','A2@')
    login_password_with_no_lowercase_letter(client,'thur@gmail.com','AF2@')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_password_with_no_number(client,'thu@gmail.com','Adfsdf@')
    login_password_with_no_number(client,'thur@gmail.com','Afsdaf@')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_password_with_no_character(client,'thu@gmail.com','Ad3fsdff')
    login_password_with_no_character(client,'thur@gmail.com','Af3sdaff')















