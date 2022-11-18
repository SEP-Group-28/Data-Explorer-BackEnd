
from flask import request,jsonify,make_response
from bson.objectid  import ObjectId
import json
import jwt
import os
import utils.token as token
from models.user import User
from utils.validate import validate_user,validate_email_and_password
from middlewares.verifyJWT import verifyJWT
from dbconnection import connectdb as db
user_collection=db().user


def authController(server):
    @server.route("/auth/login",methods=["POST"])
    def login():
        try:
            print('helllo')
            data = json.loads(request.data) 
            try:
                if not data or not data['email'] or not data['password']:
                    return make_response(jsonify({'message': 'All fields are required for logging in'}), 400)
            except:
                return make_response(jsonify({'message': 'All fields are required for logging in'}), 400)
            print(data)
            is_validated = validate_email_and_password(data.get('email'), data.get('password'))
            print(is_validated)
            print('hi.......')
            if is_validated is not True:
                print('validating')
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user = User().login(
                data["email"],
                data["password"]
            )
            if user=='wrong_email':
                return { "message": "Email does not exist...".format(email=data['email'])},404
            if user=='wrong_password':
                return { "message": "Password is incorrect..." },401
            
            if user:
                try:
                    if user['role'] == '1':
                        authObject= {
                        "id": user['_id'],
                        "role":os.environ.get('USER_ROLE'),
                        }
                        print('1 is okay')
                    elif user['role'] == '2':
                        authObject= {
                        "id": user['_id'],
                        "role":os.environ.get('ADMIN_ROLE'),
                        }
                    print(os.environ)
                    print(user['role'])
                    print(authObject)
                    access_token=token.getAccessToken(authObject)
                    print('access')
                    refresh_token=token.getRefreshToken(authObject)
                    
                    print('check')
                    result=User().update(ObjectId(user['_id']),{'refresh_token':refresh_token})
                    print('result')
                    response= make_response({
                        "message": "Login successful",
                        "access_token": access_token,
                        
                    },200)
                    print(response)
                    response.set_cookie('jwt',refresh_token, httponly=True,max_age= 24 * 60 * 60 * 1000,secure=True, samesite='None')

                    return response
                except Exception as e:
                    return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
            return{
            "message": "Error fetching auth token!, invalid email or password",
            "data": str(data),
            "error": "Unauthorized"
        }, 404
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

        

    @server.route("/auth/register",methods=["POST"])
    def register():
        try:
            user=json.loads(request.data)
            print(user)
            
           
            if not user:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            
            is_validated = validate_user(**user)
            print(is_validated)
            if is_validated is not True:
               
                return jsonify(message='Invalid data', data=None, error=is_validated), 400
            user['role'] = '1'  # 1 for normal user
            userModel = User().create(**user)
            print(userModel)
            print("userModel",userModel)

            if(userModel=='duplicateuser'):
                return {"message": "Email already exists...".format(email=user['email'])},409
            return {
            "message": "Successfully created new user",
            "data": userModel
                    }, 201
            
        except Exception as e:
            return jsonify({ "message": "Internal server error","status":500 })
            

    @server.route('/auth/new-token',methods=['GET','POST'])
    def newaccesstoken():
        try:
            cookies = request.cookies
            print("here is my cookie bro",cookies)

            if not(cookies['jwt']) :


                return jsonify({ "message": "Invalid token" ,"status":401})
            

            refresh_token = cookies['jwt']
            print("hey hey here is the refresh token",refresh_token)
            auth= User().get_by_refreshtoken(refresh_token)

            if not(auth) :
                return jsonify({ "message": "Invalid token" ,"status":403})

            authObject= {
                "id": str(auth['_id']),
                "role":auth['role'],
            }
            try:
                decoded=jwt.decode(
                    refresh_token,
                    os.environ.get('REFRESH_TOKEN_SECRET') ,algorithms=['HS256'])
                if(auth['_id'] != decoded['user_id']):
                    return jsonify({ "message": "Invalid token" ,"status":403})
                access_token=token.getAccessToken(authObject)
            except jwt.exceptions.ExpiredSignatureError:
                return jsonify({ "message": "Invalid token" ,"status":403})
        

            return jsonify({
                        "message": "Refresh token successful",
                        "access_token": access_token,
                        "status":200})
        except Exception as e:
            return make_response(jsonify({
            "message": "Error when update refresh token",
            "data":e,
        }),404)
        

    @server.route("/auth/logout",methods=['GET',"POST"])
    def logout():

        try:
            cookies = request.cookies
            if not(cookies['jwt']):
                return jsonify({ "message": "No token found" ,"status":204})
            

            refresh_token = cookies['jwt']

            auth = user_collection.find_one({
                'refresh_token':refresh_token
            })

            if not(auth) :
                return jsonify({ "message": "User does not exist..." ,"status":404})
            

            result =user_collection.update_one({'_id':ObjectId(auth['_id'])},{'$set' :{
                'refresh_token':''
            }})
            response= make_response(jsonify({
                "message": "Logout successful",

                
            }),200)
            response.set_cookie('jwt','')
        except Exception as e:
            return make_response(jsonify({
            "message": "Error when logout",
            "data":e

        }),404)
        return response

    @server.route("/auth/test",methods=['GET',"POST"])
    @verifyJWT
    def get_test(current_user):
        try:
            print(current_user)
            return make_response(jsonify({'message': 'OK'}), 200)
        except Exception as e:
            return make_response(jsonify({
            "message": "Error while testing",
            "data":e

        }),404)
        


