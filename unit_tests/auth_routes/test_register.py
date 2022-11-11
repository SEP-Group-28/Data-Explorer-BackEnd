import json

import pytest
from dbconnection import connectdb as db
user_collection=db().user

def register(client, user_json):
    return client.post('/auth/register', data=user_json, follow_redirects=False)



def register_success(client,firstname,lastname,email,password):
    user_obj = {"firstname": firstname, "lastname": lastname, "email": email, "password":password}
    user_json = json.dumps(user_obj)
    response = register(client, user_json)
    data=json.loads(response.data)
    assert response.status_code == 201
    assert 'Successfully created new user' in data.values()
    user_collection.delete_one({"email":email})


def register_email_exists(client,firstname,lastname,email,password):
    user_obj = {"firstname": firstname, "lastname": lastname, "email": email, "password":password}
    user_json = json.dumps(user_obj)
    response = register(client, user_json)
    data=json.loads(response.data)
    print(data)
    assert response.status_code == 409
    assert 'Email already exists...' in data.values()

@pytest.mark.usefixtures("client")
def test_register_success(client):
    register_success(client,'Janaki','Wijewickrama','janaki@gmail.com','Janaki@123')
    register_success(client,'Jagath','Weerasuriya','jagath@gmail.com','Jagath@123')
    register_success(client,'Thushalya','Weerasuriya','thushalya123@gmail.com','Thushalya@123')
    register_success(client,'Thulakshi','Weerasuriya','thulakshi123@gmail.com','Thulakshi@123')


@pytest.mark.usefixtures("client")
def test_register_email_exists(client):
    register_email_exists(client,'Janaki','Wijewickarama','thu@gmail.com','Thush@123')
    register_email_exists(client,'Jagath','Weerasuriya','thur@gmail.com','Thush@123')




