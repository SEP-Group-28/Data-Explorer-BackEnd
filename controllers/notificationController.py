
from pubsub.pubsubservices import subscribe_to_socket_for_real_time_notifications,historical_nots
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole
# from dotenv import load_dotenv
from models.market import Stock
import json

# load_dotenv()
import os



def notificationController(server):
    @server.route('/notifications/present', methods=['GET'])
    @verifyJWT
    def take_present_notifications(current_user):
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


    @server.route('/notifications/history', methods=['GET'])
    @verifyJWT
    def take_history_notifications(current_user):
        id = current_user["_id"]
        print("user id", id)
        print("receving........")
        return(historical_nots(id))

    @server.route('/notifications/get-count', methods=['GET'])
    @verifyJWT
    def take_history_notifications_count(current_user):
        id = current_user["_id"]
        print("user id", id)
        print("receving........")
        # print(historical_nots(id))
        return str(len(historical_nots(id)['last day notifications']))
