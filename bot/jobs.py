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
    scheduler.add_job(morning_job, 'date', run_date='2018-06-18 12:10:00', args=["U501EE1C1", "U0KV0CNF8", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-18 19:40:00', args=["U501EE1C1", "U0KV0CNF8", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-18 12:10:00', args=["U0KV0CNF8", "U501EE1C1", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-18 19:40:00', args=["U0KV0CNF8", "U501EE1C1", True])

    #------- 12 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-19 12:10:00', args=["U03MLGA33", "U04RYQ358", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-19 19:40:00', args=["U03MLGA33", "U04RYQ358", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-19 12:10:00', args=["U04RYQ358", "U03MLGA33", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-19 19:40:00', args=["U04RYQ358", "U03MLGA33", True])

     #------- 13
    scheduler.add_job(morning_job, 'date', run_date='2018-06-20 12:10:00', args=["U0L2U6AQ2", "U053E5FLS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-20 19:40:00', args=["U0L2U6AQ2", "U053E5FLS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-20 12:10:00', args=["U053E5FLS", "U0L2U6AQ2", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-20 19:40:00', args=["U053E5FLS", "U0L2U6AQ2", True])

    #------- 14 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-21 12:10:00', args=["U0KVD5TDJ", "U7TA5EP5Y", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-21 19:40:00', args=["U0KVD5TDJ", "U7TA5EP5Y", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-21 12:10:00', args=["U7TA5EP5Y", "U0KVD5TDJ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-21 19:40:00', args=["U7TA5EP5Y", "U0KVD5TDJ", True])

    #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-22 12:10:00', args=["U68FYTJVC", "U0FDAV8HF", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-22 19:40:00', args=["U68FYTJVC", "U0FDAV8HF", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-22 12:10:00', args=["U0FDAV8HF", "U68FYTJVC", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-22 19:40:00', args=["U0FDAV8HF", "U68FYTJVC", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-06-25 12:10:00', args=["U6UE195C3", "U6DDYBZ6Z", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-25 19:40:00', args=["U6UE195C3", "U6DDYBZ6Z", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-25 12:10:00', args=["U6DDYBZ6Z", "U6UE195C3", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-25 19:40:00', args=["U6DDYBZ6Z", "U6UE195C3", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-06-26 12:10:00', args=["U03MLE9CD", "U03LN8G2W", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-26 19:40:00', args=["U03MLE9CD", "U03LN8G2W", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-26 12:10:00', args=["U03LN8G2W", "U03MLE9CD", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-26 19:40:00', args=["U03LN8G2W", "U03MLE9CD", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-06-27 12:10:00', args=["U0KUZFVP0", "U04RZ1L76", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-27 19:40:00', args=["U0KUZFVP0", "U04RZ1L76", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-27 12:10:00', args=["U04RZ1L76", "U0KUZFVP0", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-27 19:40:00', args=["U04RZ1L76", "U0KUZFVP0", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-06-28 12:10:00', args=["U03MLF191", "U0VFULFEK", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-28 19:40:00', args=["U03MLF191", "U0VFULFEK", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-28 12:10:00', args=["U0VFULFEK", "U03MLF191", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-28 19:40:00', args=["U0VFULFEK", "U03MLF191", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-06-29 12:10:00', args=["U03MLCQ5F", "U0AKW5TQW", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-29 19:40:00', args=["U03MLCQ5F", "U0AKW5TQW", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-29 12:10:00', args=["U0AKW5TQW", "U03MLCQ5F", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-29 19:40:00', args=["U0AKW5TQW", "U03MLCQ5F", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-02 12:10:00', args=["U03MNKXD0", "U03MNPB8W", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-02 19:40:00', args=["U03MNKXD0", "U03MNPB8W", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-02 12:10:00', args=["U03MNPB8W", "U03MNKXD0", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-02 19:40:00', args=["U03MNPB8W", "U03MNKXD0", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-03 12:10:00', args=["U1XBTPLSJ", "U04E63ZQS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-03 19:40:00', args=["U1XBTPLSJ", "U04E63ZQS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-03 12:10:00', args=["U04E63ZQS", "U1XBTPLSJ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-03 19:40:00', args=["U04E63ZQS", "U1XBTPLSJ", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-04 12:10:00', args=["U6871AM51", "U1ESJL8AZ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-04 19:40:00', args=["U6871AM51", "U1ESJL8AZ", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-04 12:10:00', args=["U1ESJL8AZ", "U6871AM51", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-04 19:40:00', args=["U1ESJL8AZ", "U6871AM51", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-05 12:10:00', args=["U0A272J0J", "U0A26H59B", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-05 19:40:00', args=["U0A272J0J", "U0A26H59B", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-05 12:10:00', args=["U0A26H59B", "U0A272J0J", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-05 19:40:00', args=["U0A26H59B", "U0A272J0J", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-06 12:10:00', args=["U03MLGSUD", "U0WSZ2FNE", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-06 19:40:00', args=["U03MLGSUD", "U0WSZ2FNE", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-06 12:10:00', args=["U0WSZ2FNE", "U03MLGSUD", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-06 19:40:00', args=["U0WSZ2FNE", "U03MLGSUD", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-09 12:10:00', args=["U03MNAAFL", "U03MLH4C9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-09 19:40:00', args=["U03MNAAFL", "U03MLH4C9", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-09 12:10:00', args=["U03MLH4C9", "U03MNAAFL", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-09 19:40:00', args=["U03MLH4C9", "U03MNAAFL", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-10 12:10:00', args=["U03MLEVG1", "U03MNAKHQ", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-10 19:40:00', args=["U03MLEVG1", "U03MNAKHQ", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-10 12:10:00', args=["U03MNAKHQ", "U03MLEVG1", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-10 19:40:00', args=["U03MNAKHQ", "U03MLEVG1", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-11 12:10:00', args=["U02S32ZT0", "U03MLEV4P", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-11 19:40:00', args=["U02S32ZT0", "U03MLEV4P", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-11 12:10:00', args=["U03MLEV4P", "U02S32ZT0", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-11 19:40:00', args=["U03MLEV4P", "U02S32ZT0", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-12 12:10:00', args=["U03MNE8SG", "U1NL21RMH", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-12 19:40:00', args=["U03MNE8SG", "U1NL21RMH", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-12 12:10:00', args=["U1NL21RMH", "U03MNE8SG", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-12 19:40:00', args=["U1NL21RMH", "U03MNE8SG", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-13 12:10:00', args=["U0PMA3TH9", "U03MN93SN", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-13 19:40:00', args=["U0PMA3TH9", "U03MN93SN", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-13 12:10:00', args=["U03MN93SN", "U0PMA3TH9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-13 19:40:00', args=["U03MN93SN", "U0PMA3TH9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-16 12:10:00', args=["U0RGZSUE9", "U03LPHT2C", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-16 19:40:00', args=["U0RGZSUE9", "U03LPHT2C", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-16 12:10:00', args=["U03LPHT2C", "U0RGZSUE9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-16 19:40:00', args=["U03LPHT2C", "U0RGZSUE9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-17 12:10:00', args=["U1GMEJJQ5", "U1NR52JD7", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-17 19:40:00', args=["U1GMEJJQ5", "U1NR52JD7", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-17 12:10:00', args=["U1NR52JD7", "U1GMEJJQ5", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-17 19:40:00', args=["U1NR52JD7", "U1GMEJJQ5", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-18 12:10:00', args=["U1NQL0R8E", "U1SK161BR", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-18 19:40:00', args=["U1NQL0R8E", "U1SK161BR", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-18 12:10:00', args=["U1SK161BR", "U1NQL0R8E", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-18 19:40:00', args=["U1SK161BR", "U1NQL0R8E", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-19 12:10:00', args=["U203JLH2M", "UA0DVRK62", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-19 19:40:00', args=["U203JLH2M", "UA0DVRK62", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-19 12:10:00', args=["UA0DVRK62", "U203JLH2M", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-19 19:40:00', args=["UA0DVRK62", "U203JLH2M", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-20 12:10:00', args=["U773HD18B", "U9ZC1S9EY", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-20 19:40:00', args=["U773HD18B", "U9ZC1S9EY", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-20 12:10:00', args=["U9ZC1S9EY", "U773HD18B", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-20 19:40:00', args=["U9ZC1S9EY", "U773HD18B", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-23 12:10:00', args=["U3BASC7E3", "UA0DYP38W", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-23 19:40:00', args=["U3BASC7E3", "UA0DYP38W", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-23 12:10:00', args=["UA0DYP38W", "U3BASC7E3", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-23 19:40:00', args=["UA0DYP38W", "U3BASC7E3", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-24 12:10:00', args=["U1XC9N9M0", "U9ZBZRK4L", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-24 19:40:00', args=["U1XC9N9M0", "U9ZBZRK4L", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-24 12:10:00', args=["U9ZBZRK4L", "U1XC9N9M0", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-24 19:40:00', args=["U9ZBZRK4L", "U1XC9N9M0", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-25 12:10:00', args=["U0NE37F25", "UA90MJ8FK", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-25 19:40:00', args=["U0NE37F25", "UA90MJ8FK", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-25 12:10:00', args=["UA90MJ8FK", "U0NE37F25", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-25 19:40:00', args=["UA90MJ8FK", "U0NE37F25", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-26 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-26 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-26 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-26 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-27 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-27 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-27 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-27 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-30 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-30 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-30 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-30 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-07-31 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-31 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-07-31 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-07-31 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-01 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-01 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-01 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-01 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-02 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-02 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-02 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-02 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])
    
    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-03 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-03 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-03 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-03 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-06 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-06 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-06 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-06 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-07 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-07 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-07 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-07 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-08 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-08 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-08 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-08 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-09 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-09 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-09 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-09 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-10 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-10 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-10 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-10 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

#----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-13 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-13 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-13 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-13 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-14 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-14 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-14 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-14 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-15 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-15 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-15 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-15 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-16 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-16 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-16 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-16 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-17 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-17 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-17 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-17 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-20 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-20 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-20 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-20 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    #----
    scheduler.add_job(morning_job, 'date', run_date='2018-08-21 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-21 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-08-21 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-08-21 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

    # --- 4th floor
    #------- 11 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-11 12:10:00', args=["U03MLEVG1", "U03MNE8SG", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-11 19:40:00', args=["U03MLEVG1", "U03MNE8SG", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-11 12:10:00', args=["U03MNE8SG", "U03MLEVG1", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-11 19:40:00', args=["U03MNE8SG", "U03MLEVG1", False])

    #------- 12 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-12 12:10:00', args=["U0PMA3TH9", "U0WSZ2FNE", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-12 19:40:00', args=["U0PMA3TH9", "U0WSZ2FNE", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-12 12:10:00', args=["U0WSZ2FNE", "U0PMA3TH9", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-12 19:40:00', args=["U0WSZ2FNE", "U0PMA3TH9", False])
     #------- 13
     #  
    scheduler.add_job(morning_job, 'date', run_date='2018-06-13 12:10:00', args=["U0ZJBE30V", "U203JLH2M", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-13 19:40:00', args=["U0ZJBE30V", "U203JLH2M", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-13 12:10:00', args=["U203JLH2M", "U0ZJBE30V", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-13 19:40:00', args=["U203JLH2M", "U0ZJBE30V", False])

     #------- 14 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-14 12:10:00', args=["U6UE195C3", "U6871AM51", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-14 19:40:00', args=["U6UE195C3", "U6871AM51", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-14 12:10:00', args=["U6871AM51", "U6UE195C3", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-14 19:40:00', args=["U6871AM51", "U6UE195C3", False])
    
     #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-15 12:10:00', args=["U4HQU7V71", "U6B7RCXGQ", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-15 19:40:00', args=["U4HQU7V71", "U6B7RCXGQ", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-15 12:10:00', args=["U6B7RCXGQ", "U4HQU7V71", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-15 19:40:00', args=["U6B7RCXGQ", "U4HQU7V71", False])

    #test

    scheduler.add_job(evening_job, 'date', run_date='2018-06-11 19:40:00', args=["U6DDYBZ6Z", "U03MNE8SG", False])

    #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-15 12:10:00', args=["U8MKB1SU9", "U9042TTRS", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-15 19:40:00', args=["U8MKB1SU9", "U9042TTRS", True])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-15 12:10:00', args=["U9042TTRS", "U8MKB1SU9", True])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-15 19:40:00', args=["U9042TTRS", "U8MKB1SU9", True])

     #------- 15 
    scheduler.add_job(morning_job, 'date', run_date='2018-06-18 12:10:00', args=["U8WHXDMG9", "U03LN8G2W", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-18 19:40:00', args=["U8WHXDMG9", "U03LN8G2W", False])
    
    scheduler.add_job(morning_job, 'date', run_date='2018-06-18 12:10:00', args=["U03LN8G2W", "U8WHXDMG9", False])
    scheduler.add_job(evening_job, 'date', run_date='2018-06-18 19:40:00', args=["U03LN8G2W", "U8WHXDMG9", False])
       
    print("sheduler trigageredddd")
    scheduler.start()

    return HttpResponse()



def job(user_id, with_user_id, is_3rd):
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