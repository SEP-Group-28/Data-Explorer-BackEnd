import json

import pytest

from db_access import db_action


def register(client, user_json):
    return client.post('/user/register', data=user_json, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_register_success(client):
    user_obj = {"user": {"firstName": "James", "lastName": "Anderson", "email": "james@gmail.com", "password":"abcd1234"}}
    user_json = json.dumps(user_obj)
    response = register(client, user_json)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert 'Successfully Registered' in data.values()

    db_action("remove_one", [{"email": "james@gmail.com"}, "users"], "admin")

@pytest.mark.usefixtures("client")
def test_register_email_exists(client):
    user_obj = {"user": {"firstName": "James", "lastName": "Anderson", "email": "abc@gmail.com", "password":"abcd1234"}}
    user_json = json.dumps(user_obj)
    response1 = register(client, user_json)
    response = register(client, user_json)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'Email already inuse.' in data.values()

    db_action("remove_one", [{"email": "abc@gmail.com"}, "users"], "admin")
