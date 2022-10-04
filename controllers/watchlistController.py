from flask import Blueprint, request
import json
from models.watchlist import Watchlist
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os

def watchlistController(server):
    @server.route('/removemarket', methods=['DELETE'])
    # @verifyJWT
    def removemarket(current_user):
        try:
            data=request.json
            print(data)
            id=current_user["_id"]
            crypto=data['crypto']
            watchlistmodel=Watchlist()
            watchlist=watchlistmodel.getwatchlist(id)
            if(watchlist):
                # watchlist=getresult['list']
                if crypto in watchlist:
                    watchlist.remove(crypto)
            
                    updateresult=watchlistmodel.updatewatchlist(id,watchlist)
                    if(updateresult):
                        updatedwatchlist=watchlistmodel.getwatchlist(id)
                        return {
                        "message": "Successfully remove crypto from watchlist",
                        "data": updatedwatchlist
                        },200
                    else:
                        return {
                                    "message": "Watchlist is empty",
                                    "data": None
                                },200
               
                return {
                        "message": "Remove crypto from watchlist fail",
                        "data":None
                    },400
            return {
                        "message": "No watchlist for this user",
                        "data":None
                    },400


        except Exception as e:
            print(e)
            return {
                        "message": "Remove crypto from watchlist fail",
                        "data":None,
                        "error":str(e)
                    },400


        

    
        # return remove_from_watch_list(current_user['email'], data['brands'])

    @server.route('/addmarket', methods=['POST'])
    # @verifyJWT
    def addmarket(current_user):
        try:
            data=request.json
            print(data)
            id=current_user["_id"]
            crypto=data['crypto']
            watchlistmodel=Watchlist()
            watchlist=watchlistmodel.getwatchlist(id)
            if not(watchlist):
                watchlistmodel.createwatchlist(id)
                watchlist=watchlistmodel.getwatchlist(id)
                # watchlist=getresult['list']
            if crypto not in watchlist:
                watchlist.append(crypto)
                updateresult=watchlistmodel.updatewatchlist(id,watchlist)
                if(updateresult):
                        updatedwatchlist=watchlistmodel.getwatchlist(id)
                        return {
                        "message": "Successfully updated watchlist",
                        "data": updatedwatchlist
                    },200
            return {
                    "message": "Update watchlist fail",
                    "data":None
                },400

        except Exception as e:
            print(e)
            return {
                        "message": "Update watchlist fail",
                        "data":None,
                        "error":str(e)
                    },400


    @server.route('/viewwatchlist', methods=['GET'])
    # @verifyJWT
    def viewwatchlist(current_user):
        try:
            data=request.json
            print(data)
            id=current_user["_id"]
            crypto=data['crypto']
            watchlistmodel=Watchlist()
            try:
                getresult=watchlistmodel.getwatchlist(id)
                if getresult :
                    return {
                            "message": "Successfully get watchlist",
                            "data": getresult['list']
                        },200
                else:
                    return {
                                "message": "Watchlist is empty",
                                "data": None
                            },200
            except Exception as e:
                print(e)
                return {
                                "message": "Watchlist get fail",
                                "data": None
                            },200
            
        except Exception as e:
            print(e)
            return {
                        "message": "Watchlist get fail",
                        "data":None,
                        "error":str(e)
                    },400
   

    


    




