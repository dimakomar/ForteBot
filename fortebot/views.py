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
from datetime import datetime
from threading import Timer

x=datetime.today()
y=x.replace(day=x.day+0, hour=0, minute=0, second=3, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def hello_world():
    print("hello world")



def send_msg():
    open_channel_and_send("repeating message")

@api_view(['GET', 'POST'])
def messageSent(request):
    t = Timer(secs, hello_world)
    t.start()

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


def open_channel_and_send(message):
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

    sc.api_call(
        "chat.postEphemeral",
        channel=user_channel['channel']['id'],
        user='U7F85AA80',
        text=message
    )

