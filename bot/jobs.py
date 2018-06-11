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

    #------- 11 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-11 12:10:00', args=["UA0DYP38W", "U9RH0Q03T", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-11 19:40:00', args=["UA0DYP38W", "U9RH0Q03T", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-11 12:10:00', args=["U9RH0Q03T", "UA0DYP38W", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-11 19:40:00', args=["U9RH0Q03T", "UA0DYP38W", True])

    #------- 12 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U9ZBZRK4L", "U9N9NPQ0L", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U9ZBZRK4L", "U9N9NPQ0L", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U9N9NPQ0L", "U9ZBZRK4L", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U9N9NPQ0L", "U9ZBZRK4L", True])

     #------- 13
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 12:10:00', args=["UA0DVRK62", "U9ZC1S9EY", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["UA0DVRK62", "U9ZC1S9EY", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 12:10:00', args=["U9ZC1S9EY", "UA0DVRK62", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U9ZC1S9EY", "UA0DVRK62", True])

    #------- 14 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["UA90MJ8FK", "UA9DPR9EX", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["UA90MJ8FK", "UA9DPR9EX", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["UA9DPR9EX", "UA90MJ8FK", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["UA9DPR9EX", "UA90MJ8FK", True])

    #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])


    # --- 4th floor
    #------- 11 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 12:10:00', args=["U03MLEVG1", "U03MNE8SG", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U03MLEVG1", "U03MNE8SG", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-04 12:10:00', args=["U03MNE8SG", "U03MLEVG1", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U03MNE8SG", "U03MLEVG1", False])

    #------- 12 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U0PMA3TH9", "U0WSZ2FNE", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U0PMA3TH9", "U0WSZ2FNE", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-05 12:10:00', args=["U0WSZ2FNE", "U0PMA3TH9", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-05 19:40:00', args=["U0WSZ2FNE", "U0PMA3TH9", False])
     #------- 13
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 12:10:00', args=["U0ZJBE30V", "U203JLH2M", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U0ZJBE30V", "U203JLH2M", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-06 12:10:00', args=["U203JLH2M", "U0ZJBE30V", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-06 19:40:00', args=["U203JLH2M", "U0ZJBE30V", False])

     #------- 14 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["U6UE195C3", "U6871AM51", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["U6UE195C3", "U6871AM51", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-07 12:10:00', args=["U6871AM51", "U6UE195C3", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-07 19:40:00', args=["U6871AM51", "U6UE195C3", False])
    
     #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U4HQU7V71", "U6B7RCXGQ", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U4HQU7V71", "U6B7RCXGQ", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-08 12:10:00', args=["U6B7RCXGQ", "U4HQU7V71", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-08 19:40:00', args=["U6B7RCXGQ", "U4HQU7V71", False])

    #test

    scheduler.add_job(evening_job, 'date', run_date='2018-06-04 19:40:00', args=["U6DDYBZ6Z", "U03MNE8SG", False])
       
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