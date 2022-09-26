
from datetime import datetime
from flask import Flask,render_template,request,jsonify,make_response
from flask_cors import CORS
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid  import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os

from controllers.authController import authController
from controllers.userController import userController
from config.allowedOrigins import allowedOrigins
from controllers.cryptoController import cryptoController
from controllers.stockController import stockController
from apscheduler.schedulers.background import BackgroundScheduler
# import utils.validation as validate

server = Flask(__name__)
scheduler = BackgroundScheduler()

# pub_sub_model()
# scheduler.addjob(get_live_data)
# scheduler.addjob(save_live_data)
# scheduler.addjob(check_notifications)

# scheduler.start()
# server.config["MONGO_URI"]='mongodb://localhost:27017/TestDB'

# mongo = PyMongo(server)

CORS(server,supports_credentials=True,origins=allowedOrigins)


authController(server)
userController(server)
cryptoController(server)
stockController(server)


# @server.route("/members")
# def members():
#     return {"members":[" Member6","Member dh h ","Member   3 "]}

# @server.route("/mydetail",methods=["GET","POST"])
# def show_my_details():
    
#     if(request.method=="POST"):
#         form_data =request.form
#         print(form_data)
#         # print("Form Data",form_data)
#         name = form_data['name']
#         email = form_data['email']
#         # mongo.db.record.insert_one({'Name': form_data['name'],'Email':form_data['email']})
#         record_collection.insert_one({'Name': form_data['name'],'Email':form_data['email']})
#         return render_template('show.html',name=name,email=email)
#         print(name,email)
#     return render_template('mydetail.html')

# @server.route("/mydetail",methods=["GET","POST"])
# def show_test():
#     current_time =datetime.now()
#     return render_template("mydetail.html",current_time=current_time)




if __name__== "__main__":
    server.run(debug=True)