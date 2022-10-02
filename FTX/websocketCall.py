from models.market import Crypto
from .websocketServices import FtxClientWs
from threading import Thread

crypto_list= []

def start_streaming():

    client =FtxClientWs()
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({"type":"crypto"})
    for crypto in  fetched_crypto_list_from_market['list']:
        if (crypto not in crypto_list):
            crypto_list.append(crypto)
    

    for crypto in crypto_list:
    # crypto='SOL/USDT'
        client._subscribe({'channel': 'trades', 'market': crypto})
        trades=client._trades[crypto]
        # print('trades',id(trades))
        start_listen_for_each_crypto_interval(client,crypto,trades)
        print('starteed')

def start_listen_for_each_crypto_interval(client, crypto,trades):

    fifteen_sec_interval_socket = Thread(target=client.start_interval_socket, args=(crypto,'15s',trades))
    one_min_interval_socket = Thread(target=client.start_interval_socket, args=(crypto,'1m',trades))
    fifteen_min_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'15m',trades))
    thirty_min_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'30m',trades))
    one_hour_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'1h',trades))
    one_day_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'1d',trades))

    fifteen_sec_interval_socket.start()
    one_min_interval_socket.start()
    fifteen_min_interval_socket.start()
    thirty_min_interval_socket.start()
    one_hour_interval_socket.start()
    one_day_interval_socket.start()

    