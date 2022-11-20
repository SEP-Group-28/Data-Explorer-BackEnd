from models.technicalIndicator import TechnicalIndicator

def technicalIndicactorsController(server):

    #ROUTE TO GET THE RSI CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE OBV CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE ROC CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE EMA CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE MA CALCULATIONS USING TIMESTAMP(PAGINATION)
    @server.route('/ma/<market_type>/<market_name>/<interval>/<timestamp>/<datalimit>', methods=['GET'])
    def calculate_ma(market_type,market_name, interval,timestamp,datalimit):
        try:
            return TechnicalIndicator().calculate_ma(market_type,market_name, interval,timestamp,datalimit)
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    #ROUTE TO GET THE SMA CALCULATIONS USING TIMESTAMP(PAGINATION)
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
    #ROUTE TO GET THE WMA CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE STOCH CALCULATIONS USING TIMESTAMP(PAGINATION)
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
    #ROUTE TO GET THE BBANDS CALCULATIONS USING TIMESTAMP(PAGINATION)
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

    #ROUTE TO GET THE MACD CALCULATIONS USING TIMESTAMP(PAGINATION)
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
