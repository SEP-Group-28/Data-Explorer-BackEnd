from pubsub.pubsubservices import historical_nots
from middlewares.verifyJWT import verifyJWT
from models.notification import Notification

def notificationController(server):

    @server.route('/notifications/history', methods=['GET']) #ROUTE TO GET HISTORICAL NOTIFICATIONS
    @verifyJWT
    def take_history_notifications(current_user):
        try:
            id = current_user["_id"]
            return(historical_nots(id))
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500


    @server.route('/notifications/get-count', methods=['GET']) #ROUTE TO GET THE COUNT OF ALL NOTIFICATIONS
    @verifyJWT
    def take_history_notifications_count(current_user):
        try:
            id = current_user["_id"]
            return str(len(historical_nots(id)['last day notifications']))
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/notifications/delete/<cryptoname>/<price>', methods=['DELETE']) #ROUTE TO DELETE NOTICATIONS USING CRYPTONAME AND PRICE
    @verifyJWT
    def delete_history_notifications(current_user,cryptoname,price):
        try:
            id = current_user["_id"]
            if (id!=None and cryptoname != None and price!= None):
                result=Notification.delnotification(id,cryptoname,price)
            return result
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/notifications/delete/all', methods=['DELETE']) #ROUTE TO DELETE ALL NOTIFICATIONS AT ONCE
    @verifyJWT
    def delete_all_history_notifications(current_user):
        try:
            id = current_user["_id"]
            if (id!=None ):
                result=Notification.delallnotifications(id)
            return result
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500
