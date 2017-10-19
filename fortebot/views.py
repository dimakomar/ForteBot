from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .errors import *
import json

@api_view(['GET', 'POST'])
def messageSent(request):
    if request.method == 'POST':
        print(request.body)
        return success_response()
    else:
        return success_response()

