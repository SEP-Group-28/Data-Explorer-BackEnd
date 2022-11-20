import bson, os
from werkzeug.security import generate_password_hash, check_password_hash
from dbconnection import connectdb as db
import cloudinary.uploader
import re

user_collection=db().user

#USER MODEL
class User:
    """User Model"""
    def __init__(self):
        return
    def changeactivation(self,user_id,founduser):
        if(founduser['active']=='1'):
            activation='0'
        elif(founduser['active']=='0'):
            activation='1'
        user = user_collection.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": {'active':activation, 'refresh_token':None}
            }
        )
        user = self.get_by_id(user_id)
        return user

    def create(self, firstname="",lastname="", email="", password="", role=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return 'duplicateuser'
        new_user = user_collection.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": self.encrypt_password(password),
                "active":'1',
                "role": role
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_user_list(self, users):
        edited_list = []
        for user in users:
            temp = {"firstname":user['firstname'],'lastname':user['lastname'],'email':user['email'], "_id": str(user["_id"]), "active":user['active']}
            if ('dob' in user):
                temp['dob']=user['dob']
            elif ('country' in user):
                temp['country']=user['country']
            edited_list.append(temp)
        return edited_list

    def get_all_search(self, search, filter, skip, take):
        """Get all users using search"""
        try:
            regx = re.compile(search, re.IGNORECASE)
            users = user_collection.find({filter.lower():regx})
            user_count = len(self.get_user_list(users))
            users_ =  user_collection.find({filter.lower():regx, 'role':'1'}).skip(skip).limit(5)
            
            return self.get_user_list(users_), user_count
        except Exception as e:
            print(e)


    def get_all(self,skip,take):
        try:
            """Get all users"""
            users = user_collection.find({'role':'1'}).skip(skip).limit(take)
            return self.get_user_list(users)    
        except Exception as e:
            print(e)
    def get_total_count(self):
        try:
            # get user count
            items = user_collection.find({'role':'1'}).count()
            return items
        except Exception as e:
            print(e)


    def get_by_id(self, user_id):
        """Get a user by id"""
        user = user_collection.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            return
        user["_id"] = str(user["_id"])

        user.pop("password")
        return user

    def get_password_by_id(self, user_id):
        """Get password of user by id"""
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
        user = user_collection.find_one({"refresh_token": refreshtoken})
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
       
        try:
            cloudinary.config(cloud_name = os.environ.get('CLOUD_NAME'), api_key=os.environ.get('CLOUDINARY_API_KEY'), 
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'))
            upload_result = None
          
            file_to_upload = photodetails
            if file_to_upload:
                
                upload_result = cloudinary.uploader.upload(file_to_upload)
                return upload_result
            return 
        except Exception as e:
            print(e)
        


        

    

    def delete(self, email):
        """Delete a user"""

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
        if not(user) :
            return 'wrong_email'
        if not check_password_hash(user["password"], password):
            return 'wrong_password'
        user.pop("password")
        return user
