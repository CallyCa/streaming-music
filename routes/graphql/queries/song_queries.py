import graphene
from routes.graphql.types.song_type import SongType

class SongQueries(graphene.ObjectType):
    all_songs = graphene.List(SongType)
    song = graphene.Field(SongType, id=graphene.Int())

    def resolve_all_songs(self, info):
        query = SongType.get_query(info)
        return query.all()

    def resolve_song(self, info, id):
        query = SongType.get_query(info)
        return query.get(id)
