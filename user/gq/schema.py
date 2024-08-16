import graphene
from user.gq.queries import Query
from user.gq.mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
