import json

import pytest

from unit_tests.auth_routes import test_login

def login(client):
    cred_obj = {"email": "thu@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data =json.loads(login_res.data) 
    token = login_data['access_token']
    return token


@pytest.mark.usefixtures("client")
def test_view_watchlist_success(client):
    token = login(client)
    response = client.get('/view-watchlist', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['data'])
    assert type(data['data'])==list and len(data['data'])>0
    assert 'Successfully get watchlist' in data.values()


@pytest.mark.usefixtures("client")
def test_add_to_watchlist_success(client):
    token = login(client)
    market_name = 'BNB/USDT'
    brands_obj = json.dumps({"crypto": market_name})
    response = client.post('/add-market', data=brands_obj, headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    assert response.status_code == 200
    assert "Successfully added to watchlist" in data.values()
    assert market_name in data['data']
    client.delete('/remove-market', data=json.dumps({"crypto": market_name}),headers={'Authorization': "Bearer "+ token}, follow_redirects=False)

@pytest.mark.usefixtures("client")
def test_already_exist_in_watchlist(client):
    token = login(client)
    market_name = 'ETH/USDT'
    brands_obj = json.dumps({"crypto": market_name})
    response = client.post('/add-market', data=brands_obj, headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    assert response.status_code == 200
    assert "Crypto type already added" in data.values()
    assert market_name in data['data']

@pytest.mark.usefixtures("client")
def test_remove_watchlist_success(client):
    token = login(client)
    market_name = 'SOL/USDT'
    brands_obj = json.dumps({"crypto": market_name})
    response = client.delete('/remove-market', data=brands_obj, headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Successfully remove crypto from watchlist" in data.values()
    # assert False in data.values()
    assert market_name not in data['data']
    client.post('/add-market', data=json.dumps({"crypto": market_name}), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)


@pytest.mark.usefixtures("client")
def test_remove_watchlist_empty(client):
    cred_obj = {"email": "thur@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data)
    token = login_data['access_token']
    brand = 'BTC/USDT'
    brands_obj = json.dumps({"crypto": brand})
    response = client.delete('/remove-market', data=brands_obj,headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 400
    print(data)
    assert "No watchlist for this user" in data.values()
    assert False in data.values()

@pytest.mark.usefixtures("client")
def test_view_no_watchlist(client):
    cred_obj = {"email": "thur@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data = json.loads(login_res.data)
    token = login_data['access_token']
    response = client.get('/view-watchlist', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Watchlist is empty" in data.values()
    assert False in data.values()
