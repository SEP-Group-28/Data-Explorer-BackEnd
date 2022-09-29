
from datetime import datetime
import json
import queue
from random import randint
from models.market import Crypto


class Crypto_Broker:

    def __init__(self):
        self.listeners = []
        self.db_push_queue =[]
        self.id=randint(1,10000)

    def subscribe(self):
        q = queue.Queue(maxsize=1000)
        print('q is added',q)
        self.listeners.append(q)
        return q

    def publish(self,cryptoname,interval, msg,candle_closed):
      
        send_msg = [msg['time'].iloc[-1],msg['open'].iloc[-1],msg['high'].iloc[-1],msg['low'].iloc[-1],msg['close'].iloc[-1],msg['volume'].iloc[-1]]
     
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
        for i in reversed(range(len(self.listeners))):
            
            try:
                self.listeners[i].put_nowait(format_sse(json.dumps(send_msg)))
            except queue.Full:
                del self.listeners[i]



        if len(self.db_push_queue)<=10:  
            if(candle_closed==True): #add trade data in relevant interval
                self.db_push_queue.append(send_msg)
    
        else: ##limit database call by using a queue
      
            crypto_data_list=Crypto.getCryptoDataList(interval,cryptoname)
       
            new_data = crypto_data_list['data']
        
            for dec_set in self.db_push_queue:
                if (crypto_data_list['data'][-1][0]<dec_set[0]):
                    new_data.append(dec_set)
            Crypto.removeCryptoDataList(interval,cryptoname)

            Crypto.insertCryptoDataList(interval,cryptoname,new_data)

            self.db_push_queue = []
    
    def get_historical_data(self,cryptoname,interval):

        history_details= Crypto.getCryptoDataList(interval,cryptoname)
    
        history_data = history_details['data']

        for trade_data in self.db_push_queue:
            last_history_data_time=history_data[-1][0]
            trade_data_time=trade_data[0]
            if (last_history_data_time<trade_data_time):  ##Additional protection to certify data 
                history_data.append(trade_data)   
        return(history_data)

def format_sse(data: str, event=None) -> str:  ##Format dataset message in to exchangeble message
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg