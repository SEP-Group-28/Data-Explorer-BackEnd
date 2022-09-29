
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
from models.market import Stock
import json

load_dotenv()
import os


def stockController(server):
    @server.route('/history/<stock>/<interval>',methods=['GET'])
    def seed_history(stock,interval):
        stockdata = Stock().getStockDataList(stock, interval)
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
