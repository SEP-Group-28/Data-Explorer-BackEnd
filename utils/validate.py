"""Validator Module"""
import re
from bson.objectid import ObjectId

def validate(data, regex):
    """Custom Validator"""
    return True if re.search(regex, data) else False

def validate_password(password: str,reg):
    """Password Validator"""
    # reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

# def validate_book(**args):
#     """Book Validator"""
#     if not args.get('title') or not args.get('image_url') \
#         or not args.get('category') or not args.get('user_id'):
#         return {
#             'title': 'Title is required',
#             'image_url': 'Image URL is required',
#             'category': 'Category is required',
#             'user_id': 'User ID is required'
#         }
#     if args.get('category') not in ['romance', 'peotry', 'politics' 'picture book', 'science', 'fantasy', 'horror', 'thriller']:
#         return {
#             'status': 'error',
#             'message': 'Invalid category'
#         }
#     try:
#         ObjectId(args.get('user_id'))
#     except:
#         return {
#             'user_id': 'User ID must be valid'
#         }
#     if not isinstance(args.get('title'), str) or not isinstance(args.get('description'), str) \
#         or not isinstance(args.get('image_url'), str):
#         return {
#             'title': 'Title must be a string',
#             'description': 'Description must be a string',
#             'image_url': 'Image URL must be a string',
#         }
#     return True

def validate_user(**args):
    """User Validator"""
    print(args.get('email'))
    if  not args.get('email') or not args.get('password') or not args.get('firstname') or not args.get('lastname'):
        return {
            'email': 'Email is required',
            'password': 'Password is required',
            'firstname': 'First name is required',
            'lastname': 'Last name is required',
        }
    if not isinstance(args.get('firstname'), str) or not isinstance(args.get('lastname'), str) or\
        not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
            'firstname': 'First name must be a string',
            'lastname': 'Last name must be a string',
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    # if not validate_password(args.get('password')):
    #     return {
    #         'password': 'Password is invalid, Should be atleast 8 characters with \
    #             upper and lower case letters, numbers and special characters'
    #     }
    if not validate_password(args.get('password'),'[A-Z]'):
#print(args.get('password'))
        return {
        'password':"Password must contain at least one uppercase letter"
        }
    elif not (validate_password(args.get('password'),'[a-z]')):
        return {
               'password': "Password must contain at least one lowercase letter"
            }
            
    elif not (validate_password(args.get('password'),'[0-9]') ):
        return {'password':"Password must contain at least one number"}

    elif not (validate_password(args.get('password'),'[#?!@$%^&*-]')):
        return {
                'password':"Password must contain at least one special character"
            }
            
    if not 2 <= len(args['firstname']) :
        return {
            'firstname': '1'
        }
    if not 2 <= len(args['lastname']) :
        return {
            'lastname': 'Last Name must be between 2 and 30 characters'
        }
    return True

def validate_email_and_password(email, password):
    """Email and Password Validator"""
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(password,'[A-Z]'):
        return {
        'password':"Password must contain at least one uppercase letter"
        }
    elif not (validate_password(password,'[a-z]')):
        return {
               'password': "Password must contain at least one lowercase letter"
            }
            
    elif not (validate_password(password,'[0-9]') ):
        return {'password':"Password must contain at least one number"}
        
    elif not (validate_password(password,'[#?!@$%^&*-]')):
        return {
                'password':"Password must contain at least one special character"
            }
            
    return True
