import graphene


class Query(graphene.ObjectType):
    ping = graphene.String(description='pong', to=graphene.String())
    # def ping(self, args, info):
    #     return "pong"
