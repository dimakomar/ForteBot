from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .errors import *
from slackclient import SlackClient
import json
import os
import jwt

slack_token = ""

@api_view(['GET', 'POST'])
def messageSent(request):
    if request.method == 'POST':
        print(request.META)
        print(request)
        # encoded = jwt.encode({'some': 'xoxb-258274331425-2FwnRFieJt51f9Wy5HtuJBAH'}, 'hello', algorithm='HS256')
        # print(encoded)
        path = os.path.join('noname')
        with open(path , 'r') as myfile:
            encoded_token = myfile.read()
            decoded = jwt.decode(encoded_token, 'hello', algorithms=['HS256'])
            slack_token = decoded['some']
            sc = SlackClient(slack_token)
            sc.api_call(
                "chat.postMessage",
                channel="#general",
                text="Hello from Python! :tada:"
            )

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