from models.technicalIndicator import TechnicalIndicator
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request,Response
from models.user import User
from middlewares.verifyRoles import verifyRole

def technicalIndicactorsController(server):    
    @server.route('/rsi/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_rsi(market_type, market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_rsi(market_type, market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/obv/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_obv(market_type, market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_obv(market_type, market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/roc/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_roc(market_type,market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_roc(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/ema/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_ema(market_type,market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_ema(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/ma/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_ma(market_type,market_name, interval,timestamp,datalimit):
        try:
            print("Printing ",market_type,market_name, interval,timestamp,datalimit)
            return TechnicalIndicator().calculate_ma(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/sma/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_sma(market_type,market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_sma(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/wma/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def get_wma(market_type,market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_wma(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/stoch/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def get_stoch(market_type, market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_stoch(market_type, market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/bbands/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def get_bbands(market_type, market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_bbands(market_type, market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/macd/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def get_macd(market_type, market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_macd(market_type, market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500
