from random import randint

from models.notification import Notification
from models.market import Crypto
from .cryptobrokermodel import Crypto_Broker,NotificationAnnouncer
# from db_access import db_action
from time import time

crypto_brokers = {}
crypto_list = []
notifications = []
# alertsdict={}
notification_brokers={}
# notification_announcer = NotificationAnnouncer()

def subscribe_to_socket_for_real_time_crypto(name,interval): 
    crypto_broker = crypto_brokers[name][interval]
    return(crypto_broker.subscribe())

def publish_to_socket_for_real_time_crypto(name,interval,raw_data,candleclosed): 
    crypto_broker=crypto_brokers[name][interval]
    
    crypto_broker.publish(name,interval,raw_data,candleclosed)

def get_history_for_crypto(cryptoname,interval):
    return(crypto_brokers[cryptoname][interval].get_historical_data(cryptoname,interval))

def get_history_for_crypto_timestamp(cryptoname,interval,timestamp):
    return(crypto_brokers[cryptoname][interval].get_historical_data_timestamp(cryptoname,interval,timestamp))

def start_publisher_subscriber_model():  #Initialize the model for each crypto interval
    fetched_crypto_list_from_market=Crypto.getCryptoListFromMarket({'type':'crypto'})
    # symbl_set = db_action("read_one",[{"type":"crypto"},"symbols"],"admin")
    # print('crypto_list:---------',fetched_crypto_list_from_market)
    for crypto in fetched_crypto_list_from_market['list']:

        if (crypto not in crypto_list):
            # print(crypto)
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
        notification_brokers[crypto]={'1m':NotificationAnnouncer()}

# btc:[[],[],[],[],[]],sol:[[]]/\
        crypto_brokers[crypto] =crypto_broker_list
# <crypto>/<crypto_price>/<token>
# def add_firebase_alert(crypto_name,crypto_price,user_id):
#     if crypto_price not in alertsdict:
#         alertsdict[crypto_price]=[[crypto_name+'/USDT',user_id]]
#     elif type(alertsdict[crypto_price]==list):
#         alertsdict[crypto_price].append([crypto_name+'/USDT',user_id])

#     return alertsdict
  

def subscribe_to_socket_for_real_time_notifications(crypto_name):
    return(notification_brokers[crypto_name].listen_nots())

def publish_to_socket_for_real_time_notifications(data):
    notifications.append([data['symbol'],data])
   
def look_for_nots():
    while(True):
        if(len(notifications)>0):
            crypto_name=notifications[0][0]
            notification_brokers[crypto_name].announce_nots(notifications[0][1])
            data={"time":int(time()*1000),"data":notifications[0][1]}
            print("pubsub data", data)
            result=Notification.insertnotifications(data)
            print("notification result", result)
            # db_action("insert_one",[{"time":int(time()*1000),"data":notifications[0]},"notifications"],"admin")
            notifications.pop(0)


def historical_nots():
    time_filter = int(time()*1000 - (5*24*60*60*1000))
    timeDetails={"time": {"$gte":time_filter}}
    data=Notification.gethistoricnotifications(timeDetails)
    print("line 70, ..", data)
    # data = db_action("read_many",[{"time": {"$gte":time_filter}},"notifications"],"admin")
    opt = []
    for dt in data:
        opt.append([dt['time'],dt['data']])

    for dt in notifications:
        opt.append([int(time()*1000),dt])

    return({"last 5 days notifications":opt})





        
    