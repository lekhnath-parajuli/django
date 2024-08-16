import graphene


class BaseResponseType(object):
    code = graphene.Int()
    status = graphene.String()
    message = graphene.String()
    message_key = graphene.String()
