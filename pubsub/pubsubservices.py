from random import randint
from models.market import Crypto
from .cryptobrokermodel import Crypto_Broker
# from db_access import db_action
from time import time

crypto_brokers = {}
crypto_list = []

def subscribe_to_socket_for_real_time_crypto(name,interval): 
    crypto_broker = crypto_brokers[name][interval]
    return(crypto_broker.subscribe())

def publish_to_socket_for_real_time_crypto(name,interval,raw_data,candleclosed): 
    crypto_broker=crypto_brokers[name][interval]
    
    crypto_broker.publish(name,interval,raw_data,candleclosed)

def get_history_for_crypto(cryptoname,interval):
    return(crypto_brokers[cryptoname][interval].get_historical_data(cryptoname,interval))

def start_publisher_subscriber_model():  #Initialize the model for each crypto interval
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({'type':'crypto'})
    # symbl_set = db_action("read_one",[{"type":"crypto"},"symbols"],"admin")
    print('crypto_list:---------',fetched_crypto_list_from_market)
    for crypto in fetched_crypto_list_from_market['list']:

        if (crypto not in crypto_list):
            print(crypto)
            crypto_list.append(crypto)

    for crypto in crypto_list:
        crypto_broker_list= {
            "1d":Crypto_Broker(),
            "1h":Crypto_Broker(),
            "30m":Crypto_Broker(),
            "15m":Crypto_Broker(),
            "1m":Crypto_Broker(),
            "5m":Crypto_Broker()
        }

        crypto_brokers[crypto] =crypto_broker_list
  




        
    