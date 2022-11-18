
from middlewares.verifyJWT import verifyJWT
from flask import jsonify
from middlewares.verifyRoles import verifyRole
from models.market import Stock
import json


def stockController(server):
    @server.route('/stockhistory/<stock>/<interval>',methods=['GET'])
    def seed_history(stock,interval):
        try:
            print("Arrived............",stock)
            stockdata = Stock().getStockDataList(stock, interval)
            print("hellllllo")
            json_format_stock_data = json.dumps(stockdata)
            return json_format_stock_data
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/stockhistory/<stock>/<interval>/<timestamp>/<datalimit>',methods=['GET'])
    def take_stock_history_data_timestamp(stock,interval,timestamp,datalimit):
        try:
            stockdata = Stock().getStockDataListTimestamp(stock, interval,timestamp,datalimit)
            # print(stockdata)
            json_format_stock_data = json.dumps(stockdata)
            return json_format_stock_data
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    @server.route('/getstocklist',methods=['GET'])
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

    # @server.route('/getstock',methods=['GET'])
    # def get_stock():
    #     try:
    #         stock=Stock().getStock()
    #         if(stock):
    #             return jsonify({
    #             "message": "successfully retrieved stock ",
    #             "data": stock
    #         })
    #         return jsonify({
    #             "message": "failed to get stock",
    #             "data": None
    #     }), 400
    #     except Exception as e:
    #         return jsonify({
    #             "message": "failed to get stock",
    #             "error": str(e),
    #             "data": None
    #     }), 400
