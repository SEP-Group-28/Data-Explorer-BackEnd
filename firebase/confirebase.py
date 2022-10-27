import requests
import json

serverToken='AAAAHH3JbgU:APA91bEEtC7EAGqil7asmq-U1LZ5O6Q0IRGoUcQ0dS6uAv8HKzqlBP0INHLtcvRcEvEX4GD4zKwcftWO6-c6QMksvowSZj8Kf4N1Hv9FLk6-lYdaf_gEz719ucCkr3i6hBDaBYdai-gW'

def confirebase(deviceToken):
    headers={
        'Content-Type' : 'application/json',
        'Authorization' : 'key='+ serverToken
    }
    body={
        'notification':{
            'title':'Sending push from python script',
            'body':'New message'
        },
        'to':deviceToken,
        'priority':'high'

    }
    response=requests.post('https://fcm.googleapis.com/fcm/send',headers=headers,data=json.dumps(body))
    print('response is :-',response)
    print('response_status_code',response.status_code)
    print(response.json())