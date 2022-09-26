
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.models import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os


def stockController(server):
    @server.route('/history/<stock>',methods=['GET'])
    def seed_history():
        data=request.json


    @server.route('/data/<stock>',methods=['GET'])
    def data_take():
        try:
            data=request.json
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
        
        except Exception as e:
            print (e)