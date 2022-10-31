"""Application Models"""
import bson, os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from dbconnection import connectdb as db
import cloudinary.uploader

# record_collection =db.record
print(db)
user_collection=db().user



class User:
    """User Model"""
    def __init__(self):
        return
    def changeactivation(self,user_id,founduser):
        # print('founduser',founduser)
        if(founduser['active']=='1'):
            activation='0'
        elif(founduser['active']=='0'):
            activation='1'
        user = user_collection.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": {'active':activation}
            }
        )
        user = self.get_by_id(user_id)
        return user

    def create(self, firstname="",lastname="", email="", password=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return 'duplicateuser'
#print("heelo")
        new_user = user_collection.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": self.encrypt_password(password),
        
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self,skip,take):
        try:
            """Get all users"""
            print('checlllll')
            users = user_collection.find().skip(skip).limit(take)
            print('looooooo')
            edited_list= [{"firstname":user['firstname'],'lastname':user['lastname'],'email':user['email'], "_id": str(user["_id"]),'active':user['active']} for user in users]
            # print(edited_list)
            return edited_list
                
        except Exception as e:
            print(e)
    def get_total_count(self):
        try:
            print('\nkdksfks')
            items=user_collection.estimated_document_count()
            print('items',items)
            return items
        except Exception as e:
            print(e)


    def get_by_id(self, user_id):
        """Get a user by id"""
        # user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        user = user_collection.find_one({"_id": bson.ObjectId(user_id)})

        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user
    # def get_watchlist_by_id(self,user_id):
    #     user = user_collection.find_one({"_id": bson.ObjectId(user_id)})
    #     if not user:
    #         return
    #     if 'watchlist' in user:
    #         return user['watchlist']
    #     else: 
    #         return False

    def get_password_by_id(self, user_id):
        """Get password of user by id"""
        # user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        user = user_collection.find_one({"_id": bson.ObjectId(user_id)})

        if not user:
            return
        return user['password']

    def get_by_email(self, email):
        """Get a user by email"""
        user = user_collection.find_one({"email": email})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user
    def get_by_refreshtoken(self, refreshtoken):
        """Get a user by refreshtoken"""
        user = user_collection.find_one({"refreshtoken": refreshtoken})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, data={}):
        """Update a user"""
        
        user = user_collection.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user
    
    def update_photo(self, photodetails):
        """Update user photo"""
        print('update user came')
       
        try:
            cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('CLOUDINARY_API_KEY'), 
            api_secret=os.getenv('CLOUDINARY_API_SECRET'))
            upload_result = None
          
            file_to_upload = photodetails
            print(file_to_upload)
            # app.logger.info('%s file_to_upload', file_to_upload)
            if file_to_upload:
                
                upload_result = cloudinary.uploader.upload(file_to_upload)
                # app.logger.info(upload_result)
                print('upload_result',upload_result)
                return upload_result
            return 
        except Exception as e:
            print(e)
        


        
        # user = user_collection.update_one(
        #     {"_id": bson.ObjectId(user_id)},
        #     {
        #         "$set": data
        #     }
        # )
        # user = self.get_by_id(user_id)
        # return user
    

    def delete(self, email):
        """Delete a user"""

        # Books().delete_by_user_email(email)
        user_collection.delete_one({"email": email})
        deluser = self.get_by_email(email)
        return deluser

    def disable_account(self, user_id):
        """Disable a user account"""
        user = user_collection.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user
    def check_encrypted_password(self,entered_password,password):
        if not check_password_hash(entered_password,password):
            return False
        return True

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        # print("db password :", user["password"])
        # print("entered password:", password)
        if not(user) :
            return 'wrong_email'
        if not check_password_hash(user["password"], password):
            return 'wrong_password'
        user.pop("password")
        return user
