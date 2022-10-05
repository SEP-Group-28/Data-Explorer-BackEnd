
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
        FIFO_listners=range(len(self.listeners))
        for i in reversed(FIFO_listners):
            
            try:
                self.listeners[i].put_nowait(convert_to_sse_format(json.dumps(send_msg)))
            except queue.Full:
                del self.listeners[i]

        if len(self.db_push_queue)<=5:  
            if(candle_closed==True): #add trade data in relevant interval
                self.db_push_queue.append(send_msg)
    
        else: ##limit database call by using a queue
      
            crypto_data_list=Crypto.getCryptoDataList(interval,cryptoname)
            print('printing crypto data list',cryptoname, interval, crypto_data_list)
            history_data = crypto_data_list['data']
        
            for dec_set in self.db_push_queue:
                # print('history data length',len(history_data[-1]))
                if(len(history_data)==0):
                    history_data.append(dec_set)
                elif (history_data[-1][0]<dec_set[0]):
                    history_data.append(dec_set)
            Crypto.updateCryptoDataList(interval,cryptoname,history_data)
            # Crypto.removeCryptoDataList(interval,cryptoname)
            # print('')
            # Crypto.insertCryptoDataList(interval,cryptoname,history_data)
            self.db_push_queue = []
    
    def get_historical_data(self,cryptoname,interval):

        history_details= Crypto.getCryptoDataList(interval,cryptoname)
    
        history_data = history_details['data']

        for trade_data in self.db_push_queue:
            last_history_data_time=history_data[-1][0]
            trade_data_time=trade_data[0]
            if (last_history_data_time<trade_data_time):  ##Additional protection to certify data 
                history_data.append(trade_data)   
        # print('history data requesting',history_data)
        return(history_data)

def convert_to_sse_format(data: str, event=None) -> str:  ##Format dataset message in to exchangeble message as a server sent event
    msg = f'data: {data}\n\n'
    if event is not None: #meaning this is a message event
        msg = f'event: {event}\n{msg}'
    return msg