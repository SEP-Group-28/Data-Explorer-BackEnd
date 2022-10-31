import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

def connectdb():
    DATABASE_URL=os.getenv('DATABASE_URL') 
    # cluster= MongoClient(DATABASE_URL) #use for remote server

    cluster = MongoClient(DATABASE_URL,27017)  
    #use for localhost (mongodb compass)
    db=cluster.TestDB
    return db
