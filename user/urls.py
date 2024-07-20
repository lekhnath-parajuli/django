from user import views
from django.urls import path
from django.http import HttpResponse


urlpatterns = [
    path("ping", lambda *args, **kwargs: HttpResponse("pong")),
    path("register", view=views.register),
    path("login", view=views.login),
    path("contact", view=views.contact_create),
    path("contact/<str:id>", view=views.contact_update),
]
