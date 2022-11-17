from audioop import add
from flask import request,jsonify,make_response
from bson.objectid  import ObjectId
import bcrypt
import jwt
from middlewares.verifyJWT import verifyJWT
import os
import utils.token as token
from models.alert import Alert
from models.alertusertoken import Add_TOKEN
from models.user import User
from utils.validate import validate_user,validate_email_and_password

def alertController(server): #Alert Controller


    @server.route('/alert/add-alert/<crypto_name>/<crypto_price>',methods=['POST']) #Route to add an alert using crypto name and crypto price
    @verifyJWT
    def add_alert(current_user,crypto_name,crypto_price): 
        try:
            alert_list=Alert().add_alert_for_price(crypto_name,float(crypto_price),current_user["_id"])
            return {"message": "Successfully added alert",
                "alertlist": alert_list['alertlist']},200
        except Exception as e:
            return jsonify({
                "message": "failed to add alert",
                "error": str(e),
                "data": None
        }), 400
    

    @server.route('/alert/remove-alert/<crypto_name>/<crypto_price>',methods=['DELETE'])#Route to delete an alert using crypto name and crypto price
    @verifyJWT
    def remove_alert(current_user,crypto_name,crypto_price):    
        try:
            alert = Alert().remove_alert_for_price(crypto_name,float(crypto_price),current_user["_id"])
            if not(alert):
                return{"message": "Already removed"},202
            else :
                alert_list=alert
                return{"message": "Successfully removed alert",
                    "alertlist": alert_list['alertlist']},200
        except Exception as e:
            return jsonify({
                "message": "failed to add alert",
                "error": str(e),
                "data": None
        }), 400



    @server.route('/alert/add-token/<token>',methods=['POST'])#Route to add an firebase token for alerts
    @verifyJWT
    def add_token(current_user,token):
        try:
             tokenlist=Add_TOKEN().add_token_for_user(current_user['_id'],token)
             return {"message": "Successfully added token",
                "tokenlist":tokenlist },200
        except Exception as e:
            return jsonify({
                "message": "failed to add token",
                "error": str(e),
                "data": None
        }), 400
 
    @server.route('/alert/remove-token/<token>',methods=['DELETE']) #Route to remove firebase token for alerts
    @verifyJWT
    def remove_token(current_user,token):
        try:
             tokenlist=Add_TOKEN().remove_token_for_user(current_user['_id'],token)
             return {"message": "Successfully removed token",
                "tokenlist":tokenlist },200
        except Exception as e:
            return jsonify({
                "message": "failed to remove token",
                "error": str(e),
                "data": None
        }), 400
        


    @server.route('/alert/get-alerts/<crypto_name>',methods=['GET'])#Route to get alerts for each crypto for each user
    @verifyJWT
    def get_all_alerts_for_user(current_user,crypto_name):
        crypto_name=crypto_name+'/USDT'
        user_id=current_user['_id']
        try:
            fetched_alerts=Alert().take_previous_alerts_for_price(crypto_name)
            previous_alert_prices=[]
            if fetched_alerts is None:
                return previous_alert_prices
            alertlist=fetched_alerts['alertlist']
            for i in alertlist:
                if (i[1]==user_id):
                    previous_alert_prices.append(i[0])
            return {"message":"Successfully fetched all alerts for crypto",'allalertlistcrypto':previous_alert_prices},200
            
        except Exception as e:
            return {"message":"Fetching all alerts for crypto failed"},404



    @server.route('/alert/get-all-alerts',methods=['GET'])
    @verifyJWT
    def get_all_alerts(current_user):
        user_id=current_user['_id']
        try:
            fetched_alerts=Alert().take_previous_all_alerts()
            data=[]
            for i in fetched_alerts:
                for j in i['alertlist']:
                    if j[1]==user_id:
                        data.append({'crypto_name':i['name'], 'crypto_price':j[0]})

            return {'message':'Successfully fetched all alerts',"allalertlist":data},200
            
        except Exception as e:
            return {"message":"Fetching all alerts failed"},404