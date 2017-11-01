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

@api_view(['POST'])
def get_results(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    path = os.path.join('marks')
    with open(path , 'r') as marks_file:
        marks_file = marks_file.read()
        print(marks_file)
        if marks_file == "":
            send_ephemeral_msg(sc,request.data['user_id'], request.data['channel_id'],settings.NOONE_VOTED)
            return HttpResponse()
        
        marks_splitted_list = marks_file.split(",")
        numbered_list = list(filter(lambda n: n != "", marks_splitted_list))
        all_marks = sum(list(map(int, numbered_list)))
        avarage_num = round(all_marks / len(numbered_list), 1)
        path = os.path.join('last_vote_name')
        with open(path, "r") as last_vote_name_file:
            vote_name = last_vote_name_file.read()
        send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], "".join([vote_name, " result: ", str(avarage_num), " out of: ", str(len(numbered_list)), " people voted"]))  
    return HttpResponse()

@api_view(['POST'])
def help(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], settings.HELP)  
    return HttpResponse()

@api_view(['POST'])
def delivery(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], settings.DELIVERY)  
    return HttpResponse()

@api_view(['POST'])
def rate(request):
    print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)
    user_channel = open_channel_if_needed(sc, request)
    msg = request.data["text"]
    # text = ""
    with open("users", "r") as text_file:
        text = text_file.read()

    if request.data['user_id'] in text:
        send_ephemeral_msg(sc,request.data['user_id'],user_channel['channel']['id'],settings.ALREADY_VOTED_PHRASE)
        return HttpResponse()

    if str.isdigit(msg):
        number = int(msg)
        if number < 11 and number > 0 :
            with open("users", "r") as text_file:
                text = text_file.read()
        else:
            send_ephemeral_msg(sc,request.data['user_id'],user_channel['channel']['id'],settings.NOT_IN_RANGE_PHRASE)
            return HttpResponse()

        if request.data['user_id'] not in text:
            with open("users", "a") as text_file:
                text_file.write(request.data['user_id'] + '\n')    
                with open("marks", "a") as marks_file:
                    marks_file.write("".join([msg + ","]))                            
                mp = Mixpanel(settings.MIXPANEL_TOKEN)
                mp.track('Forte', msg)
            send_ephemeral_msg(sc,request.data['user_id'],user_channel['channel']['id'],settings.THANKS_PHRASE)
            return HttpResponse()
    else:
        send_ephemeral_msg(sc,request.data['user_id'],user_channel['channel']['id'],settings.NOT_A_NUMBER_PHRASE)              
    return HttpResponse()  

@api_view(['POST'])
def anonymous_msg_random(request):
    return send_normal_msg(request, "random")

@api_view(['POST'])
def anonymous_feedback(request):
    return send_normal_msg(request, settings.PRIVATE_CHANNEL)

@api_view(['POST'])
def question_vote(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] == settings.PRIVATE_CHANNEL:
        send_msg_to_all(sc, request, "".join([request.data["text"], settings.PLEASE_REPLY_WITH_ANON]))
    return HttpResponse()

@api_view(['POST'])
def temperature_vote(request):
    start_rating_vote.after_response(request,settings.VOTE_PHRASE)
    return HttpResponse()

@api_view(['POST'])
def rating_vote(request):
    return start_rating_vote.after_response(request,"".join([request.data["text"], settings.TEXT_VOTE_PHRASE]))

@api_view(['POST'])
def sent_message(request):
    tkn = getToken()
    sc = SlackClient(tkn)  
    user_channel = open_events_api_channel_if_needed(sc, request)
    t = request.data['event']['text'] 
    usr = request.data['event']['user']
    channel = user_channel['channel']['id']
    if t == "Hello" or t == "hello" or t == "Hi" or t == "hi" or t == "Hey" or t == "hey":
        send_ephemeral_msg(sc,usr,channel, "Yes, I'm here") 
        return HttpResponse()
    if t == "How are you" or t == "how are you" or t == "Wassup" or t == "wassup" or t == "sup" or t == "Sup":
        send_ephemeral_msg(sc,usr,channel, "Doing good as always") 
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
    return HttpResponse()

@after_response.enable
def start_rating_vote(request, msg):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] == settings.PRIVATE_CHANNEL:
        open('users', 'w').close()
        open('marks', 'w').close()
        open('last_vote_name', 'w').close()
        with open("last_vote_name", "a") as last_vote_name_file:
            last_vote_name_file.write(request.data['text'] if request.data['text'] != "" else "Temperature vote") 
        send_msg_to_all(sc, request, "".join([msg, "settings.PLEASE_REPLY_WITH_RATE"]))
        return HttpResponse()
    else:
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],settings.BAD_CHANNEL_PHRASE)
    return HttpResponse()

def send_msg_to_all(sc,request,msg):
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
    send_msg(sc, real_users, request, msg)
    return HttpResponse()

def send_msg(sc, real_users, req, msg):
    for user in real_users:    
        print("send")
        send_ephemeral_msg(sc,user.user_id,user.dm_channel, msg)
        

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
    path = os.path.join('noname')
    with open(path , 'r') as myfile:
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