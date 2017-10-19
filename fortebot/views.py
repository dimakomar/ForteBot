from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .errors import *
import json

@api_view(['GET', 'POST'])
def messageSent(request):
    if request.method == 'POST':
        return JsonResponse(request.data)
    else:
        return success_response()

