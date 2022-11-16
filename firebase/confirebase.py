import requests
import json
from models.alertusertoken import Add_TOKEN
# from pubsub.pubsubservices import publish_to_socket_for_real_time_notifications

serverToken='AAAAHH3JbgU:APA91bEEtC7EAGqil7asmq-U1LZ5O6Q0IRGoUcQ0dS6uAv8HKzqlBP0INHLtcvRcEvEX4GD4zKwcftWO6-c6QMksvowSZj8Kf4N1Hv9FLk6-lYdaf_gEz719ucCkr3i6hBDaBYdai-gW'

def confirebase(cryptoname, price,user_id):
    token_list=Add_TOKEN().take_token_list(user_id)
    print('price is',price)
    print('printing.....',token_list)
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
        print('response is :-',response)
        print('response_status_code',response.status_code)
        print(response.json())

    