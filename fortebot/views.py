from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .errors import *
from slackclient import SlackClient
import json
import os

slack_token = ""

@api_view(['GET', 'POST'])
def messageSent(request):
    if request.method == 'POST':
        path = os.path.join('noname')
        with open(path , 'r') as myfile:
            slack_token = myfile.read()
        print(slack_token)
        return JsonResponse(request.data)
    else:
        return success_response()




sc = SlackClient(slack_token)

sc.api_call(
  "chat.postEphemeral",
  channel="#python",
  text="Hello from Python! :tada:",
  user="U0XXXXXXX"
)