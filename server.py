from datetime import datetime
from controllers.alertController import alertController
from controllers.technicalIndicactorsController import technicalIndicactorsController
from Binance.websocketCall import start_streaming,restart_binance_connection
from controllers.watchlistController import watchlistController
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid  import ObjectId
import os

from controllers.authController import authController
from controllers.userController import userController
from config.allowedOrigins import allowedOrigins
from controllers.cryptoController import cryptoController
from controllers.stockController import stockController
from controllers.adminController import adminController
from controllers.technicalIndicactorsController import technicalIndicactorsController
from controllers.notificationController import notificationController
from apscheduler.schedulers.background import BackgroundScheduler


from pubsub.pubsubservices import start_publisher_subscriber_model,look_for_nots

def server_intialize():
    server = Flask(__name__)
    CORS(server,supports_credentials=True,origins=allowedOrigins)
    scheduler = BackgroundScheduler()

    @server.before_first_request
    def activate_job():
        start_publisher_subscriber_model()
        scheduler.add_job(start_streaming)
        scheduler.add_job(restart_binance_connection)
        scheduler.start()

    authController(server)
    userController(server)
    cryptoController(server)
    stockController(server)
    watchlistController(server)
    adminController(server)
    notificationController(server)
    technicalIndicactorsController(server)
    alertController(server)

    return server


