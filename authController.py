
from flask import request,jsonify,make_response
from bson.objectid  import ObjectId
import bcrypt
from dotenv import load_dotenv
load_dotenv()
import jwt
import os
import utils.token as token
from models import User
from utils.validate import validate_user,validate_email_and_password
def authControllers(server):
    
    @server.route("/auth/login",methods=["POST"])
    def login():
        try:
            data = request.json
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            is_validated = validate_email_and_password(data.get('email'), data.get('password'))
            # form_data=request.form
            # Email= form_data['Email']
            # Password=form_data['Password']
            if is_validated is not True:
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user = User().login(
                data["email"],
                data["password"]
            )
            if user=='wrong_email':
                return jsonify({ "message": "Email :${email} does not exist...".format(email=data['email'])}),404
            if user=='wrong_password':
                return jsonify({ "message": "Password is incorrect..." }),400

            if user:
                try:
                    authObject= {
                    "id": user['_id'],
                    "role":os.getenv('USER_ROLE'),
                    }
                    access_token=token.getAccessToken(authObject)
                    refresh_token=token.getRefreshToken(authObject)
                    
                    print(refresh_token)
                   
                    # result =user_collection.update_one({'_id':ObjectId(auth['_id'])},{'$set' :{
                    # 'refresh_token':refresh_token
                    # }})
                    result=User().update(ObjectId(user['_id']),{'refresh_token':refresh_token})
                    print(result)
                    response= make_response(jsonify({
                        "message": "Login successful",
                        "access_token": access_token,
                        
                    }),200)
                    response.set_cookie('jwt',refresh_token)
                    print(response)
                    return response
                except Exception as e:
                    return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
            return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
        except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500

        # passwordbytes = Password.encode('utf=8')
        # isMatch=bcrypt.checkpw(passwordbytes,auth['Password'])
        # if not(isMatch):
        #     return jsonify({ "message": "Password is incorrect...","status":400 })
        # print(auth['_id'])
      
        
    
        

    @server.route("/auth/register",methods=["POST"])
    def register():
        try:
            user=request.json
            
            if not user:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            
            is_validated = validate_user(**user)
            print(is_validated)
            if is_validated is not True:
               
                return dict(message='Invalid data', data=None, error=is_validated), 400
            user = User().create(**user)
       

            # form_data=request.json
            # FirstName:form_data['FirstName']
            # LastName:form_data['LastName']
            # Email:form_data['Email']
            # Password:form_data['Password']

           
            if(user=='duplicateuser'):
                print("Email :{email} already exists...".format(email=user['email']))
                return jsonify({ "message": "Email :{email} already exists...".format(email=user['email'])}),409
            
            # Password='kol'
            # print('d')
        
            
                # passwordbytes = Password.encode('utf=8')
                # salt=bcrypt.gensalt()
                # hashedpw=bcrypt.hashpw(passwordbytes,salt)
                # print("password :", hashedpw)
                # id=user_collection.insert_one({
                # 'FirstName':'Janfffi',
                # 'LastName':'Wijewickrama',
                # 'Email':'lo@gmail.com',
                # 'Password':hashedpw
                # })
            return {
            "message": "Successfully created new user",
            "data": user
        }, 201
            
        except Exception as e:
            print(e)
            return jsonify({ "message": "Internal server error","status":500 })
            

    @server.route('/new-token',methods=['GET','POST'])
    def newaccesstoken():
        print("requesting new access token")

        cookies = request.cookies
    
        print("cookiee value :", cookies)


        if not(cookies['jwt']) :
            print("invalid refresh token :", cookies['jwt'])

            return jsonify({ "message": "Invalid token" ,"status":401})
        

        refresh_token = cookies['jwt']

        auth = user_collection.find_one({
            'refresh_token':refresh_token
        })

        if not(auth) :
            print("invalid refresh token :", refresh_token)
            return jsonify({ "message": "Invalid token" ,"status":403})
        

        authObject= {
            "id": str(auth['_id']),
            "role":os.getenv('USER_ROLE'),
        }
        
        print(os.getenv('REFRESH_TOKEN_SECRET'))
        decoded=jwt.decode(
            refresh_token,
            os.getenv('REFRESH_TOKEN_SECRET') ,algorithms=['HS256'])
        print(decoded)
        if(auth['_id'] != decoded['user_id']):
            print("requesting new access token failed invalid token")
            return jsonify({ "message": "Invalid token" ,"status":403})
        access_token=token.getAccessToken(authObject)
        print("new access token getting sucessfully")
        return jsonify({
                    "message": "Refresh token successful",
                    "access_token": access_token,
                    "status":200})
        
    @server.route("/auth/logout",methods=['GET',"POST"])
    def logout():
        cookies = request.cookies
        print("cookiee value :", cookies)

        if not(cookies['jwt']):
            return jsonify({ "message": "No token found" ,"status":204})
        

        refresh_token = cookies['jwt']

        auth = user_collection.find_one({
            'refresh_token':refresh_token
        })

        if not(auth) :
            print("invalid refresh token :", refresh_token)
            return jsonify({ "message": "User does not exist..." ,"status":404})
        

        result =user_collection.update_one({'_id':ObjectId(auth['_id'])},{'$set' :{
            'refresh_token':''
        }})
        print(result)


        response= make_response(jsonify({
            "message": "Logout successful",

            
        }),200)
        response.set_cookie('jwt','')
        return response


