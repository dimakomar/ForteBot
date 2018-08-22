# from rest_framework.decorators import api_view
from django.http import HttpResponse
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
import datetime
import os
import jwt
import json

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

    scheduler.add_job(get_user_job, 'cron', hour= '12', minute='10', args=[False, True])
    scheduler.add_job(get_user_job, 'cron', hour='19', minute='45', args=[False, False])

    scheduler.add_job(get_user_job, 'cron', hour='12', minute='10', args=[True, True])
    scheduler.add_job(get_user_job, 'cron', hour='19', minute='45', args=[True, False])
    
    # scheduler.add_job(evening_job, 'date', run_date='2018-08-22 19:40:00', args=["U7F85AA80", "U7F85AA80", False]
    print("sheduler trigageredddd")
    scheduler.start()

    return HttpResponse()

def get_user_job(is_3rd, is_morning):
    session = create_assertion_session()
    client = Client(None, session)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("duty").sheet1 if is_3rd else client.open("duty").sheet1
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    now = datetime.datetime.now()
    duty_date = now.strftime("%d.%m.%Y")
    print(duty_date)
    users = list(filter(lambda x: x["date"] == duty_date, list_of_hashes))

    if len(users) > 1:
        morning_job(users[0]['id'],users[1]['id'], is_3rd) if is_morning else evening_job(users[0]['id'],users[1]['id'], is_3rd)
        morning_job(users[1]['id'],users[0]['id'], is_3rd) if is_morning else evening_job(users[1]['id'],users[0]['id'], is_3rd)
    

def evening_job(user_id, with_user_id, is_3rd):
    # print(job_request.data['user_id'])
    tkn = getToken()
    sc = SlackClient(tkn)  
    first_user_name = get_user_realname(sc, user_id)
    channel = open_channel_if_needed(sc,user_id)
    due_text = [
        {
            "text": "".join(["".join([str(first_user_name), " закінчується робочий день і також твоє чергування на", " третьому" if is_3rd else " четвертому", " поверсі, але не забудь винести сміття!! До скорої зустрічі :happycat: "])]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection"
        }
    ]

    let = sc.api_call(
        "chat.postMessage",
        channel=channel["channel"]["id"],
        attachments=due_text
    )

def morning_job(user_id, with_user_id, is_3rd):
    tkn = getToken()
    sc = SlackClient(tkn)  
    first_user_name = get_user_realname(sc, user_id)
    another_user_name = get_user_realname_and_slack_name(sc, with_user_id)
    channel = open_channel_if_needed(sc,user_id)
    due_text = [
        {
            "text": "".join(["".join([str(first_user_name), ", Доброго ранку! В тебе сьогоднi вдалий день, ти чергуєш на", " третьому" if is_3rd else " четвертому", " поверсі з"]), str(another_user_name), " :dancingpony:"]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection"
        }]

    let = sc.api_call(
        "chat.postMessage",
        channel=channel["channel"]["id"],
        attachments=due_text
    )

def failed_morning_job(user_id, with_user_id, is_3rd):
    tkn = getToken()
    sc = SlackClient(tkn)  
    first_user_name = get_user_realname(sc, user_id)
    another_user_name = get_user_realname_and_slack_name(sc, with_user_id)
    channel = open_channel_if_needed(sc,user_id)
    due_text = [
        {
            "text": "".join(["".join([str(first_user_name), ", Доброго ранку! Вчора це був пранк про чергування, а сьогоднi в тебе вдалий день, ти чергуєш на", " третьому" if is_3rd else " четвертому", " поверсі з"]), str(another_user_name), " :dancingpony:"]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection"
        }]

    let = sc.api_call(
        "chat.postMessage",
        channel=channel["channel"]["id"],
        attachments=due_text
    )

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

def getToken():
    path = os.path.join('bot/static/noname')
    with open(path , 'r') as myfile:
        encoded_token = myfile.read()
        decoded = jwt.decode(encoded_token, 'hello', algorithm='HS256')
        return decoded["some"]

def open_channel_if_needed(sc, user): 
    let = sc.api_call(
        "im.open",
        user=user,
    ) 
    return let
    
def food_job(day):
    tkn = getToken()
    sc = SlackClient(tkn)

    menu_dict = {
        "Friday": "Меню на понеділок: \n🥣 - Бульйон курячий, \n🍝 - Равіолі ай порчіні, \n🥗 - Салат Цезар, \n Ціна: 78 грн",
        "Monday": "Меню на завтра: \n🥣 - Крем суп з беконом, \n🍝 - Спагеті Карбонара, \n🥗 - Інсалада ді Вітелло \n Ціна: 78 грн",
        "Tuesday": "Меню на завтра: \n🥣 - Крема ді порчіні, \n🍝 - Спагеті Болоньєзе, \n🥗 - Інсалада ді Фета \n Ціна: 78 грн",
        "Wednesday": "Меню на завтра: \n🥣 - Бульйон з равіолі з м'ясом кролика, \n🍝 - Фетучуні з грибами і шинкою, \n🥗 - Інсалада ді Прошуто \n Ціна: 78 грн",
        "Thursday": "Меню на завтра: \n🥣 - Крем суп з беконом, \n🍝 - Равіолі з шпинатом та рікотою, \n🥗 - Інсалата Капрезе \n Ціна: 78 грн"
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
                }
            ]
        }]

    sc.api_call(
        "chat.postMessage",
        channel='C0G5R2BKL',
        attachments=question_attachments
    )