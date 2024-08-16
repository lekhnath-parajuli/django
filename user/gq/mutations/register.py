import graphene
from user import models
from user.gq.models import BaseMutationType
from graphene_django import DjangoObjectType
from infra.response import success, bad_request


class RegisterResponse(BaseMutationType, graphene.Mutation):
    class Register(DjangoObjectType):
        class Meta:
            model = models.User
            fields = ["id", "name", "email", "phone"]

    class Arguments:
        # required
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String(required=True)
        # optional
        email = graphene.String(required=False)

    data = graphene.Field(Register, required=False)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = models.User(**kwargs)
        contact = models.Contact(name=user.name, phone=user.phone)

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
