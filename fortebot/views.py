from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from .errors import *
from django.conf import settings
from slackclient import SlackClient
import json
import os
import jwt
from .user import User
from mixpanel import Mixpanel
import after_response
from time import sleep
from urllib.parse import urlencode, quote_plus

@api_view(['POST'])
def click(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    result = json.loads(request.data["payload"])
    value = result["actions"][0]["selected_options"][0]["value"]
    user = result["user"]["id"]
    channel = result["channel"]["id"]
    with open("fortebot/static/users", "r") as text_file:
        text = text_file.read()

    print("USERS")
    print(text)
    if user in text:

        send_ephemeral_msg(sc,user,channel,settings.ALREADY_VOTED_PHRASE)
        return HttpResponse()
    else:
       
        with open("fortebot/static/users", "a") as users_file:
            users_file.write(user + '\n')    
            with open("fortebot/static/marks", "a") as marks_file:
                marks_file.write("".join([value + ","]))       
                print("writed")                     
            mp = Mixpanel(settings.MIXPANEL_TOKEN)
            mp.track('Forte', value)

        
        send_ephemeral_msg(sc,user,channel,"".join([settings.THANKS_PHRASE, str(value), "*\n you can add your anonymous comment for HRs by `/anon_msg` *`text`*"]))
        return HttpResponse()

@api_view(['POST'])
def get_results(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] == settings.PRIVATE_CHANNEL:
        path = os.path.join('fortebot/static/marks')
        print(path)
        with open(path , 'r') as marks_file:
            marks_file = marks_file.read()
            if marks_file == "":
                send_ephemeral_msg(sc,request.data['user_id'], request.data['channel_id'],settings.NOONE_VOTED)
                return HttpResponse()
            marks_splitted_list = marks_file.split(",")
            numbered_list = list(filter(lambda n: n != "", marks_splitted_list))
            print(numbered_list)
            all_marks = sum(list(map(int, numbered_list)))
            avarage_num = round(all_marks / len(numbered_list), 1)
            path = os.path.join('fortebot/static/last_vote_name')
            with open(path, "r") as last_vote_name_file:
                vote_name = last_vote_name_file.read()
            send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], "".join([vote_name, " result: ", str(avarage_num), " out of: ", str(len(numbered_list)), " people voted"]))  
    else:
        send_ephemeral_msg(sc,request.data['user_id'], request.data['channel_id'],"You are not allowed to get results")
    return HttpResponse()

@api_view(['POST'])
def help(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    send_att(sc, request.data['user_id'], request.data['channel_id'], settings.HELP)  
    return HttpResponse()

@api_view(['POST'])
def delivery(request):
    print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)
    send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], settings.DELIVERY)  
    return HttpResponse()

@api_view(['POST'])
def anonymous_msg_random(request):
    return send_normal_msg(request, "random")

@api_view(['POST'])
def anonymous_feedback(request):
    return send_normal_msg(request, settings.PRIVATE_CHANNEL)

#MARK : Votes 
@api_view(['POST'])
def temperature_vote(request):
    print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)
    print(request.data['channel_id'])
    if request.data['channel_id'] != settings.PRIVATE_CHANNEL:
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],settings.BAD_CHANNEL_PHRASE)
        return HttpResponse()

    start_rating_vote(request,settings.VOTE_PHRASE)
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"You've just started the team temperature vote")
    return HttpResponse()

@api_view(['POST'])
def rating_vote(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] != settings.PRIVATE_CHANNEL:
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],settings.BAD_CHANNEL_PHRASE)
        return HttpResponse()
    
    if request.data["text"] == "" or request.data["text"] == " ":
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"You've been a step away from huge fail by *starting vote with empty message* please check `/help_forte_bot`")
        return HttpResponse()

    start_rating_vote(request,"".join([request.data["text"], settings.TEXT_VOTE_PHRASE]))
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"".join(["You've just started the vote: ", "*", request.data["text"], "*"]))
    return HttpResponse()

@api_view(['POST'])
def start_question_vote(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] != settings.PRIVATE_CHANNEL:
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],settings.BAD_CHANNEL_PHRASE)
        return HttpResponse()

    if request.data["text"] == "" or request.data["text"] == " ":
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"You've been a step away from huge fail by *starting vote with empty message* please check `/help_forte_bot`")
        return HttpResponse()

    send_msg_to_all.after_response(sc, request, "".join([request.data["text"], settings.PLEASE_REPLY_WITH_ANON]), False )
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"".join(["You've just started the question vote: ", "*",request.data["text"], "*"]))
    return HttpResponse()

#This part is responsible for Slack Events API 
@api_view(['POST'])
def sent_message(request):
    print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)  
    user_channel = open_events_api_channel_if_needed(sc, request)
    t = request.data['event']['text'] 
    usr = request.data['event']['user']
    channel = user_channel['channel']['id']
    if "Hello" in t or "hello" in t or "Hi" in t or "hi" in t or "Hey" in t or "hey" in t:
        send_ephemeral_msg(sc,usr,channel, "Hi")
        return HttpResponse()
    if t == "How are you" or t == "how are you" or t == "Wassup" or t == "wassup" or t == "sup" or t == "Sup":
        send_ephemeral_msg(sc,usr,channel, "I'm happy to be alive") 
        return HttpResponse()
    if "you" in t or "You" in t or "u" in t:
        send_ephemeral_msg(sc,usr,channel, "I can say same about you") 
        return HttpResponse()
    if "creator" in t or "Creator" in t or "created" in t or "Created" in t:
        send_ephemeral_msg(sc,usr,channel, "I'm created by DK") 
        return HttpResponse()
    if "creator" in t or "Creator" in t or "created" in t:
        send_ephemeral_msg(sc,usr,channel, "I'm created by DK") 
        return HttpResponse()
    if "think" in t or "Think" in t:
        send_ephemeral_msg(sc,usr,channel, "I'm not allowed to think about it") 
        return HttpResponse()
    if t == "myid":
        send_ephemeral_msg(sc,usr,channel, "".join([ "You are a meatbag with id `", request.data['event']['user'], "`"])) 
        return HttpResponse()
    if t == "channelid":
        send_ephemeral_msg(sc,usr,channel, "".join([ "channel id is `", request.data['event']['channel'], "`"])) 
        return HttpResponse()
    
    send_ephemeral_msg(sc,usr,channel, ":sch:? Thats too hard for me")              
    return HttpResponse()  

def send_normal_msg(request,channel):
    tkn = getToken()
    sc = SlackClient(tkn)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text="`anonymous:` " + request.data['text'] 
    )    
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'], "*Thanks*")     
    return HttpResponse()


def start_rating_vote(request, msg):
    
    tkn = getToken()
    sc = SlackClient(tkn)

    open('fortebot/static/users', 'w').close()
    open('fortebot/static/marks', 'w').close()
    open('fortebot/static/last_vote_name', 'w').close()

    with open("fortebot/static/users", "r") as text_file:
        text = text_file.read()
        print(text)
    
    with open("fortebot/static/last_vote_name", "a") as last_vote_name_file:
        last_vote_name_file.write(request.data['text'] if request.data['text'] != "" else "Temperature vote") 
    send_msg_to_all.after_response(sc, request, msg)
    return HttpResponse()

@after_response.enable
def send_msg_to_all(sc,request,msg, is_raing = True):
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
            
            real_users.append(User(user_id, user_channel['channel']['id']))
    send_msg(sc, real_users, request, msg, is_raing)
    return HttpResponse()

def send_msg(sc, real_users, req, msg, is_rating):
    number = 0
    for user in real_users:    
        number = number + 1

        if is_rating:
            send_att(sc,user.user_id,user.dm_channel, msg)    
        else: 
            send_ephemeral_msg(sc,user.user_id,user.dm_channel, msg)
        sleep(1)
        

def open_channel_if_needed(sc, request): 
    return sc.api_call(
        "im.open",
        user=request.data['user_id'],
    ) 

def open_events_api_channel_if_needed(sc, request): 
    return sc.api_call(
        "im.open",
        user=request.data['event']['user']
    )       

def getToken():
    path = os.path.join('fortebot/static/noname')
    with open(path , 'r') as myfile:
        print("opened")
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithms=[settings.CODING_ALGORITHM_NAME])
        return decoded['some']
            
def send_ephemeral_msg(sc, user, channel, text):
    sc.api_call(
        "chat.postEphemeral",
        channel=channel,
        user=user,
        text=text
    )  

def send_att(sc,user,channel,text):
    message_attachments = [
        {
            "text": text,
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "games_list",
                    "text": "Mark",
                    "type": "select",
                    "options": [
                        {
                            "text": "1",
                            "value": "1"
                        },
                        {
                            "text": "2",
                            "value": "2"
                        },
                        {
                            "text": "3",
                            "value": "3"
                        },
                        {
                            "text": "4",
                            "value": "4"
                        },
                        {
                            "text": "5",
                            "value": "5"
                        },
                        {
                            "text": "6",
                            "value": "6"
                        },
                        {
                            "text": "7",
                            "value": "7"
                        },
                        {
                            "text": "8",
                            "value": "8"
                        },
                        {
                            "text": "9",
                            "value": "9"
                        },
                        {
                            "text": "10",
                            "value": "10"
                        }
                    ]
                }
            ]
        }
    ]
    sc.api_call(
        "chat.postEphemeral",
        channel=channel,
        user=user,
        attachments=message_attachments
    )
    