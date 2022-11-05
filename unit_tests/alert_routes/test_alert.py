import json

import pytest
import jwt
import os
from unit_tests.auth_routes import test_login

def login(client):
    cred_obj = {"email": "thu@gmail.com", "password": "Thush123@"}
    cred_json = json.dumps(cred_obj)
    login_res = test_login.login(client, cred_json)
    login_data =json.loads(login_res.data) 
    token = login_data['access_token']
    return token


# @pytest.mark.usefixtures("client")
# def test_view_alert_list_success(client):
#     token = login(client)
#     response = client.get('/view-watchlist', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
#     data =json.loads(response.data) 
#     print('data...',data)
#     assert response.status_code == 200
#     print(data['data'])
#     assert type(data['data'])==list and len(data['data'])>0
#     assert 'Successfully get watchlist' in data.values()



@pytest.mark.usefixtures("client")
def test_add_alert_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    crypto_val=19000
    market_name='BTC'
    response = client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=crypto_val,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['alertlist'])
    alertlist=data['alertlist']
    assert type(alertlist)==list and [crypto_val,user_id] in alertlist
    assert 'Successfully added alert' in data.values()
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=crypto_val,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)

@pytest.mark.usefixtures("client")
def test_remove_alert_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    crypto_val=19000
    market_name='BTC'
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=crypto_val,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    response = client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=crypto_val,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['alertlist'])
    alertlist=data['alertlist']
    assert type(alertlist)==list and [crypto_val,user_id] not in alertlist
    assert 'Successfully removed alert' in data.values()


@pytest.mark.usefixtures("client")
def test_add_token_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    firebase_dummy_token='fdsfa432nknfds4n4nk'
    response = client.post('/alert/add-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['tokenlist'])
    tokenlist=data['tokenlist']
    print('token list..',tokenlist)
    assert type(tokenlist)==list and firebase_dummy_token in tokenlist
    assert 'Successfully added token' in data.values()
    client.delete('/alert/remove-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)

@pytest.mark.usefixtures("client")
def test_remove_token_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    firebase_dummy_token='fdsfa432nknfds4n4nk'
    client.post('/alert/add-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    response=client.delete('/alert/remove-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['tokenlist'])
    tokenlist=data['tokenlist']
    print('token list..',tokenlist)
    assert type(tokenlist)==list and firebase_dummy_token not in tokenlist
    assert 'Successfully removed token' in data.values()


@pytest.mark.usefixtures("client")
def test_get_alerts_for_crypto_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    market_name='BTC'
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    # client.post('/alert/add-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    response=client.get('/alert/get-alerts/{market_name}'.format(market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['allalertlistcrypto'])
    allalertlistcrypto=data['allalertlistcrypto']
    print('allalertlistcrypto..',allalertlistcrypto)
    assert type(allalertlistcrypto)==list  and 19500 in allalertlistcrypto and 23000 in allalertlistcrypto and 23500 in allalertlistcrypto
    assert 'Successfully fetched all alerts for crypto' in data.values()
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)

@pytest.mark.usefixtures("client")
def test_get_all_alerts_success(client):
    token = login(client)
    decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
    print('decoding',decoded_data)
    user_id=decoded_data['user_id']
    market_name='BTC'
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    market_name='SOL'
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.post('/alert/add-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    # client.post('/alert/add-token/{token}'.format(token=firebase_dummy_token), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    response=client.get('/alert/get-all-alerts', headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    data =json.loads(response.data) 
    print('data...',data)
    assert response.status_code == 200
    print(data['allalertlist'])
    allalertlist=data['allalertlist']
    print('allalertlist..',allalertlist)
    assert type(allalertlist)==list  and {'crypto_name':market_name+'/USDT','crypto_price':19500} in allalertlist and {'crypto_name':market_name+'/USDT','crypto_price':23000}  in allalertlist and {'crypto_name':market_name+'/USDT','crypto_price':23500}  in allalertlist
    market_name='BTC'
    assert type(allalertlist)==list  and {'crypto_name':market_name+'/USDT','crypto_price':19500} in allalertlist and {'crypto_name':market_name+'/USDT','crypto_price':23000}  in allalertlist and {'crypto_name':market_name+'/USDT','crypto_price':23500}  in allalertlist
    assert 'Successfully fetched all alerts' in data.values()
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    market_name='SOL'
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=19500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23000,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)
    client.delete('/alert/remove-alert/{market_name}/{crypto_val}'.format(crypto_val=23500,market_name=market_name), headers={'Authorization': "Bearer "+ token}, follow_redirects=False)





