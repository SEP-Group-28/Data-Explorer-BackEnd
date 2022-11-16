#  from crypt import crypt
import talib
import bson, os
# from dotenv import load_dotenv
import json
# load_dotenv()
from pymongo import MongoClient
from flask import jsonify
from dbconnection import connectdb as db
from pubsub.pubsubservices import get_history_for_crypto_timestamp_for_indicators
from .market import Stock
import numpy as np

# notification_collection=db.notifications


class TechnicalIndicator:
    def __init__(self):
        return
    def get_close_values(self,market_type, market_name, interval,timestamp,datalimit,indicator):
        print("inside close values")
        if market_type == 'crypto':
            klines = get_history_for_crypto_timestamp_for_indicators(market_name+"/USDT", interval,timestamp,datalimit,indicator)
        elif market_type=='stock':
            klines=Stock().getStockDataListTimestampForIndicators(market_name,interval,timestamp,datalimit,indicator)
            # klines = get_historical_stock_data(name, interval)
        # print("klinesss", klines)
        close_prices = np.array([i[4] for i in klines], dtype=float)
        close_times = [i[0] for i in klines]
        return close_times, close_prices


    def get_close_and_volume_values(self,market_type, market_name, interval,timestamp,datalimit,indicator):
        if market_type == 'crypto':
            klines = get_history_for_crypto_timestamp_for_indicators(market_name+"/USDT", interval,timestamp,datalimit,indicator)
        elif market_type=='stock':
            klines = Stock().getStockDataListTimestampForIndicators(market_name, interval,timestamp,datalimit,indicator)
        close_prices = np.array([i[4] for i in klines], dtype=float)
        volume = np.array([i[5] for i in klines], dtype=float)
        close_times = [i[0] for i in klines]
        return close_times, volume, close_prices
    
    def get_high_low_close_values(self,market_type, market_name, interval,timestamp,datalimit,indicator):
        if market_type == 'crypto':
            klines = get_history_for_crypto_timestamp_for_indicators(market_name+"/USDT", interval,timestamp,datalimit,indicator)
        elif market_type=='stock':
            klines = Stock().getStockDataListTimestampForIndicators(market_name, interval,timestamp,datalimit,indicator)
        high_prices = np.array([i[2] for i in klines], dtype=float)
        low_prices = np.array([i[3] for i in klines], dtype=float)
        close_prices = np.array([i[4] for i in klines], dtype=float)
        close_times = [i[0] for i in klines]
        return high_prices, low_prices, close_prices, close_times

    # def insertnotifications(self,data):
    #     result=db[notification_collection].insert_one(data)
    #     # watchlist=db[crypt].find_one({'userid':id})
    #     # if not watchlist:
    #     #     return False
    #     # # print("getwatchlist", watchlist)
    #     # if 'list' in watchlist:
    #     #     return watchlist['list']
    #     # return False
    #     return result
    def calculate_rsi(self,market_type, market_name, interval,timestamp,datalimit):
    
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,15)
        rsi = talib.RSI(close_prices)
        time_rsi = dict(zip(close_times[14:], rsi[14:]))
        json_time_rsi = json.dumps(time_rsi)
        return json_time_rsi

    def calculate_obv(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, volume, close_prices = self.get_close_and_volume_values(market_type, market_name, interval,timestamp,datalimit,0)
        obv = talib.OBV(close_prices, volume)
        dict_indicator = dict(zip(close_times, obv))
        json_dict = json.dumps(dict_indicator)
        return json_dict
    
    def calculate_roc(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,11)
        roc = talib.ROC(close_prices)
        dict_indicator = dict(zip(close_times[10:], roc[10:]))
        json_dict = json.dumps(dict_indicator)
        return json_dict

    def calculate_ema(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,30)
        ema = talib.EMA(close_prices)
        dict_indicator = dict(zip(close_times[29:], ema[29:]))
        json_dict = json.dumps(dict_indicator)
        return json_dict


    def calculate_ma(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,30)
        ma = talib.MA(close_prices)
        dict_indicator = dict(zip(close_times[29:], ma[29:]))
        json_dict = json.dumps(dict_indicator)
        return json_dict


    def calculate_sma(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,30)
        sma = talib.SMA(close_prices)
        dict_indicator = dict(zip(close_times[29:], sma[29:]))
        json_dict = json.dumps(dict_indicator)
        return json_dict


    def calculate_wma(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,30)
        wma = talib.WMA(close_prices)
        dict_indicator = dict(zip(close_times[29:], wma[29:]))
        json_dict = json.dumps(dict_indicator)
        return json_dict

    def calculate_stoch(self,market_type, market_name, interval,timestamp,datalimit):
        high_prices, low_prices, close_prices, close_times = self.get_high_low_close_values(market_type, market_name, interval,timestamp,datalimit,9)
        slowk, slowd = talib.STOCH(high_prices, low_prices, close_prices)
        slowk_dict = dict(zip(close_times[8:], slowk[8:]))
        slowd_dict = dict(zip(close_times[8:], slowd[8:]))
        dict_indicator = {'slowk': slowk_dict, 'slowd': slowd_dict}
        json_dict = json.dumps(dict_indicator)
        return json_dict
    
    def calculate_bbands(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,11)
        upperband, middleband, lowerband = talib.BBANDS(close_prices)
        dict_upperband = dict(zip(close_times[10:], upperband[10:]))
        dict_middleband = dict(zip(close_times[10:], middleband[10:]))
        dict_lowerband = dict(zip(close_times[10:], lowerband[10:]))
        dict_indicator = {'upperband': dict_upperband, 'middleband': dict_middleband, 'lowerband': dict_lowerband}
        json_dict = json.dumps(dict_indicator)
        return json_dict

    def calculate_macd(self,market_type, market_name, interval,timestamp,datalimit):
        close_times, close_prices = self.get_close_values(market_type, market_name, interval,timestamp,datalimit,34)
        macd, macdsignal, macdhist = talib.MACD(close_prices)
        dict_macd = dict(zip(close_times[33:], macd[33:]))
        dict_macdsignal = dict(zip(close_times[33:], macdsignal[33:]))
        dict_macdhist = dict(zip(close_times[33:], macdhist[33:]))
        dict_indicator = {'macd': dict_macd, 'macdsignal': dict_macdsignal, 'macdhist': dict_macdhist}
        json_dict = json.dumps(dict_indicator)
        # print(json_dict)
        return json_dict







        

        
    # def gethistoricnotifications(self,time_period):
    #     coll = db[notification_collection]
    #     result = []
    #     for read in coll.find(time_period): # returns a cursor instance of the documents related
    #         result.append(read)
    #     return(result) 
        # watchlist=notification_collection.insert_one(
        #     {
        #         'userid':id,
        #         'list':[]
        #     }
        # )
        # return watchlist

        
    # def updatewatchlist(self,id,watchlist):
    #     notification_collection.update_one({'userid':id},{"$set":{'list':watchlist}})
    #     # print("updatedwatchlist function", watchlist)
    #     # if 'list' in watchlist:
    #     #     print('list in watchlist')
    #     # print("updated watchlist", [watchlist])
    #     if not watchlist:
    #         return False
    #     return watchlist



