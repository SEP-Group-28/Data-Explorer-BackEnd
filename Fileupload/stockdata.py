import json
import time
from Dbconnection import connectdb as db_con
from datetime import timezone, datetime



db=db_con().TestDB

stock_list=['fb.us.txt', 'tsla.us.txt','yten.us.txt','baba.us.txt']
def insert_1day_interval_stock_data_to_database(stock_text_list):
    for filename in stock_text_list:
        print(filename)
        path = 'C:\\Users\\Thushalya\\Desktop\\Sem 5 Project\\Project\\stock data\\1 Day\\Stocks\\' + filename
        file = open(path, "r")
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
        db[filename.split('.')[0]].insert_one({
            "interval": "1d",
            "data": candledata
        })

def insert_1hour_to_db(list):
    for i in list:
        file_name = i + '.us.txt'
        path = 'G:\Projects\stockpilot-backend\stock_files\\1_hour\\' + file_name
        file = open(path, "r")
        ls = []
        a = False
        for x in file:
            if a:
                line = x.split(',')
                datetime_val = line[0] + ' ' + line[1]
                unix_timestamp = int(datetime.strptime(datetime_val, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                line = line[1:]
                line[0] = unix_timestamp
                line[6] = unix_timestamp
                ls.append(line)
            a = True
        file.close() 
        data_obj = {
            "type": 'data_1h',
            "data": ls
        }

        # db_action("insert_one", [data_obj, i], "admin")

def insert_5min_to_db(list):
    for i in list:
        file_name = i + '.us.txt'
        path = 'G:\Projects\stockpilot-backend\stock_files\\5_min\\' + file_name
        file = open(path, "r")
        ls = []
        a = False
        for x in file:
            if a:
                line = x.split(',')
                datetime_val = line[0] + ' ' + line[1]
                unix_timestamp = int(datetime.strptime(datetime_val, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()*1000)
                line = line[1:]
                line[0] = unix_timestamp
                line[6] = unix_timestamp
                ls.append(line)
            a = True
        file.close()
        data_obj = {
            "type": 'data_5m',
            "data": ls
        }
        # db_action("insert_one", [data_obj, i], "admin")

def delete(ls):
    for i in ls:
        pass
        # db_action("delete_collection", [i], "admin")

def add_stock(ls):
    data_obj = {
        "type": "stock",
        "data": ls
    }
    # db_action("insert_one", [data_obj, 'symbols'], "admin")

insert_1day_interval_stock_data_to_database(stock_list)
# insert_1day_to_db(['aapl', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk-a', 'nvda', 'v', 'jpm', 'jnj', 'baba', 'wmt', 'unh', 'hd'])
# insert_1hour_to_db(['aapl', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk-a', 'nvda', 'v', 'jpm', 'jnj', 'baba', 'wmt', 'unh', 'hd'])
# insert_5min_to_db(['aapl', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk-a', 'nvda', 'v', 'jpm', 'jnj', 'baba', 'wmt', 'unh', 'hd'])

# delete(['aapl', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk-a', 'nvda', 'v', 'jpm', 'jnj', 'baba', 'wmt', 'unh', 'hd'])

# add_stock(['aapl', 'msft', 'goog', 'amzn', 'fb', 'tsla', 'brk-a', 'nvda', 'v', 'jpm', 'jnj', 'baba', 'wmt', 'unh', 'hd'])
