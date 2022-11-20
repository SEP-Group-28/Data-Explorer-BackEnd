from flask import jsonify
from flask import request
import jwt
from functools import wraps
import os
from models.user import User


#VERIFY THE USER USING VERIFYJWT
def verifyJWT(f):
    try:
        @wraps(f)
        def decorated(*args, **kwargs):
            print("verifying....")
            authHeader=None
            if 'Authorization' in request.headers:
                authHeader=request.headers['Authorization']
            
            if not authHeader:
                return jsonify({'message': 'Authentication Token is missing!'}), 401

            if (not('Bearer ' in authHeader)) :
                print("in bearer if")
                return jsonify({
                    "message": "Unauthorized"
                }),401
    
            token = authHeader.split(' ')[1]
            print(token)
            if not token:
        
                return jsonify({
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }), 401
            try:
                decoded_data=jwt.decode(token,
                os.environ.get('ACCESS_TOKEN_SECRET'),algorithms=['HS256'])
           
                current_user=User().get_by_id(decoded_data['user_id'])
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
        
                
            return f(current_user, *args, **kwargs)
    
        return decorated
    except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500














