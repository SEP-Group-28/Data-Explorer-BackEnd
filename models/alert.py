from dbconnection import connectdb as db
from datetime import timezone, datetime

import flask
alert_collection=db().alerts
class Alert:
    def add_alert_for_price(self,crypto_name,crypto_price,user_id):
        previous_alerts=self.take_previous_alerts_for_price(crypto_name+'/USDT')
        # print('previous alerts printing',previous_alerts)
        if not previous_alerts:
            # alertsdict[crypto_price]=[[crypto_name+'/USDT',user_id]]
            alert_collection.insert_one({"name":crypto_name+'/USDT','alertlist':[[crypto_price,user_id]]})
        else:
            alert_list=previous_alerts['alertlist']
            # alertsdict[crypto_price].append([crypto_name+'/USDT',user_id])
            alert_list.append([crypto_price,user_id])
            # print('printing',alert_list)
            self.update_alerts_for_price(crypto_name+'/USDT',alert_list)
        return self.take_previous_alerts_for_price(crypto_name+'/USDT')
    
    def remove_alert_for_price(self,crypto_name,crypto_price,user_id):
        previous_alerts=self.take_previous_alerts_for_price(crypto_name+'/USDT')
        # print('previous alerts printing',previous_alerts)
        if previous_alerts:
            # alertsdict[crypto_price]=[[crypto_name+'/USDT',user_id]]
            # alert_collection.insert_one({"name":crypto_name+'/USDT','alertlist':[[crypto_price,user_id]]})
        # else:
            alert_list=previous_alerts['alertlist']
            if [crypto_price,user_id] not in alert_list:
                return False
            # alertsdict[crypto_price].append([crypto_name+'/USDT',user_id])
            alert_list.remove([crypto_price,user_id])
            # print('printing',alert_list)
            self.update_alerts_for_price(crypto_name+'/USDT',alert_list)
        return self.take_previous_alerts_for_price(crypto_name+'/USDT')

    def take_previous_alerts_for_price(self,crypto_name):
        try:
            fetched_alert=alert_collection.find_one({"name":crypto_name})
            # print('fetching_alert_list',fetched_alert)
        except Exception as e:
            print(e)
        # print(crypto_name,"alert is fetched",fetched_alert)
        # print('fetchng............',fetched_alert)
        if fetched_alert:
            return fetched_alert
        return fetched_alert

    def take_previous_all_alerts(self):
        try:
            alerts=alert_collection.find()
        
        except Exception as e:
            print(e)

        if alerts:
            return alerts
        return alerts

    def update_alerts_for_price(self,crypto_name,alert_list):
        alert_collection.update_one(
            {'name':crypto_name},
                    {
                        "$set":{"alertlist":alert_list}
                    }
        )


# class Alert:
#     def add_alert_for_price(self,crypto_name,crypto_price,user_id):
#         previous_alerts=self.take_previous_alerts_for_price(crypto_price)
#         if not previous_alerts:
#             # alertsdict[crypto_price]=[[crypto_name+'/USDT',user_id]]
#             alert_collection.insert_one({"price":crypto_price,'alertlist':[[crypto_name+'/USDT',user_id]]})
#         else:
#             alert_list=previous_alerts['alertlist']
#             # alertsdict[crypto_price].append([crypto_name+'/USDT',user_id])
#             alert_list.append([crypto_name+'/USDT',user_id])
#             self.update_alerts_for_price(crypto_price,alert_list)


#     def take_previous_alerts_for_price(self,crypto_price):
#         fetched_alert=alert_collection.find_one({"price":crypto_price})
#         print(crypto_price,"alert is fetched",fetched_alert)
#         if fetched_alert:
#             return fetched_alert
#         return False

#     def update_alerts_for_price(self,crypto_price,alert_list):
#         alert_collection.update_one(
#             {'price':crypto_price},
#                     {
#                         "$set":{"alertlist":alert_list}
#                     }
#         )


