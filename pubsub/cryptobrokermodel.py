import json
import queue
from models.market import Crypto
from .import pubsubservices
from firebase.confirebase import confirebase
from models.alert import Alert

#CRYPTO BROKER INSTANCE
class Crypto_Broker:
    def __init__(self):
        self.subscribers = []
        self.push_queue =[]
        self.previous_price = -1

    def subscribe(self):
        q = queue.Queue(maxsize=1000)
        self.subscribers.append(q)
        return q

    def publish(self,cryptoname,interval, msg):

 #SET THE DATA TO APPROPRIATE FORMAT
        time=(float(msg['k']['t'])/1000)
        open_price=float( msg['k']['o'])
        high_price=float(msg['k']['h'])
        low_price=float(msg['k']['l'])
        close_price=float(msg['k']['c'])
        volume=float(msg['k']['v'])
        candle_closed=msg['k']['x']
        price= float(msg['k']['c'])

        send_msg= [time,  
                    open_price,
                    high_price,
                    low_price,
                    close_price,
                    volume
                    ]

##SENDING ALERTS

        def sending_notifications(i):  
            confirebase(cryptoname,i[0],i[1])
            pubsubservices.publish_to_socket_for_real_time_notifications(
                {"message":"successful","type":"Crossing","price":i[0],"symbol":cryptoname},i[1])

        if interval=='1m':
            alertsdict=Alert().take_previous_alerts_for_price(cryptoname)['alertlist']

            if not (alertsdict is None):
                current_price=price
                previous_price = self.previous_price
                if(cryptoname == "BTC/USDT"):
                    pass

                if previous_price>=0:
                    newalertsdict=[i
                    for i in alertsdict 
                    if (   
                        (((previous_price<=i[0]<=current_price) or (previous_price>=i[0]>=current_price)) and interval=='1m') 
                        and 
                        sending_notifications(i) 
                        and False) 
                        or
                        (((previous_price>i[0] or i[0]>current_price) and (previous_price<i[0] or i[0]<current_price)) or interval!='1m')
                    ]
                    Alert().update_alerts_for_price(cryptoname,newalertsdict)

                self.previous_price=price
    
#PUBLISH THE DATA 
        FIFO_subscribers=range(len(self.subscribers))
        for i in reversed(FIFO_subscribers):
            
            try:
                self.subscribers[i].put_nowait(convert_to_sse_format(json.dumps(send_msg)))
            except queue.Full:
                del self.subscribers[i]

#DATABASE FEED
        if len(self.push_queue)<=5:  
            if(candle_closed==True): #add trade data in relevant interval
                self.push_queue.append(send_msg)
    
        else: ##limit database call by using a queue
      
            crypto_data_list=Crypto.getCryptoDataList(interval,cryptoname)
            # print('printing crypto data list',cryptoname, interval, crypto_data_list)
            history_data = crypto_data_list['data']
            for dec_set in self.push_queue:
                # print('history data length',len(history_data[-1]))
                if(len(history_data)==0):
                    history_data.append(dec_set)
                if(len(history_data[0])==0 or history_data[0]==""):
                    history_data.pop()
                    history_data.append(dec_set)
                elif (history_data[-1][0]<dec_set[0]):
                    history_data.append(dec_set)
            Crypto.updateCryptoDataList(interval,cryptoname,history_data)

            self.push_queue = []
    

#GET HISTORICAL DATA
    def get_historical_data(self,cryptoname,interval):
        history_details= Crypto.getCryptoDataList(interval,cryptoname)
    
        history_data = history_details['data']
        
        for trade_data in self.push_queue:
            last_history_data_time=history_data[-1][0]
            trade_data_time=trade_data[0]
            if (last_history_data_time<trade_data_time):  ##Additional protection to certify data 
                history_data.append(trade_data)   
        return(history_data)


#GET HISTORICAL DATA USING TIMESTAMP
    def get_historical_data_timestamp(self,cryptoname,interval,timestamp,datalimit):
        history_data= Crypto.getCryptoDataListForTimeStamp(interval,cryptoname,timestamp,datalimit)
    
        if (int(timestamp) == 0):
            for trade_data in self.push_queue:
                last_history_data_time=history_data[-1][0]
                trade_data_time=trade_data[0]
                if (last_history_data_time<trade_data_time):
                    history_data.append(trade_data)
    
        return(history_data)
    
#GET HISTORICAL DATA USING TIMESTAMP FOR INDICATORS
    def get_historical_data_timestamp_for_indicator(self,cryptoname,interval,timestamp,datalimit,indicator):

        history_data= Crypto.getCryptoDataListForTimeStampForIndicator(interval,cryptoname,timestamp,datalimit,indicator)
    
        if (int(timestamp) == 0):
            for trade_data in self.push_queue:
                last_history_data_time=history_data[-1][0]
                trade_data_time=trade_data[0]
                if (last_history_data_time<trade_data_time):
                    history_data.append(trade_data)
        return(history_data)

#CONVERT THE DATA TO SSE FORMAT
def convert_to_sse_format(data: str, event=None) -> str:  ##Format dataset message in to exchangeble message as a server sent event
    msg = f'data: {data}\n\n'
    if event is not None: #meaning this is a message event
        msg = f'event: {event}\n{msg}'
    return msg


