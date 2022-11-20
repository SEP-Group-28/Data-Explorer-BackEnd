from controllers.alertController import alertController
from controllers.technicalIndicactorsController import technicalIndicactorsController
from Binance.websocketCall import start_streaming,restart_binance_connection
from controllers.watchlistController import watchlistController
from flask import Flask
from flask_cors import CORS
from controllers.authController import authController
from controllers.userController import userController
from config.allowedOrigins import allowedOrigins
from controllers.cryptoController import cryptoController
from controllers.stockController import stockController
from controllers.adminController import adminController
from controllers.technicalIndicactorsController import technicalIndicactorsController
from controllers.notificationController import notificationController
from apscheduler.schedulers.background import BackgroundScheduler
from pubsub.pubsubservices import start_publisher_subscriber_model
from pubsub.pubsubservices import start_sending_notifications


def server_intialize():

    server = Flask(__name__) #INITIALIZE THE SERVER
    CORS(server, supports_credentials=True,origins=allowedOrigins, allow_headers=['Content-Type', 'Authorization']) #ACCEPT ONLY THE ALLOWED ORIGINS FOR CORS ERROS
    scheduler = BackgroundScheduler() #INTIALIZE THE BACKGROUND SCHEDULER

    @server.before_first_request #WAIT TO GET THE FIRST REQUEST FROM FRONTEND
    def activate_job():
        start_publisher_subscriber_model() #START THE PUBLISHER SUBSCRIBER MODEL
        scheduler.add_job(start_streaming) #CONNECT TO BINANCE WEBSOCKET AND THEN START THE STREAMING 
        scheduler.add_job(start_sending_notifications) #LOOK FOR NOTIFICATIONS TO SEND TO THE FRONTEND
        scheduler.add_job(restart_binance_connection) #IF WEBSOCKET GET DISCONNECTED RESTART THE CONNECTION
        scheduler.start() #START ALL THREADS
 
    authController(server) #ROUTES
    userController(server) 
    cryptoController(server)
    stockController(server)
    watchlistController(server)
    adminController(server)
    notificationController(server)
    technicalIndicactorsController(server)
    alertController(server)
    return server


