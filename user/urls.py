from django.urls import path
from django.http import HttpResponse



urlpatterns = [
    path("ping", lambda *args, **kwargs: HttpResponse("pong"))
]