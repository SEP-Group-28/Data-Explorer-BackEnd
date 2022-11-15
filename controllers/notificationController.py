
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
    @server.route('/notifications/present/<crypto_name>/<id>', methods=['GET'])
    def take_present_notifications(crypto_name,id):
        def stream(crypto_name,id):
            notifications = subscribe_to_socket_for_real_time_notifications(crypto_name,id)
            while True:                        
                msg = notifications.get()  
                yield msg

        return Response(stream(crypto_name,id), mimetype='text/event-stream')


    @server.route('/notifications/history/open_price', methods=['GET'])
    def take_history_notifications():
        print("receving........")
        return(historical_nots())
