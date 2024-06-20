import graphene
from routes.graphql.types.playlist_type import PlaylistType
from models.playlist import Playlist as PlaylistModel
from models.song import Song as SongModel

class PlaylistQueries(graphene.ObjectType):
    all_playlists = graphene.List(PlaylistType)
    playlist = graphene.Field(PlaylistType, id=graphene.Int(required=True))
    playlists_by_song = graphene.List(PlaylistType, song_id=graphene.Int(required=True))

    def resolve_all_playlists(self, info):
        query = PlaylistType.get_query(info)
        return query.all()

    def resolve_playlist(self, info, id):
        query = PlaylistType.get_query(info)
        return query.get(id)

    def resolve_playlists_by_song(self, info, song_id):
        query = PlaylistType.get_query(info)
        return query.join(PlaylistModel.songs).filter(SongModel.id == song_id).all()
