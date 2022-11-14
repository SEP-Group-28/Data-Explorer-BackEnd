
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from middlewares.verifyRoles import verifyRole
# from dotenv import load_dotenv
from models.market import Stock
import json

# load_dotenv()
import os


def stockController(server):
    @server.route('/stockhistory/<stock>/<interval>',methods=['GET'])
    def seed_history(stock,interval):
        print("Arrived............",stock)
        stockdata = Stock().getStockDataList(stock, interval)
        print("hellllllo")
        json_format_stock_data = json.dumps(stockdata)
        return json_format_stock_data

    @server.route('/stockhistory/<stock>/<interval>/<timestamp>/<datalimit>',methods=['GET'])
    def take_stock_history_data_timestamp(stock,interval,timestamp,datalimit):
        stockdata = Stock().getStockDataListTimestamp(stock, interval,timestamp,datalimit)
        # print(stockdata)
        json_format_stock_data = json.dumps(stockdata)
        return json_format_stock_data

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
