from dbconnection import connectdb as db

notification_collection=db().notifications

#NOTIFICATION MODEL
class Notification:
    def __init__(self):
        return

    def insertnotifications(data,user_id):
        result=notification_collection.update_one({
            "_id":user_id},
            {"$push":{"alertlist":[data['time'],data['data']['symbol'],data['data']['price']]}}, upsert=True)
        return result
    
    def delnotification(user_id,cryptoname,price):
        cryptoname=cryptoname+'/USDT'
        arraylist=notification_collection.find_one({
            '_id':user_id
        },{
            'alertlist':1, '_id':0
        })['alertlist']

        for i in range(len(arraylist)-1, -1, -1):
            if arraylist[i][1]==cryptoname and arraylist[i][2]==float(price):
                arraylist.pop(i)
                break
            
        result=notification_collection.update_one(
            {'_id':user_id},
            {'$set':{'alertlist':arraylist}}
        )

        if result:
            return 'success'
        return 'error'

    def delallnotifications(user_id):
        result=notification_collection.update_one(
            {'_id':user_id},
            {'$unset':{'alertlist':""}}
        )
        if result:
            return 'success'
        return 'error'
        
    def gethistoricnotifications(time_period):
        time_period = time_period[0]
        coll = notification_collection
        temp = coll.find(time_period) 
        return sorted(temp[0]['alertlist'], key=lambda x: x[0], reverse=True)




