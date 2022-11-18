
from pubsub.pubsubservices import subscribe_to_socket_for_real_time_notifications,historical_nots
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole
from models.notification import Notification


def notificationController(server):
    @server.route('/notifications/present', methods=['GET'])
    @verifyJWT
    def take_present_notifications(current_user):
        try:
            print("hello im taking present notifications now")
            id = current_user["_id"]
            def stream(id):
                notifications = subscribe_to_socket_for_real_time_notifications(id)
                while True:                        
                    msg = notifications.get()  
                    print("oh here is my msg",msg)
                    print("oh here is my notifications 1", notifications)
                    yield msg

            return Response(stream(id), mimetype='text/event-stream')
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/notifications/history', methods=['GET'])
    @verifyJWT
    def take_history_notifications(current_user):
        try:
            id = current_user["_id"]
            print("user id", id)
            print("receving........")
            return(historical_nots(id))
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500


    @server.route('/notifications/get-count', methods=['GET'])
    @verifyJWT
    def take_history_notifications_count(current_user):
        try:
            id = current_user["_id"]
            print("user id", id)
            print("receving........")
            # print(historical_nots(id))
            return str(len(historical_nots(id)['last day notifications']))
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/notifications/delete/<cryptoname>/<price>', methods=['DELETE'])
    @verifyJWT
    def delete_history_notifications(current_user,cryptoname,price):
        try:
            id = current_user["_id"]
            print(cryptoname)
            print(price)
            print("user id", id)
            print("receving........")
            if (id!=None and cryptoname != None and price!= None):
                result=Notification.delnotification(id,cryptoname,price)
            return result
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/notifications/delete/all', methods=['DELETE'])
    @verifyJWT
    def delete_all_history_notifications(current_user):
        try:
            id = current_user["_id"]
            # print(cryptoname)
            # print(price)
            print("user id", id)
            print("receving........")
            if (id!=None ):
                result=Notification.delallnotifications(id)
            return result
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500
