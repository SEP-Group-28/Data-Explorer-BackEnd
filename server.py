from datetime import datetime

# from controllers.alertController import alertController

from controllers.technicalIndicactorsController import technicalIndicactorsController




from FTX.websocketCall import start_streaming
from controllers.watchlistController import watchlistController
from flask import Flask
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
from controllers.adminController import adminController
from controllers.technicalIndicactorsController import technicalIndicactorsController
# from controllers.notificationController import notificationController
from apscheduler.schedulers.background import BackgroundScheduler


from pubsub.pubsubservices import start_publisher_subscriber_model,look_for_nots
server = Flask(__name__)

# scheduler.start()
# server.config["MONGO_URI"]='mongodb://localhost:27017/TestDB'

# mongo = PyMongo(server)
 
CORS(server,supports_credentials=True,origins=allowedOrigins)
scheduler = BackgroundScheduler()


@server.before_first_request
def activate_job():
    # pass
    start_publisher_subscriber_model()
    scheduler.add_job(start_streaming)
    scheduler.add_job(look_for_nots)
    # scheduler.add_job(send_alerts)
    # scheduler.add_job(look_for_nots)
    scheduler.start()

authController(server)
userController(server)
cryptoController(server)
stockController(server)
watchlistController(server)
adminController(server)
# notificationController(server)
technicalIndicactorsController(server)
alertController(server)

if __name__== "__main__":
    server.run(debug=True)