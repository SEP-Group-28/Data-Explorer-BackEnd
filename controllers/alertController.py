from audioop import add
from flask import request,jsonify,make_response
from bson.objectid  import ObjectId
import bcrypt
from dotenv import load_dotenv
load_dotenv()
import jwt
from middlewares.verifyJWT import verifyJWT
import os
import utils.token as token
from models.user import User
from utils.validate import validate_user,validate_email_and_password
from pubsub.pubsubservices import add_firebase_alert


def alertController(server):
    @server.route('/alert/<crypto_name>/<crypto_price>/<token>',methods=['POST'])
    # @verifyJWT
    def add_alert(crypto_name,crypto_price,token):
        # print("currentuser............",current_user)
        print("crypto",crypto_name)
        print('crypto_price',crypto_price)
        print('token',token)
        alertsdict=add_firebase_alert(crypto_name,float(crypto_price),token)
        return alertsdict