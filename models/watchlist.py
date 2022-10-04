import bson, os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from flask import jsonify
from dbconnection import connectdb as db_con

db=db_con().TestDB
watchlist_collection=db.watchlist


class Watchlist:
    def __init__(self):
        return

    def getwatchlist(self,id):
        watchlist=watchlist_collection.find_one({'userid':id})
        if not watchlist:
            return False
        print("getwatchlist", watchlist)
        if 'list' in watchlist:
            return watchlist['list']
        return False

        
    def createwatchlist(self,id):
        watchlist=watchlist_collection.insert_one(
            {
                'userid':id,
                'list':[]
            }
        )
        return watchlist

        
    def updatewatchlist(self,id,watchlist):
        watchlist=watchlist_collection.update_one({'userid':id},{"$set":{'list':watchlist}})
        print("updatedwatchlist function", watchlist)
        print("updated watchlist", watchlist['list'])
        if not watchlist:
            return
        return watchlist['list']



