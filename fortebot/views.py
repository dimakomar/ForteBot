from django.http import HttpResponse
from .errors import *

def messageSent(request):
    print(request.body)
    return success_response()

