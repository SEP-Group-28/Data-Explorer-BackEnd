
from dbconnection import connectdb as db_con
from datetime import timezone, datetime

import flask
db=db_con().TestDB
market_collection=db.market


class Market:
    def __init__(self,brand):
        
        self.brand=brand
       
    
    def readHistory():
        raise NotImplementedError
    def saveRealTimeData():
        raise NotImplementedError
    def callRecentHistory():
        raise NotImplementedError
    def takeData():
        raise NotImplementedError


class Stock(Market):
    def __init__(self):
        super().__init__('Stock')

    def readHistory():
        pass

    def saveRealTimeData():
        pass

    def getStockDataList(self,stock,interval):
        print("gfttcghcghcgh",stock,interval)
        stock_collection=stock
        stock_data=db[stock_collection].find_one({'interval':interval})
        print()
        if not stock_data["data"]:
            return
        return stock_data["data"]
        
    # def getStock(self):
    #     stock_data=market_collection.find_one({'type':'stock'})
    #     if not stock_data:
    #         return
    #     return stock_data

    def getStockListFromMarket(self):
        stock_list_data=market_collection.find_one({'type':'stock'})
        if not stock_list_data:
            return
        return stock_list_data


    def insert_1day_interval_stock_data_to_database(self,stock_text_list,path):
        for filename in stock_text_list:
            print(filename)
            filepath = path + filename
            file = open(filepath, "r")
            candledata = []
            # print(len(file.readlines()))

            candlelines=file.readlines()
            for index in range(1,len(candlelines)):
                data = candlelines[index].split(',')
                Date = data[0].split('-')
                unix_timestamp = int(datetime(int(Date[0]), int(Date[1]), int(Date[2])).replace(tzinfo=timezone.utc).timestamp()*1000)
                data[0] = unix_timestamp
                candledata.append(data[:6])
            file.close()
            db[(filename.split('.')[0]).upper()].insert_one({
                "interval": "1d",
                "data": candledata
            })

    def insert_1hour_interval_stock_data_to_database(self,stock_text_list,path):
        for filename in stock_text_list:
            filepath =  path+ filename
            file = open(filepath, "r")
            candledata = []
            candlelines=file.readlines()
            for index in range(1,len(candlelines)):
                data = candlelines[index].split(',')
                concat_datetime = data[0] + ' ' + data[1]
                unix_timestamp = int(datetime.strptime(concat_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                data = data[1:7]
                data[0] = unix_timestamp
                candledata.append(data)
            
            file.close() 
            
            db[(filename.split('.')[0]).upper()].insert_one({
                "interval": "1h",
                "data": candledata
            })
       


    def insert_5min_interval_stock_data_to_database(self,stock_text_list,path):
        for filename in stock_text_list:
            filepath =  path+ filename
            file = open(filepath, "r")
            candledata = []
            candlelines=file.readlines()
            for index in range(1,len(candlelines)):
                data = candlelines[index].split(',')
                concat_datetime = data[0] + ' ' + data[1]
                unix_timestamp = int(datetime.strptime(concat_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                data = data[1:7]
                data[0] = unix_timestamp
                candledata.append(data)
            
            file.close()
        
            db[(filename.split('.')[0]).upper()].insert_one({
                "interval": "5m",
                "data": candledata
            })
            print(candledata)
        

    def delete_each_stock_collection_in_database(stock_text_list):
        for filename in stock_text_list:
            db[(filename.split('.')[0]).upper()].drop()

    def delete_one_stock_collection_in_database(stockname):
            db[stockname].drop()

    def add_stock_list_to_database(stock_list):
        db.market.insert_one(data_obj = {
            "type": "stock",
            "list": stock_list
        })
    
class Crypto(Market):
    
    def __init__(self):
        super().__init__('Crypto')
        

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
    # def getCrypto(self):
    #     crypto=market_collection.find_one({'type':'crypto'})
    #     if not crypto:
    #         return
    #     return crypto
    
    def getCryptoListFromMarket(self):
        
        crypto_list=market_collection.find_one({'type':'crypto'})
        
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
        print('inserted db',result)
        if not result:
            return
        return result
  

        
    




        
