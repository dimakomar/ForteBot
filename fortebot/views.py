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
from .user import User

@api_view(['GET', 'POST'])
def vote(request):
    if request.method == 'POST':
        tkn = getToken()
        sc = SlackClient(tkn)
        user_list = sc.api_call(
            "users.list"
        )
        
        members_array = user_list["members"]
        
        ids_array = []
        for member in members_array:
            ids_array.append(member['id'])

        real_users = []
        for user_id in ids_array:
            user_channel = sc.api_call(
                "im.open",
                user=user_id,
            )

            if user_channel['ok'] == True:
                # User()
                real_users.append(User(user_id, user_channel['channel']['id']) )
    
        print(real_users)
        for user in real_users:    
            sc.api_call(
                "chat.postEphemeral",
                channel=user.dm_channel,
                user=user.user_id,
                text="message for everyone on channel"
            )
    return success_response(user_list)

@api_view(['GET', 'POST'])
def messageSent(request):

    if request.method == 'POST':
        tkn = getToken()
        sc = SlackClient(tkn)
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


def getToken():
    path = os.path.join('noname')
    with open(path , 'r') as myfile:
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithms=['HS256'])
        return decoded['some']
            