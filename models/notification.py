# from crypt import crypt
import bson, os
# from dotenv import load_dotenv
# load_dotenv()
from pymongo import MongoClient
from flask import jsonify
from dbconnection import connectdb as db

notification_collection=db().notifications


class Notification:
    def __init__(self):
        return

    def insertnotifications(data,user_id):
        print("=======================")
        print('data is',data)
        print('user_id is',user_id)
        print("=======================")
        result=notification_collection.update_one({
            "_id":user_id},
            {"$push":{"alertlist":[data['time'],data['data']['symbol'],data['data']['price']]}}, upsert=True)
        # watchlist=db[crypt].find_one({'userid':id})
        # if not watchlist:
        #     return False
        # # print("getwatchlist", watchlist)
        # if 'list' in watchlist:
        #     return watchlist['list']
        # return False
        return result

        
    def gethistoricnotifications(time_period):
        time_period = time_period[0]
        coll = notification_collection
        result = []

        # for read in coll.find(time_period): # returns a cursor instance of the documents related
        #     result.append(read)
        # return(result) 

        temp = coll.find(time_period) 
        print("type of temp", type(temp))
        print("temp alert list", temp[0]['alertlist'])
        return sorted(temp[0]['alertlist'], key=lambda x: x[0], reverse=True)

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



