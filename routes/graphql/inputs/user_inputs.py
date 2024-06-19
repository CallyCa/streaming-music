import graphene

class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
