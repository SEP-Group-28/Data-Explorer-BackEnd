
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
    try:
        @wraps(f)
        def decorated(*args, **kwargs):
            print("verifying....")
            authHeader=None
    #print('JWT verification...')
            # print(request.headers)
            # authHeader = request.headers['authorization'] or request.headers['Authorization']
            if 'Authorization' in request.headers:
                authHeader=request.headers['Authorization']
            
            if not authHeader:
                return jsonify({'message': 'Authentication Token is missing!'}), 401
    #print('authHeader', authHeader)


            if (not('Bearer ' in authHeader)) :
                print("in bearer if")
    #print('Invalid token VERIFYJWT : ', authHeader)
                return jsonify({
                    "message": "Unauthorized"
                }),401
    
            # print("out from bearer if")
            token = authHeader.split(' ')[1]
            print(token)
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
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": str(e)
                }),401
            
    #print('JWT verified...')
    #print("decoded :", decoded_data)
        
                
            return f(current_user, *args, **kwargs)
    
        return decorated
    except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500














