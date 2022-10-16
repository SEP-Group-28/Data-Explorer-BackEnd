from crypt import crypt
import bson, os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from flask import jsonify
from dbconnection import connectdb as db_con

db=db_con().TestDB
notification_collection=db.notifications


class Notification:
    def __init__(self):
        return

    def insertnotifications(self,data):
        result=db[notification_collection].insert_one(data)
        # watchlist=db[crypt].find_one({'userid':id})
        # if not watchlist:
        #     return False
        # # print("getwatchlist", watchlist)
        # if 'list' in watchlist:
        #     return watchlist['list']
        # return False
        return result

        
    def gethistoricnotifications(self,time_period):
        coll = db[notification_collection]
        result = []
        for read in coll.find(time_period): # returns a cursor instance of the documents related
            result.append(read)
        return(result) 
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



