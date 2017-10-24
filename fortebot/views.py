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

        for user in real_users:    
            sc.api_call(
                "chat.postEphemeral",
                channel=user.dm_channel,
                user=user.user_id,
                text="Hello, pls rate your team temperature from 1 to 10"
            )

    return success_response()

@api_view(['GET', 'POST'])
def messageSent(request):
    print(request.data)
    if request.method == 'POST':
        tkn = getToken()
        sc = SlackClient(tkn)  
        if str.isdigit(request.data['event']['text']):
            number = int(request.data['event']['text'])
            if number < 11 and number > 0 :
                with open("users", "a") as text_file:
                    text = text_file.read()
                    if request.data['event']['user'] not in text:
                        text_file.write(user_id + '\n')    
                        mp = Mixpanel('25d7ff3a1420b04b66b09bf53c7768af')
                        mp.track('Forte', '5', {
                            'Value': 5,
                            'Vote_id': 0 
                        })    
                    else:
                        sc.api_call(
                            "chat.postEphemeral",
                            channel=user_channel['channel']['id'],
                            user=request.data['event']['user'],
                            text="You already voted :) thanks"
                        )
            else:
                print("number is not in range")    
            print("text cointains numbers")
        else:
            print("text doesn't cointain numbers")
                
        
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
            