#DB CONNECTION TO MONGODB

import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
import pymongo
# load_dotenv()
import certifi

def connectdb():
    
    # client = pymongo.MongoClient("mongodb+srv://thushalya:try@cluster0.xxdhd7z.mongodb.net/?retryWrites=true&w=majority")
    # client = pymongo.MongoClient("mongodb+srv://thushalya:try@cluster0.xxdhd7z.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    # db = client['Crypstoxplorer']



    # print(os.environ.get('ADMIN_ROLE'))
    # DATABASE_URL='mongodb+srv://thushalya:XVgpQf4Bn9qPrewc@cluster0.xxdhd7z.mongodb.net/?retryWrites=true&w=majority'
    # mongodb+srv://thushalya:XVgpQf4Bn9qPrewc@cluster0.xxdhd7z.mongodb.net/test
    # cluster= MongoClient(DATABASE_URL) #use for remote server

    cluster = pymongo.MongoClient("mongodb://localhost:27017",27017)  
    # use for localhost (mongodb compass)
    db=cluster.TestDB
    # db=cluster.Crypstoxplorer
    return db
