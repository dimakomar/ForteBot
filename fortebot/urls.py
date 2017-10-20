"""fortebot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from fortebot import views
import schedule 
import jwt
import os
from fortebot.settings import SLACK_BOT_TOKEN

from datetime import datetime
from threading import Timer

x=datetime.today()
y=x.replace(day=x.day+0, hour=0, minute=0, second=3, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def hello_world():
    print("hello world")



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^slack/', views.messageSent),
]

t = Timer(secs, hello_world)
t.start()