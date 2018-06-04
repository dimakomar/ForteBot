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
from slackclient import SlackClient
from tzlocal import get_localzone
from django.conf import settings


def start_due():
    scheduler = BackgroundScheduler(timezone="Europe/Kiev")   

    #------- 04 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 15:05:00', args=["U1NRJF17S", "U03MN93SN", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U1NRJF17S", "U03MN93SN", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 15:05:00', args=["U03MN93SN", "U1NRJF17S", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U03MN93SN", "U1NRJF17S", True])

    #------- 05 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U8WHXDMG9", "U03MNPB8W", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U8WHXDMG9", "U03MNPB8W", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U03MNPB8W", "U8WHXDMG9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U03MNPB8W", "U8WHXDMG9", True])
     #------- 31
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 15:20:00', args=["U7Z9CBJ12", "U83KA4JVA", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U7Z9CBJ12", "U83KA4JVA", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 15:20:00', args=["U83KA4JVA", "U7Z9CBJ12", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U83KA4JVA", "U7Z9CBJ12", True])

     #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["U9X2V0RRT", "UA0E01NGN", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["U9X2V0RRT", "UA0E01NGN", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["UA0E01NGN", "U9X2V0RRT", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["UA0E01NGN", "U9X2V0RRT", True])

    #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["UA0DVRK62", "U9ZC1S9EY", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["UA0DVRK62", "U9ZC1S9EY", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U9ZC1S9EY", "UA0DVRK62", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U9ZC1S9EY", "UA0DVRK62", True])


    # --- 4th floor
    #------- 29 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 15:05:00', args=["U6DDYBZ6Z", "U03MLE9CD", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U6DDYBZ6Z", "U03MLE9CD", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 15:05:00', args=["U03MLE9CD", "U6DDYBZ6Z", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U03MLE9CD", "U6DDYBZ6Z", False])

    #------- 30 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U8XTMCHNH", "U03MLGA33", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U8XTMCHNH", "U03MLGA33", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U03MLGA33", "U8XTMCHNH", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U03MLGA33", "U8XTMCHNH", False])
     #------- 31
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 15:20:00', args=["U9042TTRS", "U501EE1C1", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U9042TTRS", "U501EE1C1", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 15:20:00', args=["U501EE1C1", "U9042TTRS", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U501EE1C1", "U9042TTRS", False])

     #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["U0AKW5TQW", "U1ESJL8AZ", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["U0AKW5TQW", "U1ESJL8AZ", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["U1ESJL8AZ", "U0AKW5TQW", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["U1ESJL8AZ", "U0AKW5TQW", False])
    
     #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U0A26H59B", "U03MNAKHQ", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U0A26H59B", "U03MNAKHQ", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U03MNAKHQ", "U0A26H59B", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U03MNAKHQ", "U0A26H59B", False])

    #test

    scheduler.add_job(morning_job, 'date', run_date='2018-05-29 19:45:00', args=["U6DDYBZ6Z", "UA0DVRK62", False])
    scheduler.add_job(morning_job, 'date', run_date='2018-05-30 12:10:00', args=["U6DDYBZ6Z", "U0540716R", False])
       
    print("sheduler trigageredddd")
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
            "text": "".join(["".join([str(first_user_name), ", Доброго ранку! В тебе сьогодні вдалий день, ти чергуєш на", " третьому" if is_3rd else " четвертому", " поверсі з"]), str(another_user_name), " :dancingpony:"]),
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