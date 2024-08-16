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
        requested_user = models.User(**kwargs)
        if not models.User.objects.filter(phone=requested_user.phone).first():
            return success(
                operation="register",
                model="user",
                data=requested_user.save() or requested_user,
            )
        return bad_request(
            operation="register",
            model="user",
            message="User already Exists",
        )


class Mutation(graphene.ObjectType):
    register = RegisterResponse.Field()
