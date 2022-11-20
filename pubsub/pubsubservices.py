from models.notification import Notification
from models.market import Crypto
from .cryptobrokermodel import Crypto_Broker
from time import time

#ARRAY STORES
crypto_brokers = {}
crypto_list = []
notifications = []

#SUBCRIBING SERVICE TO RELAVANT CRYPTO MARKET
def subscribe_to_socket_for_real_time_crypto(name,interval): 
    crypto_broker = crypto_brokers[name][interval]
    return(crypto_broker.subscribe())

#PUBLISHING SERVICE TO RELAVANT CYRPTO MARKET USING INTERVALS
def publish_to_socket_for_real_time_crypto(name,interval,raw_data): 

    change= name.split('USDT')
    name=change[0]+'/USDT'
    crypto_broker=crypto_brokers[name][interval]
    
    crypto_broker.publish(name,interval,raw_data)

#TAKE HISTORY FOR CRYPTO
def get_history_for_crypto(cryptoname,interval):
    return(crypto_brokers[cryptoname][interval].get_historical_data(cryptoname,interval))

#TAKE HISTORY FOR CRYPTO USING TIMESTAMP
def get_history_for_crypto_timestamp(cryptoname,interval,timestamp,datalimit):
    return(crypto_brokers[cryptoname][interval].get_historical_data_timestamp(cryptoname,interval,timestamp,datalimit))

#TAKE HISTORY FOR CRYPTO USING TIMESTAMP WITH INDICATORS
def get_history_for_crypto_timestamp_for_indicators(cryptoname,interval,timestamp,datalimit,indicator):
    return(crypto_brokers[cryptoname][interval].get_historical_data_timestamp_for_indicator(cryptoname,interval,timestamp,datalimit,indicator))

#INITIALIZE THE MODEL FOR EACH CRYPTO INTERVAL
def start_publisher_subscriber_model(): 
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({'type':'crypto'})
    for crypto in fetched_crypto_list_from_market['list']:

        if (crypto not in crypto_list):
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

#PUBLISHING SERVICE FOR NOTIFICATIONS
def publish_to_socket_for_real_time_notifications(data,user_id):
    notifications.append([data['symbol'],data,user_id])

 #SENDING NOTIFICATION THREAD  
def start_sending_notifications():
    while(True):
        if(len(notifications)>0):
            data={"time":int(time()*1000),"data":notifications[0][1]}
            Notification.insertnotifications(data,notifications[0][2])
            notifications.pop(0)

#TAKE HISTORICAL NOTIFICATIONS FOR A ONE DAY
def historical_nots(id):
    time_filter = int(time()*1000 - (1*24*60*60*1000))
    try:
        query=[{'_id':id},{'alertlist.$.0':{"gte":time_filter}}]
        data=Notification.gethistoricnotifications(query)
        opt = []
        for dt in data:
            opt.append([dt[0],dt[1],dt[2]])

        for dt in notifications:
            opt.append([int(time()*1000),dt[1],dt[2]])
    except Exception as e:
        return ({"last day notifications": []})

    return({"last day notifications":opt})







        
    