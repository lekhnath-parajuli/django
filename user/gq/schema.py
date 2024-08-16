import graphene
from user.gq.mutations.register import RegisterResponse


class Mutation(graphene.ObjectType):
    register = RegisterResponse.Field()


class Query(graphene.ObjectType):
    ping = graphene.String(
        description="validate server active or not",
        to=graphene.String(),
    )

    def resolve_ping(self, info, **kwargs):
        return "Pong"


schema = graphene.Schema(query=Query, mutation=Mutation)
