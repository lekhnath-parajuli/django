import graphene
from user import models
from user.helpers import helpers
from user.gq.models import BaseResponseType
from graphene_django import DjangoObjectType
from infra.response import success, bad_request


class CreateContact(BaseResponseType, graphene.Mutation):
    class Contact(DjangoObjectType):
        class Meta:
            model = models.User
            fields = ["id", "name", "phone", "is_spam"]

    class Arguments:
        # required
        name = graphene.String(required=True)
        phone = graphene.String(required=True)
        # optional
        is_spam = graphene.String(required=False)

    data = graphene.Field(Contact, required=False)

    @classmethod
    @helpers.validate_gql_access_token
    def mutate(cls, **kwargs):
        contact = models.Contact(**kwargs)

        if models.User.objects.filter(phone=user.phone).first():
            return bad_request(
                operation="register",
                model="user",
                message="User already Exists",
            )

        user.save()
        contact.save()
        models.UserContact(user_id=user, contact_id=contact)
        return success(
            operation="register",
            model="user",
            data=user,
        )
