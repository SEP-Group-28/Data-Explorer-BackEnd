import os
# from dotenv import load_dotenv
from pymongo import MongoClient
# load_dotenv()

def connectdb():
    # print(os.environ.get('ADMIN_ROLE'))
    DATABASE_URL=os.environ.get('DATABASE_URL')
    # cluster= MongoClient(DATABASE_URL) #use for remote server

    cluster = MongoClient(DATABASE_URL,27017)  
    #use for localhost (mongodb compass)
    db=cluster.TestDB
    return db
