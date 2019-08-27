from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
from pytz import timezone
import datetime
import os
import jwt
import json
import urllib.request

from slackclient import SlackClient
from tzlocal import get_localzone
from django.conf import settings
from gspread import Client
from authlib.client import AssertionSession

def create_assertion_session():
    with open('bot/static/client_secret.json', 'r') as f:
        conf = json.load(f)

    token_url = conf['token_uri']
    issuer = conf['client_email']
    key = conf['private_key']
    key_id = conf.get('private_key_id')

    header = {'alg': 'RS256'}
    if key_id:
        header['kid'] = key_id

    # Google puts scope in payload
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    claims = {'scope': ' '.join(scopes)}
    return AssertionSession(
        grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
        token_url=token_url,
        issuer=issuer,
        audience=token_url,
        claims=claims,
        subject=None,
        key=key,
        header=header,
    )   

def start_due():
    scheduler = BackgroundScheduler(timezone="Europe/Kiev")   

    scheduler.add_job(order_meeting_room, 'cron', hour= '12', minute='00', second='00', args=[])

    scheduler.add_job(stop_food_ordering, 'cron', hour= '11', minute='00', second='05', args=[])
    scheduler.add_job(get_food_job_friday, 'cron', hour= '18', minute='00', second='00', args=[])
    scheduler.add_job(close_windows, 'cron', hour= '19', minute='45', second='05', args=[])
    scheduler.add_job(get_food_job, 'cron', hour= '18', minute='00', second='05', args=[])
    
    scheduler.start()

    return HttpResponse()

def close_windows():
    tkn = getToken()
    sc = SlackClient(tkn)
    
    now = datetime.datetime.now()  
    today_str = now.strftime("%A")
    
    if today_str == "Saturday" or today_str == "Sunday" :
        return

    room_booking_text = [
            {
                "text": "Дорогі Фортівці, велике прохання :angry_cat:\n Закривайте вікна, виключайте світло і кондиціонер після закінчення вашого робочого дня\n Вдячні за вашу уважність. :doge:",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "game_selection"
            }]

    sc.api_call(
        "chat.postMessage",
        channel='C02S31R62',
        attachments=room_booking_text
    )
    

def order_meeting_room():
    tkn = getToken()
    sc = SlackClient(tkn) 

    now = datetime.datetime.now()  
    today_str = now.strftime("%A")
    
    if today_str == "Saturday" or today_str == "Sunday" :
        return

    if today_str == "Tuesday" or today_str == "Thursday" :
        room_booking_text = [
            {
                "text": "MR 1 booked 13:00 - 14:00",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "game_selection"
            }]

        sc.api_call(
            "chat.postMessage",
            channel='C0U5X43RU',
            attachments=room_booking_text
        )

def stop_food_ordering():
    tkn = getToken()
    sc = SlackClient(tkn) 

    now = datetime.datetime.now()  
    today_str = now.strftime("%A")
    
    if today_str == "Saturday" or today_str == "Sunday" :
        return

    due_text = [
        {
            "text": "Замовлення більше не приймаються, гроші здаємо Олегу Яструбецькому або в коробку біля столу на 4 поверсі. :moneybag: здаємо до 14 години",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection"
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=due_text
    )

def get_food_job_friday():
    now = datetime.datetime.now()  
    today_str = now.strftime("%A")

    if today_str != "Friday":
        print("not friday")
        return

    session = create_assertion_session()
    client = Client(None, session)
    sheet = client.open("duty").get_worksheet(2)
    list_of_hashes = sheet.get_all_records()

    tomorrow_day = datetime.date.today() + datetime.timedelta(days=3)
    tomorrow = datetime.datetime.now().replace(month = tomorrow_day.month, day=tomorrow_day.day, hour=11, minute=00)

    tomorrow_date_str = str(tomorrow)

    tomorrow_str = tomorrow.strftime("%A")

    food_for_today = [value[tomorrow_str] for value in list_of_hashes if tomorrow_str in value]

    if len(food_for_today) != 2:
        return

    tkn = getToken()
    sc = SlackClient(tkn)

    question_attachments = [
        {
            "text": "".join(["(1 / 10)", "\n", "Приймаю замовлення на обіди у понеділок\n","🥣 - ", str(food_for_today[0]) ,"\n", "🍝 - ", str(food_for_today[1]) ,"\n", "\n", "vasyl.romaniuk", " - 65 грн" ]),
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
                    },
                    {
                        "name": "game",
                        "text": "Гроші в коробці",
                        "type": "button",
                        "value": "paid",
                        "style": "primary"
                    }
                ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=question_attachments
    )

def get_food_job():     
    now = datetime.datetime.now(timezone('Europe/Kiev'))
    today_str = now.strftime("%A")

    if today_str == "Friday" or today_str == "Saturday" or today_str == "Sunday" :
        return

    session = create_assertion_session()
    client = Client(None, session)
    sheet = client.open("duty").get_worksheet(2)
    list_of_hashes = sheet.get_all_records()

    current_day = now.day

    tomorrow_day = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow = datetime.datetime.now().replace(month = tomorrow_day.month, day=tomorrow_day.day, hour=11, minute=00)

    tomorrow_date_str = str(tomorrow)

    tomorrow_str = tomorrow.strftime("%A")

    food_for_today = [value[tomorrow_str] for value in list_of_hashes if tomorrow_str in value]

    if len(food_for_today) != 2:
        return

    tkn = getToken()
    sc = SlackClient(tkn)

    question_attachments = [
        {
            "text": "".join(["(1 / 10)", "\n", "Приймаю замовлення на завтрашні обіди\n","🥣 - ", str(food_for_today[0]) ,"\n", "🍝 - ", str(food_for_today[1]) ,"\n", "\n", "vasyl.romaniuk", " - 65 грн" ]),
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
                    },
                    {
                        "name": "game",
                        "text": "Гроші в коробці",
                        "type": "button",
                        "value": "paid",
                        "style": "primary"
                    }
                ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=question_attachments
    )

    # due_text = [
    #     {
    #         "text": "Приношу свої вітання Олегу Яструбецькому :dancing-dog: :dancing-dog: :dancing-dog: :dancing-dog: :dancing-dog: ",
    #         "color": "#3AA3E3",
    #         "attachment_type": "default",
    #         "callback_id": "game_selection"
    #     }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=due_text
    )

def get_user_job(is_3rd, is_morning):
    session = create_assertion_session()
    client = Client(None, session)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("duty").get_worksheet(0) if is_3rd else client.open("duty").get_worksheet(1)
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    now = datetime.datetime.now()
    duty_date = now.strftime("%d.%m.%Y")
    users = list(filter(lambda x: x["date"] == duty_date, list_of_hashes))
    if len(users) > 1:
        morning_job(users[0]['id'],users[1]['id'], is_3rd) if is_morning else evening_job(users[0]['id'],users[1]['id'], is_3rd)
        morning_job(users[1]['id'],users[0]['id'], is_3rd) if is_morning else evening_job(users[1]['id'],users[0]['id'], is_3rd)

def get_user_realname_and_slack_name(sc, user_id):
    user_list = sc.api_call(
        "users.list"
    )
    members_array = user_list["members"]

    for member in members_array:
        if member['id'] == user_id:
            return "".join([" ", member["profile"]["real_name"], " (", member["name"],")"])
    return ""

def get_user_realname(sc, user_id):
    user_list = sc.api_call(
        "users.list"
    )
    # print(user_list)
    members_array = user_list["members"]

    for member in members_array:
        if member['id'] == user_id:
            return "".join([" ", member["profile"]["real_name"]])
    return ""

def open_channel_if_needed(sc, user): 
    let = sc.api_call(
        "im.open",
        user=user,
    ) 
    return let

def getToken():
    return str(os.environ.get('SLACK_TOKEN'))