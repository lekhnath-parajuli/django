import graphene
from user.gq.mutations.register import RegisterResponse
from user.gq.queries.login import LoginResponse


class Mutation(graphene.ObjectType):
    register = RegisterResponse.Field()


class Query(graphene.ObjectType):
    ping = graphene.String(
        description="validate server active or not",
        to=graphene.String(),
    )

    login = graphene.Field(
        LoginResponse,
        phone=graphene.String(required=True),
        password=graphene.String(required=True)
    )

    def resolve_ping(self, info, **kwargs):
        return "Pong"

    def resolve_login(*args, **kwargs):
       return LoginResponse().resolve_login(*args, **kwargs)

schema = graphene.Schema(query=Query, mutation=Mutation)
