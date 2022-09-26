
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.models import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os
from models.market import crypto


def cryptoController(server):
    @server.route('/history/<cryptoname>',methods=['GET'])
    def see_history(cryptoname):
        data=request.json
        if not data:
            return {
                "message": "Please provide crypto details",
                "data": None,
                "error": "Bad request"
            }, 400
        cryptocurrency=crypto('Crypto',cryptoname)
        history_data=cryptocurrency.readHistory(data)

    @server.route('/data',methods=['GET'])
    def take_data():
        try:
            data=request.json
            if not data:
                return {
                    "message": "Please provide crypto details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            cryptocurrency=crypto('Crypto',data['cryptoname'])
            #main thread
            # cryptocurrency.callRecentHistory()

            #need to run in a diff thread
            
            return cryptocurrency.takeData(data)
            #need to run in a diff thread
            cryptocurrency.saveRealTimeData()

            #pub sub model
            # crypto_data=cryptocurrency.sendData(data)
            
            
            
        
        except Exception as e:
            print (e)

