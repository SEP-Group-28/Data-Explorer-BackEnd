from flask import jsonify
from models.market import Stock
import json

def stockController(server):
    @server.route('/stockhistory/<stock>/<interval>',methods=['GET']) #ROUTE TO VIEW HISTORICAL STOCKS USING INTERVAL
    def seed_history(stock,interval):
        try:
            stockdata = Stock().getStockDataList(stock, interval)
            json_format_stock_data = json.dumps(stockdata)
            return json_format_stock_data
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/stockhistory/<stock>/<interval>/<timestamp>/<datalimit>',methods=['GET']) #ROUTE TO VIEW HISTORICAL STOCKS USING TIMESTAMP PAGINATION
    def take_stock_history_data_timestamp(stock,interval,timestamp,datalimit):
        try:
            stockdata = Stock().getStockDataListTimestamp(stock, interval,timestamp,datalimit)
            json_format_stock_data = json.dumps(stockdata)
            return json_format_stock_data
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/getstocklist',methods=['GET']) #ROUTE TO GET ALL STOCKS AVAILABLE AS A LIST
    def get_stock_list():
        try:
            stock_list=Stock().getStockListFromMarket()
            if(stock_list):
                return jsonify({
                "message": "successfully retrieved stock list",
                "data": stock_list['list']
            })
            return jsonify({
                
                "message": "failed to get stock list",
                "data": None
            }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to get stock list",
                "error": str(e),
                "data": None
        }), 400

