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
from models.alert import Alert
from models.alertusertoken import Add_TOKEN
from models.user import User
from utils.validate import validate_user,validate_email_and_password
# from pubsub.pubsubservices import add_firebase_alert


def alertController(server):
    @server.route('/alert/add-alert/<crypto_name>/<crypto_price>',methods=['POST'])
    @verifyJWT
    def add_alert(current_user,crypto_name,crypto_price):
        print("currentuser............",current_user)
        print("crypto",crypto_name)

        print('crypto_price',crypto_price)
        # print('token',token)
         
        try:
            alert_list=Alert().add_alert_for_price(crypto_name,float(crypto_price),current_user["_id"])
            return jsonify({"message": "Successfully added alert",
                "alertlist": alert_list['alertlist']})
        except Exception as e:
            return jsonify({
                "message": "failed to add alert",
                "error": str(e),
                "data": None
        }), 400
    
    @server.route('/alert/remove-alert/<crypto_name>/<crypto_price>',methods=['DELETE'])
    @verifyJWT
    def remove_alert(current_user,crypto_name,crypto_price):
        print("currentuser............",current_user)
        print("crypto",crypto_name)

        print('crypto_price',crypto_price)
        # print('token',token)
         
        try:
            alert_list=Alert().remove_alert_for_price(crypto_name,float(crypto_price),current_user["_id"])
            return jsonify({"message": "Successfully added alert",
                "alertlist": alert_list['alertlist']})
        except Exception as e:
            return jsonify({
                "message": "failed to add alert",
                "error": str(e),
                "data": None
        }), 400

        # return alertsdict

    @server.route('/alert/add-token/<token>',methods=['POST'])
    @verifyJWT
    def add_token(current_user,token):
        print("currentuser............",current_user)
        # print("crypto",crypto_name)
        # print('crypto_price',crypto_price)
        print('token',token)
        try:
             tokenlist=Add_TOKEN().add_token_for_user(current_user['_id'],token)
             return jsonify({"message": "Successfully added token",
                "tokenlist":tokenlist })
        except Exception as e:
            return jsonify({
                "message": "failed to add token",
                "error": str(e),
                "data": None
        }), 400
        
       
        # alertsdict=add_firebase_alert(crypto_name,float(crypto_price),token)
        # return alertsdict
    @server.route('/alert/remove-token/<token>',methods=['POST'])
    @verifyJWT
    def remove_token(current_user,token):
        print("currentuser............",current_user)
        # print("crypto",crypto_name)
        # print('crypto_price',crypto_price)
        print('token',token)
        try:
             tokenlist=Add_TOKEN().remove_token_for_user(current_user['_id'],token)
             return jsonify({"message": "Successfully removed token",
                "tokenlist":tokenlist })
        except Exception as e:
            return jsonify({
                "message": "failed to add token",
                "error": str(e),
                "data": None
        }), 400
        

    @server.route('/alert/get-alerts/<crypto_name>',methods=['GET'])
    @verifyJWT
    def get_all_alerts_for_user(current_user,crypto_name):
        print("currentuser............",current_user)
        # print("currentuser............",current_user)
        # print("crypto",crypto_name)
        # print('crypto_price',crypto_price)
        # print('token',token)
        user_id=current_user['_id']
        try:
            fetched_alerts=Alert().take_previous_alerts_for_price(crypto_name)
            print('fetched.................',fetched_alerts)
            previous_alert_prices=[]
            if fetched_alerts is None:
                return previous_alert_prices
            alertlist=fetched_alerts['alertlist']
            for i in alertlist:
                if (i[1]==user_id):
                    previous_alert_prices.append(i[0])
            return previous_alert_prices
        except Exception as e:
            print(e)

    @server.route('/alert/get-all-alerts',methods=['GET'])
    @verifyJWT
    def get_all_alerts(current_user):
        # print("currentuser............",current_user)
        # print("currentuser............",current_user)
        # print("crypto",crypto_name)
        # print('crypto_price',crypto_price)
        # print('token',token)
        user_id=current_user['_id']
        try:
            fetched_alerts=Alert().take_previous_all_alerts()
            data={}
            # print('printing the data',data)
            
            for i in fetched_alerts:
                # print('printing',i)
                # data.append([i['name'],i['al']])
                # print('printing i',i)
                data[i['name']]={}
                # print("printing data",data)
                for j in i['alertlist']:
                    if j[1]==user_id:
                        data[i['name']]=j[0]

            # print('fetched.................',data)
            return data
            # previous_alert_prices=[]
            # if fetched_alerts is None:
            #     return previous_alert_prices
            # alertlist=fetched_alerts['alertlist']
            # for i in alertlist:
            #     if (i[1]==user_id):
            #         previous_alert_prices.append(i[0])
            # return previous_alert_prices
        except Exception as e:
            print(e)


        # print(user_id)
        # alertsdict=add_firebase_alert(crypto_name,float(crypto_price),token)

        
        # return alertsdict