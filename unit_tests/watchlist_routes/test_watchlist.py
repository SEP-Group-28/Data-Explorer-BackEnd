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
def test_view_watchlist_success(client):
    token = login(client)
    response = client.get('/watchlist/view', headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "brands" in data.keys()
    assert False in data.values()

@pytest.mark.usefixtures("client")
def test_view_no_watchlist(client):
    cred_obj = {"creds": {"email": "x@gmail.com", "password": "abcd1234"}}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data)
    token = login_data['token']

    response = client.get('/watchlist/view', headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Watchlist is empty" in data.values()
    assert True in data.values()

@pytest.mark.usefixtures("client")
def test_add_to_watchlist_success(client):
    token = login(client)
    brands = ['BNBBTC']
    brands_obj = json.dumps({"brands": brands})
    response = client.post('/watchlist/addBrand', data=brands_obj, headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Successful" in data.values()
    assert False in data.values()
    client.delete('/watchlist/removeBrand', data=json.dumps({"brands": brands[0]}), headers={'x-access-token': token}, follow_redirects=False)

#
@pytest.mark.usefixtures("client")
def test_remove_watchlist_success(client):
    token = login(client)
    brand = 'BNBUSDT'
    brands_obj = json.dumps({"brands": brand})
    response = client.delete('/watchlist/removeBrand', data=brands_obj, headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Successfully updated the watch list" in data.values()
    assert False in data.values()
    client.post('/watchlist/addBrand', data=json.dumps({"brands": [brand]}), headers={'x-access-token': token}, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_remove_watchlist_empty(client):
    cred_obj = {"creds": {"email": "x@gmail.com", "password": "abcd1234"}}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data)
    token = login_data['token']
    brand = 'BNBUSDT'
    brands_obj = json.dumps({"brands": brand})
    response = client.delete('/watchlist/removeBrand', data=brands_obj, headers={'x-access-token': token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "No watch_list available for the given email" in data.values()
    assert True in data.values()
