from urllib.request import Request
from flask import Blueprint, request
import json
from models.watchlist import Watchlist
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from middlewares.verifyRoles import verifyRole
# from dotenv import load_dotenv
# load_dotenv()
import os

def watchlistController(server):
    @server.route('/remove-market', methods=['DELETE'])
    @verifyJWT
    def removemarket(current_user):
        try:
            data=json.loads(request.data)
            print("data remove market", data)
            id=current_user["_id"]
            print("user id", id)
            crypto=data['crypto']
            watchlistmodel=Watchlist()
            watchlist=watchlistmodel.getwatchlist(id)
            print("watchlist remove ", watchlist)
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
                        "data":False
                    },400


        except Exception as e:
            print(e)
            return {
                        "message": "Remove crypto from watchlist fail",
                        "data":None,
                        "error":str(e)
                    },400


        

    
        # return remove_from_watch_list(current_user['email'], data['brands'])

    @server.route('/add-market', methods=['POST'])
    @verifyJWT
    def addmarket(current_user):
        try:
            print("add market data....")
            data=json.loads(request.data)
            print(data)
            id=current_user["_id"]
            crypto=data['crypto']
            watchlistmodel=Watchlist()
            watchlist=watchlistmodel.getwatchlist(id)
            print("watchlist", watchlist)
            if not(watchlist):
                print("if not watchlist")
                watchlistmodel.createwatchlist(id)
                watchlist=watchlistmodel.getwatchlist(id)
                print("created watchlist", watchlist)
                # watchlist=getresult['list']
            if crypto not in watchlist:
                watchlist.append(crypto)
                print("watchlist append", watchlist)
                updateResult = watchlistmodel.updatewatchlist(id,watchlist)
                print("getting watchlist")
                if (updateResult):
                    updatedwatchlist=watchlistmodel.getwatchlist(id)
                    print("updateed watchlist", updatedwatchlist)
                    if(updatedwatchlist):
                        return {
                        "message": "Successfully added to watchlist",
                        "data": updatedwatchlist
                        },200
                    return {
                    "message": "Adding to watchlist fail",
                    "data":None
                    },400
                return {
                    "message": "Adding to watchlist fail",
                    "data":None
                    },400
                # print("Get watchlist crypto", watchlistmodel.getwatchlist(id))    
            return {
                    "message": "Crypto type already added",
                    "data":watchlist
                },200

        except Exception as e:
            print(e)
            return {
                        "message": "Adding to watchlist fail",
                        "data":None,
                        "error":str(e)
                    },400


    @server.route('/view-watchlist', methods=['GET'])
    @verifyJWT
    def viewwatchlist(current_user):
        try:
            print(current_user)
            
            # data=request.form
            # print(data)
            id=current_user["_id"]
            # crypto=data['crypto']
            watchlistmodel=Watchlist()
            try:
                getresult=watchlistmodel.getwatchlist(id)
                if getresult :
                    return {
                            "message": "Successfully get watchlist",
                            "data": getresult
                        },200
                else:
                    return {
                                "message": "Watchlist is empty",
                                "data": getresult
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
   

    


    




