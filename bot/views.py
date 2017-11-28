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
from .models import Message


@api_view(['POST'])
def click(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    value = ""
    result = json.loads(request.data["payload"])
    print(result)
    if result["actions"][0]["type"] == "button":
        value = result["actions"][0]["value"]
    else:
        value = result["actions"][0]["selected_options"][0]["value"]    

    callback_id = result["callback_id"]  
    print(callback_id)
    ts = result["message_ts"]
    user = result["user"]["id"]
    channel = result["channel"]["id"]


    if callback_id == "anon_msg_reply":

        send_ephemeral_msg(sc,user,channel,"To reply use `/reply " + str(value) + " text`\n")
        return HttpResponse()
        

    if value == "no_tnx":
        sc.api_call(
        "chat.delete",
        channel=channel,
        ts=ts)    
        return HttpResponse()

    if value == "comment":
        
        message_attachments = [
        {   "text": "To leave comment use `/anon_msg` *`text`* \n ```example: /anon_msg super important comment```",
                "color": "#3AA3E3",
                "mrkdwn_in": [
                    "text"
                ]
            }
        ]

        sc.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        attachments=message_attachments)
        return HttpResponse()

    if value == "anon_message":
        
        message_attachments = [
        {   "text": "To send anoymous message use `/anon_msg` *`text`* \n ```example: /anon_msg some question```",
                "color": "#3AA3E3",
                "mrkdwn_in": [
                    "text"
                ]
            }
        ]

        sc.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        attachments=message_attachments)
        return HttpResponse()

    with open("bot/static/users", "r") as text_file:
        text = text_file.read()
    
    #no need this check anymore
    if user in text:
        send_ephemeral_msg(sc,user,channel,settings.ALREADY_VOTED_PHRASE)
        return HttpResponse()
    else:
        with open("bot/static/users", "a") as users_file:
            users_file.write(user + '\n')    
            with open("bot/static/marks", "a") as marks_file:
                marks_file.write("".join([value + ","]))       
                print("writed")                     
            mp = Mixpanel(settings.MIXPANEL_TOKEN)
            mp.track('Forte', value)

        message_attachments = [
        {
            "text": "Want to comment your mark anonymously ?",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "game",
                    "text": "No, Thanks",
                    "type": "button",
                    "value": "no_tnx",
                    "style": "danger"
                },
                {
                    "name": "game",
                    "text": "Leave Comment",
                    "type": "button",
                    "value": "comment",
                    "style": "primary"
                }
            ]
        }]

        sc.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        attachments=message_attachments)
        return HttpResponse()

@api_view(['POST'])
def get_results(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    if request.data['channel_id'] == settings.PRIVATE_CHANNEL:
        path = os.path.join('bot/static/marks')
        print(path)
        with open(path , 'r') as marks_file:
            marks_file = marks_file.read()
            if marks_file == "":
                send_ephemeral_msg(sc,request.data['user_id'], request.data['channel_id'],settings.NOONE_VOTED)
                return HttpResponse()
            marks_splitted_list = marks_file.split(",")
            numbered_list = list(filter(lambda n: n != "", marks_splitted_list))
            all_marks = sum(list(map(int, numbered_list)))
            avarage_num = round(all_marks / len(numbered_list), 1)
            path = os.path.join('bot/static/last_vote_name')
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
    send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], settings.HELP)  
    return HttpResponse()

@api_view(['POST'])
def delivery(request):
    print(request.data)
    ids_path = os.path.join('bot/static/message_ids')
    with open(ids_path , 'r') as message_ids:
        let = message_ids.read()
        print(let)
    with open(ids_path , 'a') as message_ids:
        marks_file.write("".join(["1,"]))  
        
    with open(ids_path , 'r') as message_ids:
        let = message_ids.read()
        print(let)
    tkn = getToken()
    sc = SlackClient(tkn)
    send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], settings.DELIVERY)  
    return HttpResponse()

@api_view(['POST'])
def reply(request):
    
    if request.data['channel_id'] != settings.PRIVATE_CHANNEL:
        send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],settings.BAD_CHANNEL_PHRASE)
        return HttpResponse()

    params = request.data["text"].split(" ")
    message_id = params[0]

    with open("bot/static/message_user_ids", "r") as message_user_ids:
        real_user_ids = message_user_ids.read()
        splitter_ids = real_user_ids.split(",")
        print(splitter_ids) 
        user_id = splitter_ids[int(message_id)]

    tkn = getToken()
    sc = SlackClient(tkn)
    new_list = params
    new_list.pop(0)
    message_attachments = [
    {   "text":"`Managment response:` " + ' '.join(new_list),
            "color": "#3AA3E3",
            "mrkdwn_in": [
                "text"
            ]
        }
    ]
    
    channel = open_channel_if_needed(sc,request,user_id)
    sc.api_call(
        "chat.postMessage",
        channel=channel["channel"]["id"],
        attachments=message_attachments
    )
    return HttpResponse()


@api_view(['POST'])
def anonymous_feedback(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    ids_path = os.path.join('bot/static/message_ids')
    user_ids_path = os.path.join('bot/static/message_user_ids')
    with open(ids_path , 'r') as message_ids:
        ids_file = message_ids.read()
        print(ids_file)
        ids_splitted_list = ids_file.split(",")
        ids_numbered_list = list(filter(lambda n: n != "", ids_splitted_list))
        print(ids_numbered_list)
        all_ids = list(map(int, ids_numbered_list))
        print(all_ids)
        last = all_ids.pop()
        new_id = last + 1
    with open(ids_path , 'a') as message_ids:
        message_ids.write("".join([str(new_id) + ","]))

    with open(user_ids_path , 'a') as message_user_ids:
        message_user_ids.write("".join([str(request.data["user_id"]) + ","]))

    send_att_reply(sc,request.data["user_id"],settings.PRIVATE_CHANNEL,request.data["text"], new_id)
    return HttpResponse()

#MARK : Votes s
@api_view(['POST'])
def temperature_vote(request):
    tkn = getToken()
    sc = SlackClient(tkn)
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

    send_msg_to_all.after_response(sc, request,request.data["text"], False )
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'],"".join(["You've just started the question vote: ", "*",request.data["text"], "*"]))
    return HttpResponse()

#This part is responsible for Slack Events API 
@api_view(['POST'])
def sent_message(request):
    print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)  
    t = request.data['event']['text'] 
    usr = request.data['event']['user']
    channel = request.data['event']['channel'] 
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

def send_normal_msg(request,channel, text):
    tkn = getToken()
    sc = SlackClient(tkn)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=text
    )    
    send_ephemeral_msg(sc,request.data['user_id'],request.data['channel_id'], "*Thanks*")     
    return HttpResponse()


def start_rating_vote(request, msg):
    
    tkn = getToken()
    sc = SlackClient(tkn)

    open('bot/static/users', 'w').close()
    open('bot/static/marks', 'w').close()
    open('bot/static/last_vote_name', 'w').close()

    with open("bot/static/users", "r") as text_file:
        text = text_file.read()
    
    with open("bot/static/last_vote_name", "a") as last_vote_name_file:
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
    for user in real_users:    
        send_att(sc,user.user_id,user.dm_channel, msg, is_rating)    
        

def open_channel_if_needed(sc, request, user): 
    print(request.data)
    let = sc.api_call(
        "im.open",
        user=user,
    ) 
    print(let)
    return let

def open_events_api_channel_if_needed(sc, request): 
    return sc.api_call(
        "im.open",
        user=request.data['bot_id']
    )       

def getToken():
    path = os.path.join('bot/static/noname')
    with open(path , 'r') as myfile:
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithms=[settings.CODING_ALGORITHM_NAME])
        return decoded["some"]

            
def send_ephemeral_msg(sc, user, channel, text):
    sc.api_call(
        "chat.postEphemeral",
        channel=channel,
        user=user,
        text=text
    )  

def send_att_reply(sc,user,channel,text,id):
    
    send_att_reply_attachments = [
        {
            "text": text,
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "anon_msg_reply",
            "actions": [
                {
                    "name": "game",
                    "text": "Reply",
                    "type": "button",
                    "value": id,
                    "style": "primary"
                }
            ]
        }
    ]

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        attachments=send_att_reply_attachments
    )

def send_att(sc,user,channel,text, is_rating):
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
                            "text": "10",
                            "value": "10"
                        },
                        {
                            "text": "9",
                            "value": "9"
                        },
                        {
                            "text": "8",
                            "value": "8"
                        },
                        {
                            "text": "7",
                            "value": "7"
                        },
                        {
                            "text": "6",
                            "value": "6"
                        },
                        {
                            "text": "5",
                            "value": "5"
                        },
                        {
                            "text": "4",
                            "value": "4"
                        },
                        {
                            "text": "3",
                            "value": "3"
                        },
                        {
                            "text": "2",
                            "value": "2"
                        },
                        {
                            "text": "1",
                            "value": "1"
                        }
                    ]
                }
            ]
        }
    ]

    question_attachments = [
        {
            "text": text,
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "game",
                    "text": "No, Thanks",
                    "type": "button",
                    "value": "no_tnx",
                    "style": "danger"
                },
                {
                    "name": "game",
                    "text": "Send Anon Message",
                    "type": "button",
                    "value": "anon_message",
                    "style": "primary"
                }
            ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        attachments=message_attachments if is_rating else question_attachments
    )
    