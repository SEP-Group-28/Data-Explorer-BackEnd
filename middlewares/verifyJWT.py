
from flask import jsonify
from flask import request
import jwt
from functools import wraps
# from dotenv import load_dotenv
# load_dotenv()
import os
from models.user import User
# import utils.token as token
def verifyJWT(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("verifying....")

#print('JWT verification...')

        # authHeader = request.headers['authorization'] or request.headers['Authorization']
        authHeader=request.headers['Authorization']
#print('authHeader', authHeader)


        if (not('Bearer ' in authHeader)) :
            print("in bearer if")
#print('Invalid token VERIFYJWT : ', authHeader)
            return jsonify({
                "message": "Unauthorized"
            }),401
   
        # print("out from bearer if")
        token = authHeader.split(' ')[1]
        if not token:
            # print("unauthorized")
            return jsonify({
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }), 401
#print(os.getenv('ACCESS_TOKEN_SECRET'))
        # print("out from token if")
        # print("token", token)
        try:
            # print("access token, ", os.getenv('ACCESS_TOKEN_SECRET'))
            decoded_data=jwt.decode(token,
            os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
            
            # print(decoded_data)
            # print("decoded data", [decoded_data["user_id"]])
            current_user=User().get_by_id(decoded_data['user_id'])
            # print("user", current_user)
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        except Exception as e:
            print("exception", e)
            return jsonify({
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }),403
        
#print('JWT verified...')
#print("decoded :", decoded_data)
       
             
        return f(current_user, *args, **kwargs)
  
    return decorated














