
from db_con import connectdb as db_con

db=db_con().TestDB


class Market:
    def __init__(self,brand,name):
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


class stock(Market):
    def __init__(self,brand,name):
        super().__init__(brand,name)

    def readHistory():
        pass

    def saveRealTimeData():
        pass
    def callRecentHistory():
        pass


class crypto(Market):
    def __init__(self,brand,name):
        super().__init__(brand,name)

    def readHistory():
        pass

    def saveRealTimeData():
        pass
    def callRecentHistory(self,data):
        cryptoname= data['cryptoname']
        interval=data['interval']

    def takeData(self,data):
        cryptoname= data['cryptoname']
        interval=data['interval']
        collection_name=cryptoname+'/'+'USDT_'+interval
        
        # crypto_collection=db.collection_name
        # crypto_data=crypto_collection.find()

        # if not crypto_data:
        #     return
        # return crypto_data



        
