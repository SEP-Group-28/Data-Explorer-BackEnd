from models.technicalIndicator import TechnicalIndicator
# from pubsub.pubsubservices import listen_notifications,historical_nots
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole
# from dotenv import load_dotenv
import json

# load_dotenv()
import os



def technicalIndicactorsController(server):    
    @server.route('/rsi/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_rsi(market_type, market_name, interval):
        return TechnicalIndicator().calculate_rsi(market_type, market_name, interval)
        # return  generate_rsi(type_name, name, interval)


    @server.route('/obv/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_obv(market_type, market_name, interval):
        return TechnicalIndicator().calculate_obv(market_type, market_name, interval)


    @server.route('/roc/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_roc(market_type,market_name, interval):
        return TechnicalIndicator().calculate_roc(market_type,market_name, interval)


    @server.route('/ema/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_ema(market_type,market_name, interval):
        return TechnicalIndicator().calculate_ema(market_type,market_name, interval)


    @server.route('/ma/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_ma(market_type,market_name, interval):
        print("Printing ",market_type,market_name, interval)
        return TechnicalIndicator().calculate_ma(market_type,market_name, interval)


    @server.route('/sma/<market_type>/<market_name>/<interval>', methods=['GET'])
    def calculate_sma(market_type,market_name, interval):
        return TechnicalIndicator().calculate_sma(market_type,market_name, interval)


    @server.route('/wma/<market_type>/<market_name>/<interval>', methods=['GET'])
    def get_wma(market_type,market_name, interval):
        return TechnicalIndicator().calculate_wma(market_type,market_name, interval)


    @server.route('/stoch/<market_type>/<market_name>/<interval>', methods=['GET'])
    def get_stoch(market_type, market_name, interval):
        return TechnicalIndicator().calculate_stoch(market_type, market_name, interval)


    @server.route('/bbands/<market_type>/<market_name>/<interval>', methods=['GET'])
    def get_bbands(market_type, market_name, interval):
        return TechnicalIndicator().calculate_bbands(market_type, market_name, interval)


    @server.route('/macd/<market_type>/<market_name>/<interval>', methods=['GET'])
    def get_macd(market_type, market_name, interval):
        return TechnicalIndicator().calculate_macd(market_type, market_name, interval)
