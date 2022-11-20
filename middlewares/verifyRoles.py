
import json
from flask import jsonify
from flask import request
from functools import wraps


#GIVE AUTHENTICATION FOR USER TO RELAVANT ROUTES
def verifyRole(*allowedRoles):
    try:
        def decorated(f):
            @wraps(f)
            def wrapper(*args,**kwargs):
                request1 = request.data 
                print("request1",request1)
                if not(request1['user_id']):
                    return jsonify({
                        
                    "message": "User id is missing."
                    }),401
                userRole = request1['role']
                isAllow=False
                if(userRole in allowedRoles):
                    isAllow=True
                if not(isAllow):
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
