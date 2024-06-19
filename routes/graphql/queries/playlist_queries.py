import graphene
from routes.graphql.types.playlist_type import PlaylistType

class PlaylistQueries(graphene.ObjectType):
    all_playlists = graphene.List(PlaylistType)
    playlist = graphene.Field(PlaylistType, id=graphene.Int())

    def resolve_all_playlists(self, info):
        query = PlaylistType.get_query(info)
        return query.all()

    def resolve_playlist(self, info, id):
        query = PlaylistType.get_query(info)
        return query.get(id)
