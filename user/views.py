import json
import uuid
from funcy import project
from rest_framework.decorators import api_view
from django import core
from user import models
from user import serializers
from django.shortcuts import render
from django.http import HttpResponse
from user.helpers import helpers
from django.views.decorators.csrf import csrf_exempt


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

    contact = models.Contact.objects.create(
        name=data.name,
        phone_number=data.phone_number,
    )

    models.UserContact.objects.create(user_id=user, contact_id=contact)

    return HttpResponse(
        helpers.json_response(serializers.User(user.__dict__()).__dict__()),
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


@csrf_exempt
@api_view(["POST"])
@helpers.validate_access_token
def contact_create(request):
    user_id = request.META["PROFILE"]
    data = serializers.CreateContact(**{**json.loads(request.body)})
    contact = models.Contact.objects.filter(phone_number=data.phone_number).first()
    contact_id = getattr(contact, "id", None)
    user_contact = models.UserContact.objects.filter(contact_id=contact_id).first()

    if contact and user_contact:
        return HttpResponse(
            "Contact already Exists",
            content_type="text/plain",
            status=403,
        )

    if not contact:
        contact = models.Contact.objects.create(
            name=data.name, phone_number=data.phone_number
        )

    if not user_contact:
        models.UserContact.objects.create(
            contact_id=contact,
            user_id=models.User.objects.get(id=user_id),
        )

    return HttpResponse(
        helpers.json_response(serializers.Contact(**contact.__dict__).__dict__),
        content_type="application/json",
        status=200,
    )


@csrf_exempt
@api_view(["POST"])
@helpers.validate_access_token
def contact_update(request, id: uuid.UUID):
    user_id = request.META["PROFILE"]
    update_input = project(json.loads(request.body), ["name", "is_spam"])
    user_contact = models.UserContact.objects.filter(
        user_id=user_id, contact_id=id
    ).first()

    if not user_contact:
        return HttpResponse(
            "Contact not found",
            content_type="text/plain",
            status=403,
        )

    models.Contact.objects.filter(id=id).update(**update_input)
    contact = models.Contact.objects.get(id=id)

    return HttpResponse(
        helpers.json_response(serializers.Contact(**contact.__dict__).__dict__),
        content_type="application/json",
        status=200,
    )
