from middlewares.verifyJWT import verifyJWT
from flask import jsonify,request
from models.user import User
from middlewares.verifyRoles import verifyRole
from dotenv import load_dotenv
load_dotenv()
import os

def adminController(server):
    @server.route("/admin/users", methods=["GET"])
        # @verifyRole([os.getenv('ADMIN_ROLE')])
    # @verifyJWT
    def get_all_users():
        try:
            print('chekk')
            skip=request.args.get('skip')
            take=request.args.get('take')
            search_by=request.args.get('search_by')
            print('skip',skip)
            print('take',take)
            print('search_by',search_by)

            users=User().get_all(int(skip),int(take))
            # print('users',users)
            print('ji')
            userscount=User().get_total_count()
            # print('users',users)
            # print('userscount',userscount)

            if(users and userscount):
                print('gooo')
                print('users:-',users,'userscount:-',userscount)
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