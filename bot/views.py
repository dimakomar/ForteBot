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
import time
import datetime
import jwt
from .user import User
from mixpanel import Mixpanel
import after_response
from time import sleep
from urllib.parse import urlencode, quote_plus
import urllib.request
from .models import Message
from requests.auth import HTTPBasicAuth
from time import gmtime, strftime
import requests 


@api_view(['GET'])
def auth(request):
    print(request.data)
    return HttpResponse()

@api_view(['POST'])
def click(request):
    tkn = getToken()
    sc = SlackClient(tkn)

    value = ""
    result = json.loads(request.data["payload"])
    if result["actions"][0]["type"] == "button":
        value = result["actions"][0]["value"]
    else:
        value = result["actions"][0]["selected_options"][0]["value"]    

    callback_id = result["callback_id"]  
    ts = result["message_ts"]
    user = result["user"]["id"]
    channel = result["channel"]["id"]
    attachment_text = result["original_message"]["attachments"][0]["text"]
    callback_id = result["original_message"]["attachments"][0]["callback_id"]

    if value == "rejected_food":
        deleted_text = attachment_text.replace("".join(["\n", result["user"]["name"]," - 65 грн"]),'')
        
        
        users_count = len(list(filter(lambda x: x == "грн", deleted_text.split())))
        
        if not users_count:
            text_for_replacing = "(1 / 10)"
            deleted_text = deleted_text.replace(text_for_replacing,'')            

        if users_count:
            text_before_replacing = "".join(["(",str(users_count + 1)," / 10)"])
            text_for_replacing = "".join(["(",str(users_count)," / 10)"])
            deleted_text = deleted_text.replace(text_before_replacing,text_for_replacing)
        
        updated_attachments = [
        {
            "text": deleted_text,
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": callback_id,
            "actions": [
                {
                    "name": "game",
                    "text": "Замовити",
                    "type": "button",
                    "value": "get_food",
                    "style": "primary"
                },
                {
                    "name": "game",
                    "text": "Відмовитись",
                    "type": "button",
                    "value": "rejected_food",
                    "style": "danger"
                }
            ]
        }]

        sc.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        attachments=updated_attachments)

    if value == "get_food":
        due_date = datetime.datetime.strptime(callback_id, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()

        if now > due_date:
            sc.api_call(
            "chat.postEphemeral",
            channel='C0G5R2BKL',
            user=user,
            text="Вже пізно сорян")
            return HttpResponse()

        if result["user"]["name"] in attachment_text: 
            return HttpResponse()       

        users_count = len(list(filter(lambda x: x == "грн", attachment_text.split())))
        if users_count != 0:
            text_before_replacing = "".join(["(",str(users_count)," / 10)"])
            text_for_replacing = "".join(["(",str(users_count + 1)," / 10)"])
            attachment_text = attachment_text.replace(text_before_replacing,text_for_replacing)    

        updated_attachments = [
            {
                "text": "".join([attachment_text, "\n", result["user"]["name"], " - 65 грн"]),
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": callback_id,
                "actions": [
                    {
                        "name": "game",
                        "text": "Замовити",
                        "type": "button",
                        "value": "get_food",
                        "style": "primary"
                    },
                    {
                        "name": "game",
                        "text": "Відмовитись",
                        "type": "button",
                        "value": "rejected_food",
                        "style": "danger"
                    }
                ]
            }
        ]

        users_count = len(list(filter(lambda x: x == "грн", attachment_text.split())))

        if users_count == 0:
            text_for_replacing = "(1 / 10)\n"
            updated_attachments[0]["text"] = "".join([text_for_replacing, updated_attachments[0]["text"]])

        sc.api_call(
        "chat.update",
        channel=channel,
        ts=ts,
        attachments=updated_attachments)

        sc.api_call(
        "chat.postEphemeral",
        channel='C0G5R2BKL',
        user=user,
        text="Замовлення прийнято, гроші здаємо Олегу Яструбецькому або в коробку біля столу на 4 поверсі. Прохання гроші здавати до 14:00") 
        #oleg id  UEBRV4AJX
        #my id  U6DDYBZ6Z
        channel = open_channel_if_needed(sc, "U6DDYBZ6Z")
        print(channel)
        print(users_count)
        if users_count == 9:
            sc.api_call(
            "chat.postMessage",
            user="U6DDYBZ6Z",
            text="Обіди тільки що замовило 10 чоловік") 
        
    
    if value == "privat24":      

        updated_attachments = [
                        {
                "attachments": [
                    {
                        "fallback": "Required plain-text summary of the attachment.",
                        "color": "#36a64f",
                        "pretext": "Optional text that appears above the attachment block",
                        "author_name": "Bobby Tables",
                        "author_link": "http://flickr.com/bobby/",
                        "author_icon": "http://flickr.com/icons/bobby.jpg",
                        "title": "Slack API Documentation",
                        "title_link": "https://api.slack.com/",
                        "text": "Optional text that appears within the attachment",
                        "fields": [
                            {
                                "title": "Priority",
                                "value": "High",
                                "short": False
                            }
                        ],
                        "image_url": "https://firebasestorage.googleapis.com/v0/b/profileborder-2b1e7.appspot.com/o/Screen%20Shot%202018-07-13%20at%206.47.59%20PM.png?alt=media&token=700378c3-3d08-4909-a06d-c24132283e84",
                        "thumb_url": "http://example.com/path/to/thumb.png",
                        "footer": "Slack API",
                        "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                        "ts": 123456789
                    }
                ]
            }
        ]

        sc.api_call(
        "chat.postEphemeral",
        channel=channel,
        attachments=updated_attachments,
        user=user)
    return HttpResponse()

@api_view(['POST'])
def help(request):
    tkn = getToken()
    print(tkn)
    sc = SlackClient(tkn)
    

    question_attachments = [
        {
            "text": "отаке от меню сьогодни",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "game",
                    "text": "Замовити",
                    "type": "button",
                    "value": "get_food",
                    "style": "primary"
                },
                {
                    "name": "game",
                    "text": "Відмовитись",
                    "type": "button",
                    "value": "rejected_food",
                    "style": "danger"
                }
            ]
        }]

    # print(question_attachments[0]['text'])
    chan = sc.api_call(
        "channels.list",
    )
    print(chan)

    # tts_token = "Basic " + str(os.environ.get('TTS_TOKEN'))
    # data = requests.get('https://timeqa.fortegrp.com:58443/http-basic-api/v1/slack-bot-ua/users-having-time-off?date=2018-10-01', headers={"Authorization":tts_token})
    # binary = data.content
    # output = json.loads(binary)
    # print(output)
    
    return HttpResponse()



@api_view(['POST'])
def delivery(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    channel = open_channel_if_needed(sc, request.data['user_id'])
    send_ephemeral_msg(sc, request.data['user_id'], channel["channel"]["id"], settings.DUE_INFO)  
    return HttpResponse()

@api_view(['POST'])
def get_results(request):
    food_job("Monday")

@api_view(['POST'])
def get_id(request):
    print("1")
    tkn = getToken()
    sc = SlackClient(tkn)
    users_list = sc.api_call(
        "users.list",
    ) 
    # print(users_list["members"])
    user_list = list(filter(lambda x: x['profile']['display_name'] == request.data["text"], users_list["members"]))
    if  len(user_list) > 0:
        send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], "".join([ request.data["text"], " id `", user_list[0]['id'], "`"])) 
    else: 
        send_ephemeral_msg(sc, request.data['user_id'], request.data['channel_id'], '`user not fount`') 
    return HttpResponse()

@api_view(['POST'])
def reply(request):
    tkn = getToken()
    sc = SlackClient(tkn)

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
    
    channel = open_channel_if_needed(sc,user_id)
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

@api_view(['POST'])
def anon_random(request):
    tkn = getToken()
    sc = SlackClient(tkn)
    send_att_reply_attachments = [
        {
            "text": "".join([':secret_santa:: ',request.data["text"]]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "none",
            "mrkdwn_in": [
                "text"
            ]
        }
    ]

    sc.api_call(
        "chat.postMessage",
        channel="C8E34CTMJ",
        attachments=send_att_reply_attachments
    )
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
    # print(request.data)
    tkn = getToken()
    sc = SlackClient(tkn)  

    if "username" in request.data['event']:
        return HttpResponse()
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

def send_normal_duty_msg(sc,channel, text):
    sc.api_call(
        "chat.postMessage",
        channel=channel['channel']['id'],
        text=text
    )    
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
        

def open_channel_if_needed(sc, user): 
    let = sc.api_call(
        "im.open",
        user=user,
    ) 
    return let

def open_events_api_channel_if_needed(sc, request): 
    return sc.api_call(
        "im.open",
        user=request.data['bot_id']
    )


def getToken():
    return str(os.environ.get('SLACK_TOKEN'))

            
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
            # "actions": [
            #     {
            #         "name": "game",
            #         "text": "Reply",
            #         "type": "button",
            #         "value": id,
            #         "style": "primary"
            #     }
            # ]
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
    

@api_view(['POST'])
def food_job(day):
    tkn = getToken()
    sc = SlackClient(tkn)

    menu_dict = {
        "Monday": "Меню на сьогодні: Крем суп з беконом, Равіолі з шпинатом, Салат фета \n Ціна: 78 грн",
        "Tuesday": "text2",
        "Wednesday": "text3",
        "Thursday": "text4",
        "Frieday": "text5",
    }

    question_attachments = [
        {
            "text": menu_dict[day],
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "game",
                    "text": "Замовити",
                    "type": "button",
                    "value": "get_food",
                    "style": "primary"
                },
                {
                    "name": "game",
                    "text": "Відмовитись",
                    "type": "button",
                    "value": "rejected_food",
                    "style": "danger"
                },
                {
                    "name": "game",
                    "text": "Заплатити з Приват24",
                    "type": "button",
                    "value": "privat24",
                    "style": "primary"
                }
            ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C7PJLSVC2',
        attachments=question_attachments
    )
    return HttpResponse()

    def get_food_job():
        now = datetime.datetime.now()  
    today_str = now.strftime("%A")

    if today_str == "Friday":
        return

    session = create_assertion_session()
    client = Client(None, session)
    sheet = client.open("duty").get_worksheet(2)
    list_of_hashes = sheet.get_all_records()

    current_day = now.day

    tomorrow = datetime.datetime.now().replace(day=current_day+1, hour=11, minute=00)

    tomorrow_date_str = str(tomorrow)

    tomorrow_str = tomorrow.strftime("%A")

    food_for_today = [value[tomorrow_str] for value in list_of_hashes if tomorrow_str in value]

    if len(food_for_today) != 2:
        return

    tkn = getToken()
    sc = SlackClient(tkn)

    question_attachments = [
        {
            "text": "".join(["Приймаю замовлення на завтрашні обіди\n","🥣 - ", str(food_for_today[0]) ,"\n", "🍝 - ", str(food_for_today[1]) ,"\n" ]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": tomorrow_date_str,
            "actions": [
                {
                    "name": "game",
                    "text": "Замовити",
                    "type": "button",
                    "value": "get_food",
                    "style": "primary"
                },
                {
                    "name": "game",
                    "text": "Відмовитись",
                    "type": "button",
                    "value": "rejected_food",
                    "style": "danger"
                }
            ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=question_attachments
    )
    return HttpResponse()