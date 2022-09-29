from random import randint
from models.market import Crypto
from .cryptobrokermodel import Crypto_Broker
# from db_access import db_action
from time import time

crypto_brokers = {}
crypto_list = []

def publish_to_socket(name,interval,raw_data,candleclosed): 
    crypto_broker=crypto_brokers[name][interval]
    
    crypto_broker.publish(name,interval,raw_data,candleclosed)

def subscribe_to_socket(name,interval): 
    crypto_broker = crypto_brokers[name][interval]
    return(crypto_broker.subscribe())

def get_history(symbl,interval):
    return(crypto_brokers[symbl][interval].get_historical_data(symbl,interval))

def start_pub_sub_model():
    fetched_crypto_data_list=Crypto.getCryptoList({'type':'crypto'})
    # symbl_set = db_action("read_one",[{"type":"crypto"},"symbols"],"admin")
    print('crypto_list:---------',crypto_list)
    for crypto in fetched_crypto_data_list:

        if (crypto not in crypto_list):
            print(crypto)
            crypto_list.append(crypto['name'])

    for crypto in crypto_list:
        crypto_broker_list= {"1d":Crypto_Broker(),"1h":Crypto_Broker(),"30m":Crypto_Broker(),"15m":Crypto_Broker(),"1m":Crypto_Broker(),"15s":Crypto_Broker()}

        crypto_brokers[crypto] =crypto_broker_list
        # for i in crypto_broker_list:
        #     print(crypto,i,randint(1,1000))
        

#print("PubSub Initiated",symbols)



        
    