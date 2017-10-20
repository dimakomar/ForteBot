from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .errors import *
from slackclient import SlackClient
from fortebot.settings import SLACK_BOT_TOKEN
import json
import os
import jwt
import schedule
import time



@api_view(['GET', 'POST'])
def hello_world(request):
    
    return success_response()

def hello():
    print("hello")


def send_msg():
    open_channel_and_send("repeating message")

@api_view(['GET', 'POST'])
def messageSent(request):

    if request.method == 'POST':
        path = os.path.join('noname')
        with open(path , 'r') as myfile:
            encoded_token = myfile.read()
            decoded = jwt.decode(encoded_token, 'hello', algorithms=['HS256'])
            slack_token = decoded['some']
            sc = SlackClient(slack_token)
            user_channel = sc.api_call(
                "im.open",
                user=request.data['event']['user'],
            )        
            sc.api_call(
                "chat.postEphemeral",
                channel=user_channel['channel']['id'],
                user=request.data['event']['user'],
                text="you just said " + request.data['event']['text'] + " :bear:"
            )

        return JsonResponse(request.data)
    else:
        return success_response()


def open_channel_and_send():
    

    path = os.path.join('noname')
    with open(path , 'r') as myfile:
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithms=['HS256'])
        slack_token = decoded['some']
        
    sc = SlackClient(slack_token)
    user_channel = opened_dm = sc.api_call(
        "im.open",
        user='U7F85AA80',
    )            
    user_ss = sc.api_call(
                "users.list"
    )
    print(user_ss)    

    sc.api_call(
        "chat.postEphemeral",
        channel=user_channel['channel']['id'],
        user='U7F85AA80',
        text=user_ss
    )

schedule.every(15).seconds.do(open_channel_and_send)
while True:
    schedule.run_pending()
    time.sleep(1) 
