import json

import pytest
from dbconnection import connectdb as db
user_collection=db().user
# from db_access import db_action


def register(client, user_json):
    return client.post('/user/register', data=user_json, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_register_success(client):
    user_obj = {"firstName": "Janaki", "lastName": "Wijewickrama", "email": "janaki@gmail.com", "password":"Janaki123@"}
    user_json = json.dumps(user_obj)
    response = register(client, user_json)
    data = response.data

    assert response.status_code == 201
    assert 'Successfully Registered' in data.values()

    user_collection.delete_one({"email":"janaki@gmail.com"})
    # db_action("remove_one", [{"email": "james@gmail.com"}, "users"], "admin")

@pytest.mark.usefixtures("client")
def test_register_email_exists(client):
    user_obj = {"firstName": "Jagath", "lastName": "Weerasuriya", "email": "janaki@gmail.com", "password":"Jagath123@"}
    user_json = json.dumps(user_obj)
    response1 = register(client, user_json)
    response = register(client, user_json)
    data = response.data
    print(data)
    assert response.status_code == 409
    assert 'Email already inuse.' in data.values()
    # {"email": email}
    # user_collection.delete_one({"email":"janak@gmail.com"})
    # db_action("remove_one", [{"email": "abc@gmail.com"}, "users"], "admin")
