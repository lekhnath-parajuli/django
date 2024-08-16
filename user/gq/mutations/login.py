import graphene
from user import models
from user.helpers import helpers
from user.gq.models import BaseMutationType
from graphene_django import DjangoObjectType
from infra.response import success, bad_request


class LoginResponse(BaseMutationType, graphene.Mutation):
    class Token(graphene.ObjectType):
        access_token = graphene.String()

    class Arguments:
        # required
        password = graphene.String(required=True)
        phone = graphene.String(required=True)

    data = graphene.Field(Token, required=False)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        credentials = models.User(**kwargs)
        pwd_hash = helpers.encode_password(password=credentials.password)
        matched_user = models.User.objects.filter(
            phone=credentials.phone, password=pwd_hash
        ).first()

        if not matched_user:
            return bad_request(
                operation="login",
                model="user",
                message="Wrong username/password",
            )
        return success(
            operation="register",
            model="user",
            data={
                "accessToken": helpers.generate_jwt_token(user_id=str(matched_user.id))
            },
        )
