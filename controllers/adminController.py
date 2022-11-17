from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from middlewares.verifyRoles import verifyRole
import os

def adminController(server):  #Admin controller
    @server.route("/admin/users", methods=["GET"])  #Route for admin to get all users
    @verifyRole([os.getenv('ADMIN_ROLE')])
    @verifyJWT
    def get_all_users():  
        try:
            skip=request.args.get('skip')
            take=request.args.get('take')
            search_by=request.args.get('search_by')
            filter_by=request.args.get('filter_by')
            if (int(take) == -1):
                users, user_count=User().get_all_search(search_by, filter_by, int(skip), int(take)) #Get all users using pagination
                if(len(users) <= 0):
                    return {
                    "message": "No users found",
                    "data":{'users':users,'usercount':0}
                    }
                userscount=user_count
                if(users and userscount):
                    return {
                    "message": "successfully retrieved users",
                    "data":{'users':users,'usercount':userscount}
                    
                }
                return jsonify({
                    "message": "failed to get users",
                    "data": None
                }), 400
            else:
                users=User().get_all(int(skip),int(take))
                userscount=User().get_total_count()
                if(users and userscount):
                    return {
                    "message": "successfully retrieved users",
                    "data":{'users':users,'usercount':userscount}
                    
                }
                return jsonify({
                    "message": "failed to get users",
                    "data": None
                }), 400
        except Exception as e:
            print(e)
            return jsonify({
                "message": "failed to get users",
                "error": str(e),
                "data": None
        }), 400
