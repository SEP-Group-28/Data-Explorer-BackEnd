from flask import Blueprint, request
import json

from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os

def watchlistController(server):
    @server.route('/removemarket', methods=['DELETE'])
    @verifyJWT
    def removemarket(current_user):
        pass
    
        # return remove_from_watch_list(current_user['email'], data['brands'])

    @server.route('/addmarket', methods=['POST'])
    @verifyJWT
    def addmarket(current_user):
        data = json.loads(request.data, strict=False)
        print(data['brands'])
        # return add_stock_to_watch_list(current_user['email'], data['brands'])


    @server.route('/viewwatchlist', methods=['GET'])
    @verifyJWT
    def viewwatchlist(current_user):
        return
        return view_watch_list(current_user['email'])

   

    


    




