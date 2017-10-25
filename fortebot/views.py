from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .errors import *
from slackclient import SlackClient
import json
import os
import jwt
from .user import User
from mixpanel import Mixpanel
import asyncio

@api_view(['GET', 'POST'])
def anonymous_feedback(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    sc.api_call(
        "chat.postMessage",
        channel="G7NUMC5FA",
        text=request.data['event']['text']
    )    
    return success_response()

@api_view(['GET', 'POST'])
def vote(request):
    if request.method == 'POST':
        open('users', 'w').close()
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
                real_users.append(User(user_id, user_channel['channel']['id']) )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_msg(real_users))
        loop.close()

    return success_response()

async def send_msg(real_users):
    for user in real_users:    
            sc.api_call(
                "chat.postEphemeral",
                channel=user.dm_channel,
                user=user.user_id,
                text="Hello, pls rate your team temperature from 1 to 10"
            )
    pass

@api_view(['GET', 'POST'])
def messageSent(request):
    if request.method == 'POST':
        tkn = getToken()
        sc = SlackClient(tkn)  
        user_channel = open_channel_if_needed(sc, request)

        if str.isdigit(request.data['event']['text']):
            number = int(request.data['event']['text'])
            if number < 11 and number > 0 :
                with open("users", "r") as text_file:
                    text = text_file.read()
                    if request.data['event']['user'] not in text:
                        with open("users", "a") as text_file:
                            text_file.write(request.data['event']['user'] + '\n')    
                            mp = Mixpanel('25d7ff3a1420b04b66b09bf53c7768af')
                            mp.track('Forte', request.data['event']['text'], {
                                'Value': 5,
                                'Vote_id': 0 
                            })
                            sc.api_call(
                                "chat.postEphemeral",
                                channel=user_channel['channel']['id'],
                                user=request.data['event']['user'],
                                text="thanks"
                            )    
                    else:
                        sc.api_call(
                            "chat.postEphemeral",
                            channel=user_channel['channel']['id'],
                            user=request.data['event']['user'],
                            text="You already voted :) thanks"
                        )
            else:
                sc.api_call(
                    "chat.postEphemeral",
                    channel=user_channel['channel']['id'],
                    user=request.data['event']['user'],
                    text="number is not in range"
                )    
        else:
            sc.api_call(
                "chat.postEphemeral",
                channel=user_channel['channel']['id'],
                user=request.data['event']['user'],
                text="text doesnt contains numbers"
            )        

        return JsonResponse(request.data)
    else:
        return success_response()


def open_channel_if_needed(sc, request): 
    return sc.api_call(
        "im.open",
        user=request.data['event']['user'],
    )      


def getToken():
    path = os.path.join('noname')
    with open(path , 'r') as myfile:
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithms=['HS256'])
        return decoded['some']
            
