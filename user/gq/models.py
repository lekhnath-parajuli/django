import graphene


class BaseMutationType(object):
    code = graphene.Int()
    status = graphene.String()
    message = graphene.String()
    message_key = graphene.String()
