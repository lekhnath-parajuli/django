import graphene
from user.gq.queries import Query

schema = graphene.Schema(query=Query)
