from dbconnection import connectdb as database
from datetime import timezone, datetime
db = database()

market_collection=db.market

#MARKET MODEL
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
        stock_collection=stock
        stock_data=db[stock_collection].find_one({'interval':interval})
        if not stock_data["data"]:
            return
        return stock_data["data"]
    
    def getStockDataListTimestamp(self,stock, interval,timestamp,datalimit):
        stock_collection=stock
        stock_data = db[stock_collection].aggregate([
            {'$match' :{"interval":interval}},
            {'$unwind':'$data'},
            {'$sort':{'data':-1}},
            {"$skip":int(timestamp)},
            {'$limit':int(datalimit)},
        ])
        
        list1 = list(stock_data)
        list1.reverse()
        stock_list = [i['data'] for i in list1]
        
        if not stock_list:
            return
        return stock_list
        
    def getStockDataListTimestampForIndicators(self,stock, interval,timestamp,datalimit,indicator):
        stock_collection=stock
        print("Timestamp , limit",timestamp,datalimit,interval)
        stock_data = db[stock_collection].aggregate([
            {'$match' :{"interval":interval}},
            {'$unwind':'$data'},
            {'$sort':{'data':-1}},
            {"$skip":int(timestamp)},
            {'$limit':int(datalimit)+indicator},
        ])
        
        list1 = list(stock_data)
        list1.reverse()
        stock_list = [i['data'] for i in list1]
        
        if not stock_list:
            return
        return stock_list

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
            candlelines=file.readlines()
            for index in range(1,len(candlelines)):
                data = candlelines[index].split(',')
                Date = data[0].split('-')
                unix_timestamp = float(datetime(int(Date[0]), int(Date[1]), int(Date[2])).replace(tzinfo=timezone.utc).timestamp()*1000)
                data[0] = unix_timestamp
                candledata.append([float(i) for i in data[:6]])
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
                unix_timestamp = float(datetime.strptime(concat_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                data = data[1:7]
                data[0] = unix_timestamp
                candledata.append([float(i) for i in data])
            
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
                unix_timestamp = float(datetime.strptime(concat_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                data = data[1:7]
                data[0] = unix_timestamp
                candledata.append([float(i) for i in data])
            
            file.close()
        
            db[(filename.split('.')[0]).upper()].insert_one({
                "interval": "5m",
                "data": candledata
            })
        

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
    
    def getCryptoListFromMarket(self):
        crypto_list=market_collection.find_one({'type':'crypto'})
        
        if not crypto_list:
            return
        return crypto_list
        
    def getCryptoDataList(interval,collection):
        crypto_collection=collection
        crypto_data_list=db[crypto_collection].find_one({"interval":interval})
        if not crypto_data_list:
            return
        return crypto_data_list

    def updateCryptoDataList(interval,collection,new_data):
            crypto_collection=collection
            result=db[crypto_collection].update_one(
                {'interval':interval},
                {
                    "$set":{"data":new_data}
                }
            )
            if not result:
                return
            return result

    def getCryptoDataListForTimeStamp(interval,collection,timestamp,datalimit):
        crypto_collection=collection
        crypto_data_list=db[crypto_collection].aggregate([
            {'$match' :{"interval":interval}},
            {'$unwind':'$data'},
            {'$sort':{'data':-1}},
            {"$skip":int(timestamp)},
            {'$limit':int(datalimit)},

           ] )
        list1=list(crypto_data_list)
        list1.reverse()
        crypto_list=[i['data'] for i in list1]

        if not crypto_list:
            return
        return crypto_list

    def getCryptoDataListForTimeStampForIndicator(interval,collection,timestamp,datalimit,indicator):
        crypto_collection=collection
        crypto_data_list=db[crypto_collection].aggregate([
            {'$match' :{"interval":interval}},
            {'$unwind':'$data'},
            {'$sort':{'data':-1}},
            {"$skip":int(timestamp)},
            {'$limit':int(datalimit)+indicator},
    
           ] )
        list1=list(crypto_data_list)
        list1.reverse()
        crypto_list=[i['data'] for i in list1]
        if not crypto_list:
            return
        return crypto_list


  

        
    




        
