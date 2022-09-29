
from models.market import Stock



stockmodel=Stock()
stock_list=['fb.us.txt', 'tsla.us.txt','yten.us.txt','baba.us.txt']

one_day_file_path='C:\\Users\\Thushalya\\Desktop\\Sem 5 Project\\Project\\stock data\\1 Day\\Stocks\\'
one_hour_file_path='C:\\Users\\Thushalya\\Desktop\\Sem 5 Project\\Project\\stock data\\1 Hour\\Stocks\\'
five_min_file_path='C:\\Users\\Thushalya\\Desktop\\Sem 5 Project\\Project\\stock data\\5 Min\\Stocks\\'
stockmodel.insert_1day_interval_stock_data_to_database(stock_list,one_day_file_path)
stockmodel.insert_1hour_interval_stock_data_to_database(stock_list,one_hour_file_path)
stockmodel.insert_5min_interval_stock_data_to_database(stock_list,five_min_file_path)

stockmodel.delete_each_stock_collection_in_database(stock_list)
stockmodel.delete_one_stock_collection_in_database('baba')
stockmodel.add_stock_list_to_database(['adbe','calm'])


