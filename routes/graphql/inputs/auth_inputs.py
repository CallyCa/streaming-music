import graphene

class AuthInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
