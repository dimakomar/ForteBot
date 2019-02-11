from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from pytz import utc
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

    scheduler.add_job(get_food_job, 'cron', hour= '16', minute='09', second='10', args=[])

    scheduler.add_job(get_user_job, 'cron', hour= '12', minute='10', args=[False, True])
    scheduler.add_job(get_user_job, 'cron', hour='19', minute='45', args=[False, False])

    scheduler.add_job(get_user_job, 'cron', hour='12', minute='10', args=[True, True])
    scheduler.add_job(get_user_job, 'cron', hour='19', minute='45', args=[True, False])
    
    scheduler.start()

    return HttpResponse()

def get_food_job():
    session = create_assertion_session()
    client = Client(None, session)
    sheet = client.open("duty").get_worksheet(2)
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)

    now = datetime.datetime.now()    

    current_day = now.day

    tomorrow = datetime.datetime.now().replace(day=current_day+1, hour=11, minute=00)

    tomorrow_date_str = str(tomorrow)

    tomorrow_str = tomorrow.strftime("%A")

    food_for_today = [value[tomorrow_str] for value in list_of_hashes if tomorrow_str in value]

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

def open_channel_if_needed(sc, user): 
    let = sc.api_call(
        "im.open",
        user=user,
    ) 
    return let

def food_job(day, index_val):
    tkn = getToken()
    sc = SlackClient(tkn)

    monday_dict = {
        "1": "🥣 - Бульйон курячий,\n Ціна: 14.00 грн \n",
        "2": "🥣 - Філе курки тушене в томатно-соєвому соусі з макаронами,\n Ціна: 27.00 грн \n",
        "3": "🥣 - Плов \n Ціна: 27.00 грн",
        "4": "🥣 - Салат з капусти , огірків і болг.перцю \n Ціна: 78 грн",
        "5": "🥣 - Млинці з маком і медом \n Ціна: 20.00 грн"
    }

    tuesday_dict = {
        "1": "🥣 - Розсольник,\n Ціна: 14.00 грн",
        "2": "🥣 - Свинина тушена з болгарським перцем з гороховим пюре,\n Ціна: 27.00 грн",
        "3": "🥣 - Шніцель з овочевим рагу \n Ціна: 27.00 грн",
        "4": "🥣 - Салат з помідорів зі сметаною \n Ціна: 11.00 грн",
        "5": "🥣 - Штрудель з яблуками  і сливами з шоколадним кремом \n Ціна:  20.00 грн"
    }

    wednesday_dict = {
        "1": "🥣 - Сирна юшка,\n Ціна: 14.00 грн",
        "2": "🥣 - Гречаники з м”ясом,\n Ціна: 27.00 грн",
        "3": "🥣 - Макарони по-флотськи \n Ціна: 27.00 грн",
        "4": "🥣 - Салат з бурячка \n Ціна: 11.00 грн",
        "5":""
    }

    thursday_dict = {
        "1": "🥣 - Суп овочевий\n Ціна: 14.00 грн",
        "2": "🥣 - Січеники з тушеною картоплею\n Ціна: 27.00 грн",
        "3": "🥣 - ТТушена курка з грибами і з макаронами \n Ціна: 27.00 грн",
        "4": "🥣 - Салат з капусти з крабовими паличками і кукурузкою \n Ціна: 12.00 грн",
        "5": "🥣 - Млинці з сиром і малиною зі сметаною \n Ціна: 20.00 грн"
    }

    friday_dict = {
        "1": "🥣 - Борщ зелений\n Ціна: 14.00 грн \n",
        "2": "🥣 - М”ясні зрази(начинка яйце,голандський сир ,зелень) з тушеною картоплею\n Ціна: 27.00 грн \n",
        "3": "🥣 - Тушена печінка  з гречкою \n Ціна:  25.00 грн",
        "4": "🥣 - Салат “Дністер” \n Ціна: 12.00 грн",
        "5": "🥣 - Штрудель з грушами і вишнями зі згущонкою \n Ціна: 20.00 грн"
    }

    menu_dict = {
        "Friday": friday_dict[index_val],
        "Monday": monday_dict[index_val],
        "Tuesday": tuesday_dict[index_val],
        "Wednesday": wednesday_dict[index_val],
        "Thursday": thursday_dict[index_val]
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

    # print(question_attachments[0]['text'])
    if question_attachments[0]['text'] is not '':
        sc.api_call(
            "chat.postMessage",
            channel='GCR6G6DRD',
            attachments=question_attachments
        )
def getToken():
    return str(os.environ.get('SLACK_TOKEN'))