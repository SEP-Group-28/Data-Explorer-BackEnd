#DB CONNECTION TO MONGODB

import os
from pymongo import MongoClient

def connectdb():
    
# client = pymongo.MongoClient("mongodb+srv://thushalya:XVgpQf4Bn9qPrewc@cluster0.xxdhd7z.mongodb.net/?retryWrites=true&w=majority")
# db = client.test

    # print(os.environ.get('ADMIN_ROLE'))
    DATABASE_URL=os.environ.get('DATABASE_URL')
    # mongodb+srv://thushalya:XVgpQf4Bn9qPrewc@cluster0.xxdhd7z.mongodb.net/test
    # cluster= MongoClient(DATABASE_URL) #use for remote server

    cluster = MongoClient(DATABASE_URL,27017)  
    #use for localhost (mongodb compass)
    db=cluster.TestDB
    return db
