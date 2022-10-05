
from pubsub.pubsubservices import subscribe_to_socket
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
from models.market import Stock
import json

load_dotenv()
import os



def notificationController(server):
    @server.route('/notifications/present/', methods=['GET'])
    def take_present_notifications():
        def stream():
            notifications = subscribe_to_socket()
            while True:                        
                msg = notifications.get()  
                yield msg

        return Response(stream(), mimetype='text/event-stream')


    @server.route('/notifications/history/', methods=['GET'])
    def take_history_notifications():
        return(historical_nots())
