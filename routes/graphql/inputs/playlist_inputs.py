import graphene

class PlaylistInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    songs = graphene.List(graphene.Int)
