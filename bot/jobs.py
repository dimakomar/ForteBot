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

    #------- 29 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-29 12:10:00', args=["U7CP33F7F", "U773HD18B", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-29 19:40:00', args=["U7CP33F7F", "U773HD18B", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-29 12:10:00', args=["U773HD18B", "U7CP33F7F", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-29 19:40:00', args=["U773HD18B", "U7CP33F7F", True])

    #------- 30 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-30 12:10:00', args=["U23J06WDQ", "U0540716R", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-30 19:40:00', args=["U23J06WDQ", "U0540716R", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-30 12:10:00', args=["U0540716R", "U23J06WDQ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-30 19:40:00', args=["U0540716R", "U23J06WDQ", True])
     #------- 31
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-05-31 16:30:00', args=["U8XTMCHNH", "U7YNB7X1P", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-31 19:40:00', args=["U8XTMCHNH", "U7YNB7X1P", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-31 16:30:00', args=["U7YNB7X1P", "U8XTMCHNH", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-31 19:40:00', args=["U7YNB7X1P", "U8XTMCHNH", True])

     #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-01 12:10:00', args=["U83FNRUQ3", "U85RV466Q", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-01 19:40:00', args=["U83FNRUQ3", "U85RV466Q", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-01 12:10:00', args=["U85RV466Q", "U83FNRUQ3", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-01 19:40:00', args=["U85RV466Q", "U83FNRUQ3", True])


    # --- 4th floor
    #------- 29 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-29 12:10:00', args=["UA0DVRK62", "U9ZC1S9EY", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-29 19:40:00', args=["UA0DVRK62", "U9ZC1S9EY", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-29 12:10:00', args=["U9ZC1S9EY", "UA0DVRK62", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-29 19:40:00', args=["U9ZC1S9EY", "UA0DVRK62", False])

    #------- 30 
    scheduler.add_job(morning_job, 'date', run_date='2018-05-30 12:10:00', args=["UA0DYP38W", "U9ZBZRK4L", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-30 19:40:00', args=["UA0DYP38W", "U9ZBZRK4L", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-30 12:10:00', args=["U9ZBZRK4L", "UA0DYP38W", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-30 19:40:00', args=["U9ZBZRK4L", "UA0DYP38W", False])
     #------- 31
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-05-31 16:30:00', args=["UA3DB10M6", "U0VEQ7P0U", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-31 19:40:00', args=["UA3DB10M6", "U0VEQ7P0U", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-05-31 16:30:00', args=["U0VEQ7P0U", "UA3DB10M6", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-05-31 19:40:00', args=["U0VEQ7P0U", "UA3DB10M6", False])

     #------- 1 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-01 12:10:00', args=["U6B7RCXGQ", "U0L2U6AQ2", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-01 19:40:00', args=["U6B7RCXGQ", "U0L2U6AQ2", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-01 12:10:00', args=["U0L2U6AQ2", "U6B7RCXGQ", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-01 19:40:00', args=["U0L2U6AQ2", "U6B7RCXGQ", False])
    

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