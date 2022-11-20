from models.market import Crypto
from pubsub.pubsubservices import publish_to_socket_for_real_time_crypto
from binance import ThreadedWebsocketManager
from binance.enums import KLINE_INTERVAL_15MINUTE, KLINE_INTERVAL_1DAY, KLINE_INTERVAL_1HOUR, KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_30MINUTE,KLINE_INTERVAL_5MINUTE
import socket
import time

#list to use for append each crypto market
crypto_list= []

#Function to continue streaming after connecting to binance websocket
def start_streaming():

    #Connect to binance websocket 
    twm = ThreadedWebsocketManager(api_key='E4qXXp67zhZevj0Um2AQ83OPvDEjysaRVdfHRPvNXR2EXWjIW9dyjZPY4ep574CC', api_secret='pYiSC30hGJqqOBFlmNcaLgojSx5scRf2xEBCp3feuc9CIq7T1wKpCQwdI7H5EUaW')

    twm.start()
    print("Connected to binance websocket")
    #Take all crypto markets from database 
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({"type":"crypto"})
    for crypto in  fetched_crypto_list_from_market['list']:
        if (crypto not in crypto_list):
            crypto_list.append((crypto.split('/USDT')[0])+'USDT')

    #Start streaming to get data for each crypto interval 
    for crypto in crypto_list:
        start_listen_for_each_crypto_interval(twm,crypto)


#Function to start streaming for each crypto interval
def start_listen_for_each_crypto_interval(twm, crypto): 
    def handle_socket_message(msg): #Call back function when trigger upon a message come from binance websocket
        publish_to_socket_for_real_time_crypto(msg['s'], msg['k']['i'], msg) #Call the method inside the Broker to publish the data to frontend

    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1MINUTE) #Listen to each interval
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_5MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_15MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_30MINUTE)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1HOUR)
    twm.start_kline_socket(callback=handle_socket_message, symbol=crypto, interval=KLINE_INTERVAL_1DAY)

def checkInternetSocket(host="8.8.8.8", port=53, timeout=3):  #check internet socket is working or not
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return (True)
    except socket.error as ex:
        return (False)

def restart_binance_connection(): #Restart binance connection if the connection get lost

    while (True):

        restart = False

        while (not checkInternetSocket()):
            if (not restart):
                restart = True
                print("Connection broken reconnecting...")
            time.sleep(5)

        if (restart):
            print("Connection restarted")
            start_streaming()

