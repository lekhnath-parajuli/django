import json
from rest_framework.decorators import api_view
from django import core
from user import models
from user import serializers
from django.shortcuts import render
from django.http import HttpResponse
from user.helpers import helpers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@csrf_exempt
@api_view(["POST"])
def register(request):
    data = serializers.Registration(**json.loads(request.body))
    if models.User.objects.filter(phone_number=data.phone_number).first():
        return HttpResponse(
            "User already Exists", content_type="text/plain", status=403
        )

    user = models.User.objects.create(
        name=data.name,
        email=data.email,
        phone_number=data.phone_number,
        password=helpers.encode_password(password=data.password.encode("UTF-8")),
    )

    serialized_user = serializers.User(
        id=user.id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
    )

    return HttpResponse(
        helpers.json_response(serialized_user),
        content_type="application/json",
        status=200,
    )
