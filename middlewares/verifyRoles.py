
from flask import jsonify
from flask import request,abort
import jwt
from functools import wraps
# from dotenv import load_dotenv
# load_dotenv()
import os
import models
import utils.token as token

def verifyRole(*allowedRoles):
    try:
        def decorated(f):
            @wraps(f)
            def wrapper(*args,**kwargs):
                if not(request['user_id']):
                    return jsonify({
                        
                    "message": "User id is missing."
                    }),401
                userRole = request['role']
                isAllow=False
                if(userRole in allowedRoles):
                    isAllow=True

    #print("allowedRoles", allowedRoles)
    #print("user role", userRole)
                if not(isAllow):
    #print("not allowed role")
                    return jsonify({
                    "message": "Unauthorized request user not allowed"
                }),401
            
                return f( *args, **kwargs)
                
            return wrapper
        return decorated
    except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500
