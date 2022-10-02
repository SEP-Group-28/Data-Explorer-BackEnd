import hmac, json, time, zlib
import threading
from collections  import defaultdict, deque
from itertools    import zip_longest
from typing       import DefaultDict, Deque, List, Dict, Tuple, Optional
from gevent.event import Event
from threading    import Thread, Lock,enumerate
import websocket
import datetime
from pubsub.pubsubservices import publish_to_socket
import time
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class WebsocketManager:
    _CONNECT_TIMEOUT_S = 5

    def __init__(self):
        self.connect_lock = Lock()
        self.ws = None

    def _get_url(self):
        raise NotImplementedError()

    def _on_message(self,ws, message):
        raise NotImplementedError()

    def send(self, message):
        self.connect()
        self.ws.send(message)

    def send_json(self, message):
        self.send(json.dumps(message))

    def _on_open(self,ws):
        raise NotImplementedError()

    def _connect(self):
        assert not self.ws, "ws should be closed before attempting to connect"
        self.ws = websocket.WebSocketApp(
             self._get_url(),
            on_open=self._wrap_callback(self._on_open),
            on_message=self._wrap_callback(self._on_message),
            on_close=self._wrap_callback(self._on_close),
            on_error=self._wrap_callback(self._on_error),
        )

        wst = Thread(target=self._run_websocket, args=(self.ws,))
        wst.daemon = True
        wst.start()
    
        ts = time.time()
        while self.ws and (not self.ws.sock or not self.ws.sock.connected):
            if time.time() - ts > self._CONNECT_TIMEOUT_S:
                self.ws = None
                return
            time.sleep(1)

    def _wrap_callback(self, f):
        def wrapped_f(ws, *args, **kwargs):
            if ws is self.ws:
                try:
                    f(ws, *args, **kwargs)
                except Exception as e:
                    raise Exception(f'Error running websocket callback: {e}')
        return wrapped_f

    def _run_websocket(self, ws):
        try:    
            ws.run_forever()
        except Exception as e:
            raise Exception(f'Unexpected error while running websocket: {e}')
        finally:
            self._reconnect(ws)

    def _reconnect(self, ws):
        assert ws is not None, '_reconnect should only be called with an existing ws'
        if ws is self.ws:
            self.ws = None
            ws.close()
            self.connect()

    def connect(self):
        if self.ws:
            return
        with self.connect_lock:
            while not self.ws:
                self._connect()
                if self.ws:
                    return

    def _on_close(self,ws,close_msg):
        self._reconnect(ws)

    def _on_error(self, ws, error):
        self._reconnect(ws)

    def reconnect(self) -> None:
        if self.ws is not None:
            self._reconnect(self.ws)
Datadict={}
Flagdict={}
class FtxClientWs(WebsocketManager):
    _ENDPOINT = 'wss://ftx.com/ws/'

    def __init__(self, subaccount_name=None) -> None:
        super().__init__()
        self._trades: DefaultDict[str, Deque] = defaultdict(lambda: deque([], maxlen=100))
        self._api_key ='ldACQ0gfDgKg5_eQoQYDwjUafNL1V4B8W77qD_p9'
        self._api_secret ='qMNgwI4gc3QwPnUs3ESFarb54NJKL4O5h7RBg51B'
        self._reset_data()
        self._flags = {'get_trades' : {'aggregate': False}}

    def _on_open(self,ws):
        self._reset_data()

    def _reset_data(self) -> None:
        self._subscriptions: List[Dict] = []
        self._tickers: DefaultDict[str, Dict] = defaultdict(dict)

    def _get_url(self) -> str:
        return self._ENDPOINT

    def _subscribe(self, subscription: Dict) -> None:
        self.send_json({'op': 'subscribe', **subscription})
        self._subscriptions.append(subscription)

    def _unsubscribe(self, subscription: Dict) -> None:
        self.send_json({'op': 'unsubscribe', **subscription})
        while subscription in self._subscriptions:
            self._subscriptions.remove(subscription)

    def get_trades(self, market: str, aggregate: bool = True) -> List[Dict]:
        self._flags['get_trades']['aggregate'] = aggregate
        subscription = {'channel': 'trades', 'market': market}
     
        if subscription not in self._subscriptions:
            self._subscribe(subscription)
        return list(self._trades[market].copy())


    def get_ticker(self, market: str) -> Dict:
        subscription = {'channel': 'ticker', 'market': market}
        if subscription not in self._subscriptions:
            self._subscribe(subscription)
        return self._tickers[market]

    def _handle_trades_message(self, message: Dict) -> None:
        if (self._flags['get_trades']['aggregate']):

            self._trades[message['market']].append(message['data'])
            # print('appendif',len(self._trades[message['market']]),self._trades[message['market']])
        else:
         
            self._trades[message['market']].extend(reversed(message['data']))
            # print('appendelse',len(self._trades[message['market']]),self._trades[message['market']])
        
    def _handle_ticker_message(self, message: Dict) -> None:
        self._tickers[message['market']] = message['data']


    def _on_message(self,ws, raw_message) -> None:
        # print(raw_message)
        message = json.loads(raw_message)
        message_type = message['type']
        if message_type in {'subscribed', 'unsubscribed'}:
            return
        elif message_type == 'info':
            if message['code'] == 20001:
                return self.reconnect()
        elif message_type == 'error':
            raise Exception(message)
        channel = message['channel']

        if channel == 'trades':
            # print('ooooooo')
            self._handle_trades_message(message)
        if channel == 'ticker':
            self._handle_ticker_message(message)
    
    ##Convert ticker data to OHLC data





    def start_interval_socket(self,crypto,interval,trades):
        def process_tick(trades1):
            data=Datadict[crypto][interval]
            tick=trades1[-1]
            
            # global flag
            flag=Flagdict[crypto][interval]
            # global frontier
            # print(flag)
            # print('kkkkkkkk')
            # print('sss')
            # print('crypto',crypto,interval,end='\r')
            if (flag==True):
                trades1.clear()
                trades1.append(tick)
                print('aaawa')
                start_time = datetime.utcnow().isoformat() #"almost"
                # time_      = time.time() #* 1000  with higher precision
                op         = tick['price']
                hi         = tick['price']
                lo         = tick['price']
                cl         = tick['price']
                vol        = tick['size' ]
                row        = {
                            'time'      :time.time(), 
                            'open'      : op        , 
                            'high'      : hi        , 
                            'low'       : lo        , 
                            'close'     : cl        ,
                            'volume'    : vol        }
                if crypto not in Datadict:
                    Datadict[crypto]={}
                Datadict[crypto][interval]=data=pd.concat([data,pd.DataFrame.from_records([row])])
                # print('id init 2',threading.current_thread().ident,id(data))
                if crypto not in Flagdict:
                    Flagdict[crypto]={}
                flag = False
                Flagdict[crypto][interval]=flag
            else:
                # print('False')
                # print('id put data',threading.current_thread().ident,id(data))
                # print(data['high'].iloc)
                if   (tick['price'] > data['high'].iloc[-1]):
                    data['high'].iloc[-1] = tick['price']
                elif (tick['price'] < data['low' ].iloc[-1]):
                    data['low' ].iloc[-1] = tick['price']

                data['close' ].iloc[-1]  = tick['price']
                data['volume'].iloc[-1] += tick['size' ]
                # print(tick)
            
        def on_tick():
            # print('startinggggg')
            # client._subscribe({'channel': 'ticker', 'market': crypto})
            while True:

                try:

                    try:
                        # print(trades[-1])
                        # print('trades',trades)
                        # print(trades[-1])
                        process_tick(trades)
                        # print('trades[-1]  ',trades[-1])
                        # print('trade',trades)
                        # trades.pop()
                    except IndexError:
                        pass

                    time.sleep(0.001)
                except KeyboardInterrupt:
                    # client_ws._reset_data()
                    scheduler.remove_job('onClose')
                    scheduler.shutdown()
#print('Shutdown')
                    break
            
        def candle_close(interval,crypto,RES):
            print("candle close")
            # global flag
            # global frontier
            if crypto not in Flagdict:
                Flagdict[crypto]={}
            flag     = True
            Flagdict[crypto][interval]=flag
            # print(flag,crypto,interval)
            # frontier = pd.Timestamp.utcnow().floor(RES).isoformat()
            # # print('onclose :-',data)
            # print('empty',data.empty) 
            # print('RESOLI+UTION............',RES)
            # data['time'].iloc[-1]=time.time()
            data=Datadict[crypto][interval]
            # data['time'].iloc[-1]=time.time()   
            if not(data.empty):
                # print('queue value 2',[crypto,interval,data])
                publish_to_socket(crypto,interval,data,True)
#print('Closed')
            # print(frontier)
            # print('close0',threading.enumerate())
            
            # print(threading.current_thread())
        def on_calc_candle(interval,crypto,RES):
            # global flag
            # global frontier
            # flag     = False
            # Flagdict[crypto]=flag
            # print('RESOLI+UTION............',RES)
            # frontier = pd.Timestamp.utcnow().floor(RES).isoformat()
         
            # # print('onclose :-',data)
            # print('empty',data.empty)
                  
            data=Datadict[crypto][interval]
            # data['time'].iloc[-1]=time.time()   
            if not(data.empty):

                # print('queue value 1',[crypto,interval,data])
                publish_to_socket(crypto,interval,data,False)
            # print(frontier)
            # print('close0',threading.enumerate())
            
            # print(threading.current_thread())

        ASSET = crypto
        RES   = interval
        # print(interval)
       

        # global flag   
        if crypto not in Flagdict:
            Flagdict[crypto]={}
        flag= True
        Flagdict[crypto][interval]=flag
        # global frontier
        # if(interval[-1]=='m'):
        #     RES=interval[:-1]+'T'
        # elif(interval[-1]=='d')
        # frontier  = pd.Timestamp.utcnow().floor(RES
        # ).isoformat() 
        cols      = [ 'time', 'open', 'high', 'low', 'close', 'volume']
        
        data      = pd.DataFrame(columns=cols)
        if crypto not in Datadict:
            Datadict[crypto]={}
        Datadict[crypto][interval]=data
        # print('id init',threading.current_thread().ident,id(data))
        # trades   = trades

        scheduler = BackgroundScheduler()

        scheduler.configure(timezone='utc')
#print(interval)
        interval=interval
        scheduler.add_job(on_calc_candle, trigger='cron', second='*/1',args=[interval,ASSET,RES])
        if(interval=='15s'):
            scheduler.add_job(candle_close, trigger='cron', second='0, 15, 30, 45',args=['15s',ASSET,RES])
        elif(interval=='1m'):
#print('printing 1m')
            scheduler.add_job(candle_close, trigger='cron', minute='0-59',args=['1m',ASSET,RES])
        elif(interval=='15m'):
            scheduler.add_job(candle_close, trigger='cron', minute='0, 15, 30, 45',args=['15m',ASSET,RES])
        elif(interval=='30m'):
            scheduler.add_job(candle_close, trigger='cron', minute='0, 30',args=['30m',ASSET,RES])
        elif(interval=='1h'):
            scheduler.add_job(candle_close, trigger='cron', hour='0-23',args=['1h',ASSET,RES])
        elif(interval=='1d'):
            scheduler.add_job(candle_close, trigger='cron', day='1-31',args=['1d',ASSET,RES])
        scheduler.start()
        # print(threading.enumerate())
        # on_tic = Thread(target=on_tick())
        # on_tic.daemon = True
        # on_tic.start()
#print('ontick.................')
        on_tick()

# print(threading.enumerate())





#Exmaple use

# client = FtxClientWs()

# # print(client.get_ticker(market='BTC/USDT'))
# # print('first',enumerate())
# print(client.get_trades('BTC-PERP'))

# dt = datetime.datetime.fromtimestamp(1663665996.4405653)
# dt1=datetime.datetime.fromtimestamp(1663665996.4088287)
# print(dt)
# print(dt1)
# while True:
#     print('second',enumerate())
#     time.sleep(60*60*24)
 

# # client.get_ticker("BTC-PERP")
# client._trades
