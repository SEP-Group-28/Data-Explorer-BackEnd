
from email import message
import queue
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
from pubsub.pubsubservices import subscribe_to_socket,get_history
load_dotenv()
import os
from models.market import Crypto


def cryptoController(server):
    @server.route('/history/<market>/<interval>',methods=['GET'])
    def take_history_data(market,interval):
        try:
            # data=request.json
            # if not data:
            #     return {
            #         "message": "Please provide crypto details",
            #         "data": None,
            #         "error": "Bad request"
            #     }, 400
            market=market+'/USDT'
            # cryptocurrency=Crypto(data['cryptoname'])
            # cryptoname= data['cryptoname']
            # interval=data['interval']
            # history_data=get_history(cryptoname,interval)
            cryptoname= market
            interval=interval
            history_data=get_history(cryptoname,interval)
            # if not historical_data:
            #     return
            # return historical_data
            # history_data=cryptocurrency.readHistory(data)
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

        

    @server.route('/present/<market>/<interval>',methods=['GET'])
    def take_present_data(market,interval):
        try:
            print('trying')
#print('Market',market)
#print('Interval',interval)
            market=market+'/USDT'
#print('newmarket',market)
            # data=request.json
            # if not data:
            #     return {
            #         "message": "Please provide crypto details",
            #         "data": None,
            #         "error": "Bad request"
            #     }, 400
            # cryptocurrency=Crypto('Crypto',data['cryptoname'])
            # cryptoname= data['cryptoname']
            # interval=data['interval']
            # cryptocurrency=Crypto('Crypto',market)
            cryptoname= market
#print('cryptoname',cryptoname)
            interval=interval
            def stream(cryptoname,interval):

                messages = subscribe_to_socket(cryptoname,interval) 
                print('messages',messages.get())
                while True:   
                    
                    msg = messages.get()
                    print('listened',interval,cryptoname,msg)
                    # encoded=str(msg).encode()
                    # print('encoded ',msg)
                    yield msg
            
            return Response(stream(cryptoname,interval), mimetype='text/event-stream')
            

            #main thread
            # cryptocurrency.callRecentHistory()

            #need to run in a diff thread
            
            
            #need to run in a diff thread
            # cryptocurrency.saveRealTimeData()

            #pub sub model
            # crypto_data=cryptocurrency.sendData(data)
            
            
        
        except Exception as e:
             return jsonify({
                "message": "failed to get live crypto details",
                "error": str(e),
                "data": None
        }), 400


    # @server.route('/getcrypto',methods=['GET'])
    # def get_crypto():
    #     try:
    #         # data=request.json
    #         # if not data:
    #         #     return {
    #         #         "message": "Please provide crypto details",
    #         #         "data": None,
    #         #         "error": "Bad request"
    #         #     }, 400 
    #         crypto=Crypto().getCrypto()
    #         if(crypto):
    #             return jsonify({
    #             "message": "successfully retrieved crypto",
    #             "data": crypto
    #         })
    #         return jsonify({
    #             "message": "failed to get crypto details",
    #             "data": None
    #     }), 400
    #     except Exception as e:
    #         return jsonify({
    #             "message": "failed to get crypto details",
    #             "error": str(e),
    #             "data": None
    #     }), 400

    @server.route('/getcryptolist',methods=['GET'])
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
            print(e)
            return jsonify({
                "message": "failed to get crypto list",
                "error": str(e),
                "data": None
        }), 400

           


        