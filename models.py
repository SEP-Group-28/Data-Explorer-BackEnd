"""Application Models"""
import bson, os
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL') 
# cluster= MongoClient(DATABASE_URL) #use for remote server

cluster = MongoClient(DATABASE_URL,27017)  
#use for localhost (mongodb compass)
db=cluster.TestDB
record_collection =db.record
user_collection=db.user

# class Books:
#     """Books Model"""
#     def __init__(self):
#         return

#     def create(self, title="", description="", image_url="", category="", user_id=""):
#         """Create a new book"""
#         book = self.get_by_user_id_and_title(user_id, title)
#         if book:
#             return
#         new_book = db.books.insert_one(
#             {
#                 "title": title,
#                 "description": description,
#                 "image_url": image_url,
#                 "category": category,
#                 "user_id": user_id
#             }
#         )
#         return self.get_by_id(new_book.inserted_id)

#     def get_all(self):
#         """Get all books"""
#         books = db.books.find()
#         return [{**book, "_id": str(book["_id"])} for book in books]

#     def get_by_id(self, book_id):
#         """Get a book by id"""
#         book = db.books.find_one({"_id": bson.ObjectId(book_id)})
#         if not book:
#             return
#         book["_id"] = str(book["_id"])
#         return book

#     def get_by_user_id(self, user_id):
#         """Get all books created by a user"""
#         books = db.books.find({"user_id": user_id})
#         return [{**book, "_id": str(book["_id"])} for book in books]
       
#     def get_by_category(self, category):
#         """Get all books by category"""
#         books = db.books.find({"category": category})
#         return [book for book in books]

#     def get_by_user_id_and_category(self, user_id, category):
#         """Get all books by category for a particular user"""
#         books = db.books.find({"user_id": user_id, "category": category})
#         return [{**book, "_id": str(book["_id"])} for book in books]

#     def get_by_user_id_and_title(self, user_id, title):
#         """Get a book given its title and author"""
#         book = db.books.find_one({"user_id": user_id, "title": title})
#         if not book:
#             return
#         book["_id"] = str(book["_id"])
#         return book

#     def update(self, book_id, title="", description="", image_url="", category="", user_id=""):
#         """Update a book"""
#         data={}
#         if title: data["title"]=title
#         if description: data["description"]=description
#         if image_url: data["image_url"]=image_url
#         if category: data["category"]=category

#         book = db.books.update_one(
#             {"_id": bson.ObjectId(book_id)},
#             {
#                 "$set": data
#             }
#         )
#         book = self.get_by_id(book_id)
#         return book

#     def delete(self, book_id):
#         """Delete a book"""
#         book = db.books.delete_one({"_id": bson.ObjectId(book_id)})
#         return book

#     def delete_by_user_id(self, user_id):
#         """Delete all books created by a user"""
#         book = db.books.delete_many({"user_id": bson.ObjectId(user_id)})
#         return book


class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, firstname="",lastname="", email="", password=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return 'duplicateuser'
        new_user = db.users.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": self.encrypt_password(password),
        
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        """Get all users"""
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        # user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        user = db.users.find_one({"_id": bson.ObjectId(user_id)})

        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, data={}):
        """Update a user"""
        
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def delete(self, user_id):
        """Delete a user"""

        Books().delete_by_user_id(user_id)
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_by_id(user_id)
        return user

    def disable_account(self, user_id):
        """Disable a user account"""
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

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
