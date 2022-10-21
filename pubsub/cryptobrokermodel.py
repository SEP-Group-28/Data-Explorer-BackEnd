from pubsubservices import add_notification
from datetime import datetime
import json
import queue
from random import randint
from models.market import Crypto

# from pubsubservices import add_notification


class Crypto_Broker:

    def __init__(self):
        self.subscribers = []
        self.push_queue =[]
        # self.id=randint(1,10000)

    def subscribe(self):
        q = queue.Queue(maxsize=10)
        print('q is added',q)
        self.subscribers.append(q)
        return q

    def publish(self,cryptoname,interval, msg,candle_closed):
      
        send_msg = [
            msg['time'].iloc[-1],
            msg['open'].iloc[-1],
            msg['high'].iloc[-1],
            msg['low'].iloc[-1],
            msg['close'].iloc[-1],
            msg['volume'].iloc[-1]
            ]
     
        # print('annnounced',msg,interval)
        # json_msg={
        #    'time': msg['time'].iloc[-1],
        #     'open':msg['open'].iloc[-1],
        #     'high':msg['high'].iloc[-1],
        #     'low':msg['low'].iloc[-1],
        #     'close':msg['close'].iloc[-1],
        #     'volume':msg['volume'].iloc[-1],
        #     'state':state
        # }
        
        # print('length',len(self.listeners),self.id)
        FIFO_subscribers=range(len(self.subscribers))
        for i in reversed(FIFO_subscribers):
            
            try:
                self.subscribers[i].put_nowait(convert_to_sse_format(json.dumps(send_msg)))
            except queue.Full:
                del self.listeners[i]

        if (interval=="1m" and candle_closed==True):

            # data = db_action("read_one",[{"type":"data_1d"},sy],"admin")
            crypto_data_list_details=Crypto.getCryptoDataList('1d',cryptoname)
            crypto_data=crypto_data_list_details['data']
            if len(crypto_data)!=0:
                peak_price = float(crypto_data[-1][1])
                open_price= msg['open'].iloc[-1]
                percent_price = ((float(open_price) - peak_price)/peak_price)*100

                if (percent_price>75):
                    add_notification({"message":"successful","type":"Over 75 percent increment","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price>50):
                    add_notification({"message":"successful","type":"Over 50 percent increment","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price>25):
                    add_notification({"message":"successful","type":"Over 25 percent increment","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price>5):
                    add_notification({"message":"successful","type":"Over 5 percent increment","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price<(-25)):
                    add_notification({"message":"successful","type":"Over 25 percent decrement","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price<(-50)):
                    add_notification({"message":"successful","type":"Over 50 percent decrement","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})
                elif(percent_price<(-75)):
                    add_notification({"message":"successful","type":"Over 75 percent decrement","symbol":cryptoname,"open price":open_price,"current peak price":peak_price})

        if len(self.push_queue)<=5:  
            if(candle_closed==True): #add trade data in relevant interval
                self.push_queue.append(send_msg)
    
        else: ##limit database call by using a queue
      
            crypto_data_list=Crypto.getCryptoDataList(interval,cryptoname)
            # print('printing crypto data list',cryptoname, interval, crypto_data_list)
            history_data = crypto_data_list['data']
        #[""]
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
            # Crypto.removeCryptoDataList(interval,cryptoname)
            # print('')
            # Crypto.insertCryptoDataList(interval,cryptoname,history_data)
            self.push_queue = []
    
    def get_historical_data(self,cryptoname,interval):

        history_details= Crypto.getCryptoDataList(interval,cryptoname)
    
        history_data = history_details['data']

        for trade_data in self.push_queue:
            last_history_data_time=history_data[-1][0]
            trade_data_time=trade_data[0]
            if (last_history_data_time<trade_data_time):  ##Additional protection to certify data 
                history_data.append(trade_data)   
        # print('history data requesting',history_data)
        return(history_data)

    
class NotificationAnnouncer:

    def __init__(self):
        self.listener_set = []

    def listen_nots(self):
        qu = queue.Queue(maxsize=100)
        self.listener_set.append(qu)
        return (qu)

    def announce_nots(self, msg):

        msg = convert_to_sse_format(data=msg)

        for i in reversed(range(len(self.listener_set))):
            try:
                self.listener_set[i].put_nowait(msg)
            except queue.Full:
                del self.listener_set[i]

def convert_to_sse_format(data: str, event=None) -> str:  ##Format dataset message in to exchangeble message as a server sent event
    msg = f'data: {data}\n\n'
    if event is not None: #meaning this is a message event
        msg = f'event: {event}\n{msg}'
    return msg


