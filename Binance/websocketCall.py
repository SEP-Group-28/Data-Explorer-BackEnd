from models.market import Crypto
# from .websocketServices import FtxClientWs
# from threading import Thread
from pubsub.pubsubservices import publish_to_socket_for_real_time_crypto
from binance import ThreadedWebsocketManager
from binance.enums import KLINE_INTERVAL_15MINUTE, KLINE_INTERVAL_1DAY, KLINE_INTERVAL_1HOUR, KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_30MINUTE,KLINE_INTERVAL_5MINUTE
from binance.exceptions import BinanceAPIException
import socket
import time

crypto_list= []
api_key = 'E4qXXp67zhZevj0Um2AQ83OPvDEjysaRVdfHRPvNXR2EXWjIW9dyjZPY4ep574CC'
api_secret = 'pYiSC30hGJqqOBFlmNcaLgojSx5scRf2xEBCp3feuc9CIq7T1wKpCQwdI7H5EUaW'



def start_streaming():

    # client =FtxClientWs()
   
    
    print(api_key)
    print(api_secret)
    # if (checkInternetSocket()):

    twm = ThreadedWebsocketManager(api_key='E4qXXp67zhZevj0Um2AQ83OPvDEjysaRVdfHRPvNXR2EXWjIW9dyjZPY4ep574CC', api_secret='pYiSC30hGJqqOBFlmNcaLgojSx5scRf2xEBCp3feuc9CIq7T1wKpCQwdI7H5EUaW')

    twm.start()

    print("Publisher started working !!!")

    # for smbl in symbols:
    #     start_to_listen(twm,smbl)
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({"type":"crypto"})
    for crypto in  fetched_crypto_list_from_market['list']:
        if (crypto not in crypto_list):
            crypto_list.append((crypto.split('/USDT')[0])+'USDT')

    # print(crypto_list)
    for crypto in crypto_list:
    # crypto='SOL/USDT'
        # client._subscribe({'channel': 'trades', 'market': crypto})
        # trades=client._trades[crypto]
        # print('trades',id(trades))
        start_listen_for_each_crypto_interval(twm,crypto)
        # print('starteed')


def start_listen_for_each_crypto_interval(twm, crypto):

   
    # one_min_interval_socket = Thread(target=client.start_interval_socket, args=(crypto,'1m',trades))
    # five_min_interval_socket = Thread(target=client.start_interval_socket, args=(crypto,'5m',trades))
    # # fifteen_min_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'15m',trades))
    # thirty_min_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'30m',trades))
    # one_hour_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'1h',trades))
    # one_day_interval_socket=Thread(target=client.start_interval_socket, args=(crypto,'1d',trades))

    
    # one_min_interval_socket.start()
    # five_min_interval_socket.start()
    # # fifteen_min_interval_socket.start()
    # thirty_min_interval_socket.start()
    # one_hour_interval_socket.start()
    # one_day_interval_socket.start()

    def handle_socket_message(msg):
        publish_to_socket_for_real_time_crypto(msg['s'], msg['k']['i'], msg)
        # announce_socket(msg['s'], msg['k']['i'], msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_5MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_15MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_30MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1HOUR)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1DAY)

    # twm.join()
def checkInternetSocket(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return (True)
    except socket.error as ex:
        return (False)

def restart_binance_connection():

    while (True):

        reboot = False

        while (not checkInternetSocket()):
            if (not reboot):
                reboot = True
                print("Connection broken recconecting...")
            time.sleep(5)

        if (reboot):
            print("Connection rebooted")
            start_streaming()

