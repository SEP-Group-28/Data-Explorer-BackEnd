from dbconnection import connectdb as db

alert_collection=db().alerts

#ALERT MODEL
class Alert:
    def add_alert_for_price(self,crypto_name,crypto_price,user_id):
        previous_alerts=self.take_previous_alerts_for_price(crypto_name+'/USDT')
        if not previous_alerts:
            alert_collection.insert_one({"name":crypto_name+'/USDT','alertlist':[[crypto_price,user_id]]})
        else:
            alert_list=previous_alerts['alertlist']
            alert_list.append([crypto_price,user_id])
            self.update_alerts_for_price(crypto_name+'/USDT',alert_list)
        return self.take_previous_alerts_for_price(crypto_name+'/USDT')
    
    def remove_alert_for_price(self,crypto_name,crypto_price,user_id):
        previous_alerts=self.take_previous_alerts_for_price(crypto_name+'/USDT')
        if previous_alerts:
            alert_list=previous_alerts['alertlist']
            if [crypto_price,user_id] not in alert_list:
                return False
            alert_list.remove([crypto_price,user_id])
            self.update_alerts_for_price(crypto_name+'/USDT',alert_list)
        return self.take_previous_alerts_for_price(crypto_name+'/USDT')

    def take_previous_alerts_for_price(self,crypto_name):
        try:
            fetched_alert=alert_collection.find_one({"name":crypto_name})
        except Exception as e:
            print(e)

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


