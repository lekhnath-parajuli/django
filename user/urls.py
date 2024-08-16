import graphene
from user import views
from user.gq.schema import schema
from django.urls import path
from django.http import HttpResponse
from graphene_django.views import GraphQLView


urlpatterns = [
    # path("gq", GraphQLView.as_view(graphiql=True, schema=schema)),
    path("ping", lambda *args, **kwargs: HttpResponse("pong")),
    path("register", view=views.register),
    path("login", view=views.login),
    path("login", view=views.login),
    path("contacts", view=views.contacts),
    path("contact", view=views.contact_create),
    path("contact/<str:id>", view=views.contact_update),
]
