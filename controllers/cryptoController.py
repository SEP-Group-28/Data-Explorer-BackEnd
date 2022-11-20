from flask import jsonify,Response
from pubsub.pubsubservices import subscribe_to_socket_for_real_time_crypto,get_history_for_crypto,get_history_for_crypto_timestamp
import os
from models.market import Crypto


def cryptoController(server):
    @server.route('/history/<market>/<interval>',methods=['GET']) #ROUTE TO GET HISTORICAL DATA
    def take_history_data(market,interval):
        try:
            market=market+'/USDT'
            cryptoname= market
            interval=interval
            history_data=get_history_for_crypto(cryptoname,interval)
            if(history_data):
                    return jsonify({
                    "message": "successfully retrieved history details",
                    "data": history_data
                })
            return jsonify({
                    "message": "failed to get history details",
                    "data": None
            }), 400

        except Exception as e:
            return jsonify({
                "message": "failed to get history details",
                "error": str(e),
                "data": None
        }), 400

        

    @server.route('/present/<market>/<interval>',methods=['GET']) #ROUTE TO GET CURRENT REAL TIME DATA FROM SOCKET
    def take_present_data(market,interval):
        try: 
            print('present')
            market=market+'/USDT'
            cryptoname= market
            interval=interval
            def stream(cryptoname,interval):
                messages = subscribe_to_socket_for_real_time_crypto(cryptoname,interval) 
                while True:   
                    msg = messages.get()
                    print("messeage", msg)
                    yield msg
            
            return Response(stream(cryptoname,interval), mimetype='text/event-stream') #sending multipurpose internet mail extension with a type and subtype   
        except Exception as e:
             return jsonify({
                "message": "failed to get live crypto details",
                "error": str(e),
                "data": None
        }), 400


    @server.route('/getcryptolist',methods=['GET']) #ROUTE TO GET ALL CRYPTO CURRENCIES AS A LIST
    def get_crypto_list():
        try:
            crypto_list=Crypto().getCryptoListFromMarket()
            if(crypto_list):
                return jsonify({
                "message": "successfully retrieved crypto list",
                "data": crypto_list['list']
            })
            return jsonify({
                "message": "failed to get crypto list",
                "data": None
        }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to get crypto list",
                "error": str(e),
                "data": None
        }), 400
    
    @server.route('/',methods=['GET'])
    def home():
        return "Welcome to Crypto API"


    @server.route('/history/<market>/<interval>/<timestamp>/<datalimit>',methods=['GET']) #ROUTE TO GET HISTORICAL DATA USING TIME STAMP
    def take_history_data_timestamp(market,interval,timestamp,datalimit):
        try:
            market=market+'/USDT'
            cryptoname= market
            interval=interval
            history_data=get_history_for_crypto_timestamp(cryptoname,interval,timestamp,datalimit)
            if(history_data):
                    return jsonify({
                    "message": "successfully retrieved history details",
                    "data": history_data
                })
            return jsonify({
                    "message": "failed to get history details",
                    "data": None
            }), 400

        except Exception as e:
            return jsonify({
                "message": "failed to get history details",
                "error": str(e),
                "data": None
        }), 400


           


        