
from dbconnection import connectdb as db_con

import flask
db=db_con().TestDB
market_collection=db.market


class Market:
    def __init__(self,brand,name=''):
        self.brand=brand
        self.name=name
    
    def readHistory():
        raise NotImplementedError
    def saveRealTimeData():
        raise NotImplementedError
    def callRecentHistory():
        raise NotImplementedError
    def takeData():
        raise NotImplementedError


class Stock(Market):
    def __init__(self,brand,name):
        super().__init__('Stock',name)

    def readHistory():
        pass

    def saveRealTimeData():
        pass

    def get_stock_data(self,stock,interval):
        stock_collection=stock
        stock_data=db[stock_collection].find({'type':interval})
        if not stock_data:
            return
        return stock_data
        
    def getStock(self):
        stock_data=market_collection.find_one({'type':'stock'})
        if not stock_data:
            return
        return stock_data

    def getStockList(self):
        stock_list_data=market_collection.find({'type':'stock'})
        if not stock_list_data:
            return
        return stock_list_data
class Crypto(Market):
    def __init__(self,brand,name):
        super().__init__('Crypto',name)

    # def readHistory(self,data):
    #     cryptoname= data['cryptoname']
    #     interval=data['interval']
    #     historical_data=data_center.get_history(cryptoname,interval)
    #     if not historical_data:
    #         return
    #     return historical_data

    # def takeData(self,data):
    #     cryptoname= data['cryptoname']
    #     interval=data['interval']
        # collection_name=cryptoname+'/'+'USDT_'+interval
        # def stream(cryptoname,interval):
        #     messages = listen_socket(cryptoname,interval)  
        #     while True:                        
        #         msg = messages.get()  
        #         yield msg

        # return flask.Response(stream(cryptoname,interval), mimetype='text/event-stream')



    #market collection calls
    def getCrypto(self):
        crypto=market_collection.find_one({'type':'crypto'})
        if not crypto:
            return
        return crypto

    
    def getCryptoList(self):
        crypto_list=market_collection.find({'type':'crypto'})
        if not crypto_list:
            return
        return crypto_list
        
        # crypto_collection=db.collection_name
        # crypto_data=crypto_collection.find()

        # if not crypto_data:
        #     return
        # return crypto_data





    #Crypto collection calls
    def getCryptoDataList(interval,collection):
        # print(data)
        crypto_collection=collection
#print('collect',crypto_data_collection)
#print('int',interval)

        crypto_data_list=db[crypto_collection].find_one({"interval":interval})
#print('data list',crypto_data_list)
        if not crypto_data_list:
            return
        return crypto_data_list
    
    def removeCryptoDataList(interval,collection):
        crypto_collection=collection
        result=db[crypto_collection].delete_one({'interval':interval})
        if not result:
            return
        return result

    def insertCryptoDataList(interval,collection,new_data):
        crypto_collection=collection
        result=db[crypto_collection].insert_one({'interval':interval,'data':new_data})
        if not result:
            return
        return result
  

        
    




        
