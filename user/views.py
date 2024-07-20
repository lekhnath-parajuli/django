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
            "User already Exists",
            content_type="text/plain",
            status=403,
        )

    user = models.User.objects.create(
        name=(data.name or "").strip(),
        email=(data.email or "").strip(),
        phone_number=(data.phone_number or "").strip(),
        password=helpers.encode_password(
            password=(data.password or "").strip().encode("UTF-8")
        ),
    )

    models.Contact.objects.create(
        name=data.name,
        user_id=user,
        phone_number=data.phone_number,
    )

    serialized_user = serializers.User(
        id=user.id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
    )

    return HttpResponse(
        helpers.json_response(serialized_user.__dict__()),
        content_type="application/json",
        status=200,
    )


@csrf_exempt
@api_view(["POST"])
def login(request):
    data = serializers.Login(**json.loads(request.body))
    user = models.User.objects.filter(
        name=data.name,
        password=helpers.encode_password(
            password=(data.password or "").strip().encode("UTF-8")
        ),
    ).first()

    if not user:
        return HttpResponse(
            "Wrong username/password",
            content_type="text/plain",
            status=403,
        )

    access_token = helpers.generate_jwt_token(user_id=str(user.id))
    return HttpResponse(
        helpers.json_response({"access_token": access_token}),
        content_type="application/json",
        status=200,
    )
