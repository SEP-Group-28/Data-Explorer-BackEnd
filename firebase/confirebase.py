import requests
import json
from models.alertusertoken import Add_TOKEN
#SERVER TOKEN
serverToken='AAAAHH3JbgU:APA91bEEtC7EAGqil7asmq-U1LZ5O6Q0IRGoUcQ0dS6uAv8HKzqlBP0INHLtcvRcEvEX4GD4zKwcftWO6-c6QMksvowSZj8Kf4N1Hv9FLk6-lYdaf_gEz719ucCkr3i6hBDaBYdai-gW'

def confirebase(cryptoname, price,user_id): #CALL FIREBASE
    try:
        token_list=Add_TOKEN().take_token_list(user_id)
        for i in token_list:
            deviceToken=i
            headers={
                'Content-Type' : 'application/json',
                'Authorization' : 'key='+ serverToken
            }
            body={
                'notification':{
                    'title':'New Alert',
                    'body':'Alert for '+ str(cryptoname) + ' Crossing '+ str(price),
                },
                'to':deviceToken,
                'priority':'high'
            }
            response=requests.post('https://fcm.googleapis.com/fcm/send',headers=headers,data=json.dumps(body))
            
    except Exception as e:
            return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": str(e)
        }, 500

    