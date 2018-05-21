from rest_framework.decorators import api_view
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
from slackclient import SlackClient
from tzlocal import get_localzone

def start_due():
    scheduler = BackgroundScheduler(timezone="Europe/Kiev")   

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-11 12:45:00', args=["U0WSZ2FNE", "U0PMA3TH9", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-11 16:00:00', args=["U0WSZ2FNE", "U0PMA3TH9", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-11 19:30:00', args=["U0WSZ2FNE", "U0PMA3TH9", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-11 12:45:00', args=["U0PMA3TH9", "U0WSZ2FNE", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-11 16:00:00', args=["U0PMA3TH9", "U0WSZ2FNE", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-11 19:30:00', args=["U0PMA3TH9", "U0WSZ2FNE", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-11 12:45:00', args=["U03MLGA33", "U9042TTRS", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-11 16:00:00', args=["U03MLGA33", "U9042TTRS", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-11 19:30:00', args=["U03MLGA33", "U9042TTRS", False])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-11 14:00:00', args=["U9042TTRS", "U03MLGA33", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-11 16:00:00', args=["U9042TTRS", "U03MLGA33", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-11 19:30:00', args=["U9042TTRS", "U03MLGA33", False])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-14 14:00:00', args=["U0RGZSUE9", "U0ZJBE30V", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-14 16:00:00', args=["U0RGZSUE9", "U0ZJBE30V", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-14 19:30:00', args=["U0RGZSUE9", "U0ZJBE30V", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-14 14:00:00', args=["U0ZJBE30V", "U0RGZSUE9", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-14 16:00:00', args=["U0ZJBE30V", "U0RGZSUE9", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-14 19:30:00', args=["U0ZJBE30V", "U0RGZSUE9", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-14 12:45:00', args=["U501EE1C1", "U0AKW5TQW", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-14 16:00:00', args=["U501EE1C1", "U0AKW5TQW", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-14 19:30:00', args=["U501EE1C1", "U0AKW5TQW", False])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-14 12:45:00', args=["U0AKW5TQW", "U501EE1C1", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-14 16:00:00', args=["U0AKW5TQW", "U501EE1C1", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-14 19:30:00', args=["U0AKW5TQW", "U501EE1C1", False])

    # #------------

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-15 12:45:00', args=["U1GMEJJQ5", "U1NR52JD7", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-15 16:00:00', args=["U1GMEJJQ5", "U1NR52JD7", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-15 19:30:00', args=["U1GMEJJQ5", "U1NR52JD7", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-15 12:45:00', args=["U1NR52JD7", "U1GMEJJQ5", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-15 16:00:00', args=["U1NR52JD7", "U1GMEJJQ5", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-15 19:30:00', args=["U1NR52JD7", "U1GMEJJQ5", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-15 12:45:00', args=["U1ESJL8AZ", "U0A26H59B", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-15 16:00:00', args=["U1ESJL8AZ", "U0A26H59B", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-15 19:30:00', args=["U1ESJL8AZ", "U0A26H59B", False])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-15 12:45:00', args=["U0A26H59B", "U1ESJL8AZ", False])
    # scheduler.add_job(job, 'date', run_date='2018-05-15 16:00:00', args=["U0A26H59B", "U1ESJL8AZ", False])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-15 19:30:00', args=["U0A26H59B", "U1ESJL8AZ", False])

    

    # #------------

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-16 12:45:00', args=["U1NQL0R8E", "U1SK161BR", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-16 16:00:00', args=["U1NQL0R8E", "U1SK161BR", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-16 19:30:00', args=["U1NQL0R8E", "U1SK161BR", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-16 12:45:00', args=["U1SK161BR", "U1NQL0R8E", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-16 16:00:00', args=["U1SK161BR", "U1NQL0R8E", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-16 19:30:00', args=["U1SK161BR", "U1NQL0R8E", True])

    #  #------------

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-17 12:45:00', args=["U203JLH2M", "U224S25GR", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-17 16:00:00', args=["U203JLH2M", "U224S25GR", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-17 19:30:00', args=["U203JLH2M", "U224S25GR", True])

    # scheduler.add_job(morning_job, 'date', run_date='2018-05-17 12:45:00', args=["U224S25GR", "U203JLH2M", True])
    # scheduler.add_job(job, 'date', run_date='2018-05-17 16:00:00', args=["U224S25GR", "U203JLH2M", True])
    # scheduler.add_job(evening_job, 'date', run_date='2018-05-17 19:30:00', args=["U224S25GR", "U203JLH2M", True])

    #------------
    scheduler.add_job(evening_job, 'date', run_date='2018-05-18 19:40:00', args=["U3BASC7E3", "U1XC9N9M0", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-18 19:40:00', args=["U1XC9N9M0", "U3BASC7E3", True])
    
    #------- 21 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-21 12:10:00', args=["U0NE37F25", "U0NE3297B", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-21 19:40:00', args=["U0NE37F25", "U0NE3297B", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-21 12:10:00', args=["U0NE3297B", "U0NE37F25", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-21 19:40:00', args=["U0NE3297B", "U0NE37F25", True])

    #------- 22 
    #test
    scheduler.add_job(evening_job, 'date', run_date='2018-05-22 12:10:00', args=["U6DDYBZ6Z", "U6DDYBZ6Z", True])
    #
    scheduler.add_job(morning_job, 'date', run_date='2018-05-22 12:10:00', args=["U1NQV7CCW", "U6XA6UD97", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-22 19:40:00', args=["U1NQV7CCW", "U6XA6UD97", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-22 12:10:00', args=["U6XA6UD97", "U1NQV7CCW", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-22 19:40:00', args=["U6XA6UD97", "U1NQV7CCW", True])
     #------- 23 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-23 12:10:00', args=["U1DHZQZ8E", "U7KD2UM42", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-23 19:40:00', args=["U1DHZQZ8E", "U7KD2UM42", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-23 12:10:00', args=["U7KD2UM42", "U1DHZQZ8E", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-23 19:40:00', args=["U7KD2UM42", "U1DHZQZ8E", True])
     #------- 24 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-24 12:10:00', args=["U6B7RCXGQ", "U0VEQ7P0U", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-24 19:40:00', args=["U6B7RCXGQ", "U0VEQ7P0U", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-24 12:10:00', args=["U0VEQ7P0U", "U6B7RCXGQ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-24 19:40:00', args=["U0VEQ7P0U", "U6B7RCXGQ", True])
     #------- 25 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-25 12:10:00', args=["U7KHJRNER", "U4HQU7V71", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-25 19:40:00', args=["U7KHJRNER", "U4HQU7V71", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-24 12:10:00', args=["U4HQU7V71", "U7KHJRNER", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-24 19:40:00', args=["U4HQU7V71", "U7KHJRNER", True])
   
    scheduler.add_job(evening_job, 'date', run_date='2018-05-18 18:57:00', args=["U6DDYBZ6Z", "U7KHJRNER", True])
    print("sheduler triggeredddd")

    scheduler.start()

    return HttpResponse()

def job(user_id, with_user_id, is_3rd):
    # print(job_request.data['user_id'])
    # print(job_request.data)
    print("triggered")
    tkn = getToken()
    sc = SlackClient(tkn)  
    first_user_name = get_user_realname(sc, user_id)
    another_user_name = get_user_realname_and_slack_name(sc, with_user_id)
    channel = open_channel_if_needed(sc,user_id)
    due_text = [
        {
            "text": "".join(["".join([str(first_user_name), ", не забудь, тебе на кухні чекають обовязки на", " третьому" if is_3rd else " четвертому", " поверсі і захопи заодно"]), str(another_user_name)]),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection"
        }]

    let = sc.api_call(
        "chat.postMessage",
        channel=channel["channel"]["id"],
        attachments=due_text
    )
    print("result")
    print(let)

def evening_job(user_id, with_user_id, is_3rd):
    # print(job_request.data['user_id'])
    # print(job_request.data)
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
        }]

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
            "text": "".join(["".join([str(first_user_name), ", Доброго ранку! В тебе сьогодні вдалий день, ти чергуєш на", " третьому" if is_3rd else " четвертому", " поверсі з"]), str(another_user_name)]),
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