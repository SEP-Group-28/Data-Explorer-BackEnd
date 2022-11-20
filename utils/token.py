from datetime import datetime, timedelta
import jwt
import os

#SET ACCESSTOKEN TO ONE HOUR
def getAccessToken(auth):
    return jwt.encode(
        payload={    
            "user_id": auth['id'],
            "role": auth['role'],
            "exp":datetime.utcnow()+timedelta(seconds=60*60)
        },
         key=os.environ.get('ACCESS_TOKEN_SECRET'),
    )

#SET REFRESH TOKEN TO ONE DAY
def getRefreshToken(auth):
    return jwt.encode(
        payload={ "user_id": auth['id'],
        "exp":datetime.utcnow()+timedelta(seconds=60*60*24)
        },
        key=os.environ.get('REFRESH_TOKEN_SECRET'),

    )


