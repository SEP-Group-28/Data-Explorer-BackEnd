import json

import pytest

from unit_tests.user_routes import test_login

def login(client):
    cred_obj = {"email": "thu@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = login_res.data
    token = login_data['access_token']
    return token


@pytest.mark.usefixtures("client")
def test_view_watchlist_success(client):
    token = login(client)
    response = client.get('/view-watchlist', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = response.data
    assert response.status_code == 200
    assert "brands" in data.keys()
    assert False in data.values()

@pytest.mark.usefixtures("client")
def test_view_no_watchlist(client):
    cred_obj = {"email": "thur@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = login_res.data
    token = login_data['access_token']

    response = client.get('/view-watchlist', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = response.data
    assert response.status_code == 200
    assert "Watchlist is empty" in data.values()
    assert True in data.values()

@pytest.mark.usefixtures("client")
def test_add_to_watchlist_success(client):
    token = login(client)
    brands = ['BTC/USDT']
    brands_obj = json.dumps({"crypto": brands})
    response = client.post('/add-market', data=brands_obj, headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = response.data
    assert response.status_code == 200
    assert "Successful" in data.values()
    assert False in data.values()
    client.delete('/remove-market', data=json.dumps({"crypto": brands[0]}),headers={'Authorization': "Bearer "+ token}, follow_redirects=False)

#
@pytest.mark.usefixtures("client")
def test_remove_watchlist_success(client):
    token = login(client)
    brand = 'BTC/USDT'
    brands_obj = json.dumps({"crypto": brand})
    response = client.delete('/remove-market', data=brands_obj, headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = response.data
    assert response.status_code == 200
    assert "Successfully updated the watch list" in data.values()
    assert False in data.values()
    client.post('/add-market', data=json.dumps({"crypto": [brand]}), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_remove_watchlist_empty(client):
    cred_obj = {"email": "thush@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = login_res.data
    token = login_data['access_token']
    brand = 'BTC/USDT'
    brands_obj = json.dumps({"crypto": brand})
    response = client.delete('/remove-market', data=brands_obj,headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = response.data
    assert response.status_code == 200
    assert "No watch_list available for the given email" in data.values()
    assert True in data.values()
