from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
load_dotenv()
import os

print(os.getenv('ACCESS_TOKEN_SECRET'))
def getAccessToken(auth):
    return jwt.encode(
        payload={    
            "user_id": auth['id'],
            "role": auth['role'],
            "exp":datetime.utcnow()+timedelta(seconds=60)
        },
         key=os.getenv('ACCESS_TOKEN_SECRET'),


    )


def getRefreshToken(auth):
    return jwt.encode(
        payload={ "user_id": auth['id'],
        "exp":datetime.utcnow()+timedelta(seconds=60*60*24)
        },
        key=os.getenv('REFRESH_TOKEN_SECRET'),

    )


