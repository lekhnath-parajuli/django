import json
from user import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@csrf_exempt
def register(request):
    data = serializers.User(**json.loads(request.body))
    return HttpResponse("registration done")
