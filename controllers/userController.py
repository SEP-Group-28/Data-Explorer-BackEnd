
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from io import BufferedReader
from werkzeug.security import check_password_hash
from models.watchlist import Watchlist

def userController(server):
    @server.route("/api/user/<id>", methods=["GET"]) #ROUTE TO GET THE DETAILS OF USER INCLUDING WATCHLIST
    @verifyJWT
    def get_current_user(id):
        try:
            user=User().get_by_id(id)
            if(user):
                user_watchlist = Watchlist().getwatchlist(id)
                if not(user_watchlist):
                    user_watchlist = []
                user['watchlist'] = user_watchlist
                return jsonify({
                "message": "successfully retrieved user profile",
                "data": user
            })
            return jsonify({
                "message": "failed to get account details",
                "data": None
        }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to get account details",
                "error": str(e),
                "data": None
        }), 400
    
    

    @server.route("/api/user/update-profile/<id>", methods=["POST"]) #ROUTE TO UPDATE THE PROFILE OF USER
    @verifyJWT
    def update_user(id):
        try:
            data = request.json
            userdata = User().update(id, data)
            if(userdata):
                return jsonify({
                    "message": "successfully updated account",
                    "data": userdata
                }), 201
            return jsonify({
                "message": "failed to update account",
                "error": str(e),
                "data": None
        }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to update account",
                "error": str(e),
                "data": None
        }), 400
    
   
    @server.route("/api/user/update-photo/<id>", methods=["POST"]) #ROUTE TO UPDATE THE PROFILE PHOTO OF USER USING CLODUINARY
    @verifyJWT
    def update_user_photo(id):
        try:
            rquest=request
            photodetails=request.files.get('Image')
            photodetails.name=photodetails.filename
            photodetails=BufferedReader(photodetails)
            if not photodetails:
                return {
                    "message": "Please provide image details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            
            upload_result=User().update_photo(photodetails) 
            if len(upload_result)!=0:
                user_id=User().update(id,{'imagepath':upload_result['url']})
                if(user_id):
                    return jsonify({
                    "message": "successfully updated profile picture",
                    "data": user_id
                })
                return jsonify({
                    'message':"failed to upload",
                    'data':None
                })
            return jsonify({
                "message": "failed to update photo",
                "data": None
        }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to update photo",
                "error": str(e),
                "data": None
        }), 400


    @server.route('/api/user/change-active',methods=['POST']) #ROUTE TO CHANGE THE ACTIVATION OF THE USER
    def changeactive():
        try:
            data=request.json
            userid=data['user_id']
            userdetails=User().get_by_id(userid)
            if not(userdetails):
                 return {
                    'message':"failed to change activation",
                    'data':None
                },404
            result=User().changeactivation(userid,userdetails)
            return {
                    'message':"Successfully changed activation",
                    'data':result
                },200

        except Exception as e:
            return jsonify({
                "message": "failed to change activation",
                "error": str(e),
                "data": None
        }), 400


    @server.route('/api/user/update-password-by-user',methods=['POST']) #ROUTE TO UPDATE THE PASSWORD OF THE USER
    def updatpasswordbyuser():
        try:
            data=request.json
            new_password=data['new_password']
            old_password=data['old_password']
            user_id=data['user_id']
            user_model=User()
            password=user_model.get_password_by_id(user_id)
            if not(password):
                return {
                'message':"failed to change password",
                'data':None
            },404
            password_match=check_password_hash(password,old_password)
            if(password_match==False):
                return {
                'message':"Entered Old password is incorrect",
                'data':None
            },404
            encrypted_password=user_model.encrypt_password(new_password)
            user=user_model.update(user_id,{'password':encrypted_password})
            if (user):
                return {
                'message':"Password update successfully",
                'data':None
            },200
            return {
                'message':"Password update failed",
                'data':None
            },500

        except Exception as e:
             return {
                'message':"Password update failed",
                'data': e
            },500

