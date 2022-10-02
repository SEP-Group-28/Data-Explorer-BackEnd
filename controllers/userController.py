
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
from io import BufferedReader
load_dotenv()
import os

def userController(server):
    @server.route("/api/user/<id>", methods=["GET"])
    # @verifyRole([os.getenv('USER_ROLE')])
    # @verifyJWT
    def get_current_user(id):
        try:
            user=User().get_by_id(id)
            if(user):
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
    
    

    @server.route("/api/user/update-profile/<id>", methods=["POST"])
    # @verifyRole([os.getenv('USER_ROLE')])
    # @verifyJWT
    def update_user(id):
        try:
            data = request.json
            print(data)
    
            # if user.get("name"):
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
            # return {
            #     "message": "Invalid data, you can only update your account name!",
            #     "data": None,
            #     "error": "Bad Request"
            # }, 400
        except Exception as e:
            return jsonify({
                "message": "failed to update account",
                "error": str(e),
                "data": None
        }), 400
    
    # @server.route("/user/<id>", methods=["DELETE"])
    # @verifyJWT
    # def disable_user(id):
    #     try:
    #         User().disable_account(id)
    #         return jsonify({
    #             "message": "successfully disabled acount",
    #             "data": None
    #         }), 204
    #     except Exception as e:
    #         return jsonify({
    #             "message": "failed to disable account",
    #             "error": str(e),
    #             "data": None
    #         }), 400
   
    @server.route("/api/user/update-photo/<id>", methods=["POST"])
    # @verifyRole([os.getenv('ADMIN_ROLE')])
    # @verifyJWT
    def update_user_photo(id):
        try:
            print('susafsaff')
            rquest=request
            print('request',request)
            photodetails=request.files.get('Image')
            print('filename :::',photodetails.filename)
            photodetails.name=photodetails.filename
            photodetails=BufferedReader(photodetails)
            print('photo',photodetails)
        
            if not photodetails:
                return {
                    "message": "Please provide image details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            
            upload_result=User().update_photo(photodetails)
            print('success',upload_result)
            if len(upload_result)!=0:
                print('hi',upload_result['url'])
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

    @server.route('/api/user/change-active',methods=['POST'])
    def changeactive():
        try:
            data=request.json
            print(data)
            userid=data['user_id']
            userdetails=User().get_by_id(userid)
            if not(userdetails):
                 return {
                    'message':"failed to change activation",
                    'data':None
                },404
            result=User().changeactivation(userid,userdetails)
            print('result',result)
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
            print(e)
