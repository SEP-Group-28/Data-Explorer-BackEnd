
from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.models import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os

def userControllers(server):
    @server.route("/user/<id>", methods=["GET"])
    @verifyRole([os.getenv('USER_ROLE')])
    @verifyJWT
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
    
    

    @server.route("/user/<id>", methods=["PUT"])
    @verifyRole([os.getenv('USER_ROLE')])
    @verifyJWT
    def update_user(id):
        try:
            user = request.json
            # if user.get("name"):
            user = User().update(id, user)
            if(user):
                return jsonify({
                    "message": "successfully updated account",
                    "data": user
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
    @server.route("/admin/users", methods=["GET"])
    @verifyRole([os.getenv('ADMIN_ROLE')])
    @verifyJWT
    def get_all_users():
        try:
            user=User().get_all
            if(user):
                return jsonify({
                "message": "successfully retrieved users",
                "data": user
            })
            return jsonify({
                "message": "failed to get users",
                "data": None
        }), 400
        except Exception as e:
            return jsonify({
                "message": "failed to get users",
                "error": str(e),
                "data": None
        }), 400
