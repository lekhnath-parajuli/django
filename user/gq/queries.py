import graphene


class Query(graphene.ObjectType):
    ping = graphene.String(
        description="validate server active or not",
        to=graphene.String(),
    )

    def resolve_ping(self, info, **kwargs):
        return "Pong"
