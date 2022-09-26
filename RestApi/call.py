
from datetime import datetime

# import pandas as pd
import time, json
from time import sleep
import client

c = client.FtxClient(api_key="ldACQ0gfDgKg5_eQoQYDwjUafNL1V4B8W77qD_p9", api_secret="qMNgwI4gc3QwPnUs3ESFarb54NJKL4O5h7RBg51B")

# while True:
#     try:
#         btc_data = requests.get('https://ftx.com/api/markets/BTC-PERP').json()
#         print(btc_data['result']['ask'])
#     except Exception as e:
#         print(f'Error obtaining BTC old data: {e}')
    
#     if btc_data['result']['ask'] < 32000.0:
#         print('The trade requirement was not satisfied.')
#         sleep(2)
#         continue
    
#     elif btc_data['result']['ask'] >= 32000.0:
#         try:
#             r = c.place_order("ETH/USD", "buy", 1800.0, 0.006, "1243")
#             print(r)
#         except Exception as e:
#             print(f'Error making order request: {e}')
        
#         sleep(2)
        
#         try:
#             check = c.get_open_orders(r['id'])
#         except Exception as e:
#             print(f'Error checking for order status: {e}')
            
#         if check[0]['status'] == 'open':
#             print ('Order placed at {}'.format(pd.Timestamp.now()))
#             break
#         else:
#             print('Order was either filled or canceled at {}'.format(pd.Timestamp.now()))
#             break
endpoint_url='https://ftx.com/api/markets'

# all_markets=requests.get(endpoint_url).json()
# print(len(all_markets['result']))
# # df=pd.DataFrame(all_markets['result'])
# # df.set_index('name',inplace=True)
# # print(df)
# print()
# print()
# print()
# check=c.get_markets()
# print(len(check))
# print(c.get_single_market('BTC-PERP'))
# print(c.get_markets())

start=datetime(2022,1,1).timestamp()
print(start)
print(len(c.get_historical_prices('BTC/USDT',60*60*24,1641013200.0)))