from flask_jwt_extended import get_jwt_identity
import graphene
from extensions.decorators import jwt_required_mutation
from models.playlist import Playlist as PlaylistModel
from extensions.extensions import db
from routes.graphql.inputs.playlist_inputs import PlaylistInput
from routes.graphql.types.playlist_type import PlaylistType
from models.song import Song as SongModel

class CreatePlaylist(graphene.Mutation):
    class Arguments:
        input = PlaylistInput(required=True)

    playlist = graphene.Field(lambda: PlaylistType)

    @jwt_required_mutation
    def mutate(self, info, input):
        user_id = get_jwt_identity()
        new_playlist = PlaylistModel(name=input.name, user_id=user_id)
        db.session.add(new_playlist)
        db.session.commit()

        return CreatePlaylist(playlist=new_playlist)

class UpdatePlaylist(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PlaylistInput(required=True)

    playlist = graphene.Field(lambda: PlaylistType)

    @jwt_required_mutation
    def mutate(self, info, id, input):
        playlist = PlaylistModel.query.get(id)
        if not playlist:
            raise Exception('Playlist not found')

        if input.name:
            playlist.name = input.name
        if input.songs:
            songs = SongModel.query.filter(SongModel.id.in_(input.songs)).all()
            playlist.songs = songs

        db.session.commit()
        return UpdatePlaylist(playlist=playlist)

class DeletePlaylist(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @jwt_required_mutation
    def mutate(self, info, id):
        playlist = PlaylistModel.query.get(id)
        if not playlist:
            raise Exception('Playlist not found')

        db.session.delete(playlist)
        db.session.commit()
        return DeletePlaylist(success=True)

class PlaylistQuery(graphene.ObjectType):
    all_playlists = graphene.List(PlaylistType)
    playlist = graphene.Field(PlaylistType, id=graphene.Int())

    def resolve_all_playlists(self, info):
        query = PlaylistType.get_query(info)
        return query.all()

    def resolve_playlist(self, info, id):
        query = PlaylistType.get_query(info)
        return query.get(id)

class RemoveSongFromPlaylist(graphene.Mutation):
    class Arguments:
        playlist_id = graphene.Int(required=True)
        song_id = graphene.Int(required=True)

    playlist = graphene.Field(lambda: PlaylistType)

    @jwt_required_mutation
    def mutate(self, info, playlist_id, song_id):
        playlist = PlaylistModel.query.get(playlist_id)
        if not playlist:
            raise Exception('Playlist not found')

        song = SongModel.query.get(song_id)
        if not song:
            raise Exception('Song not found')

        if song in playlist.songs:
            playlist.songs.remove(song)
            db.session.commit()

        return RemoveSongFromPlaylist(playlist=playlist)

class PlaylistMutations(graphene.ObjectType):
    create_playlist = CreatePlaylist.Field()
    update_playlist = UpdatePlaylist.Field()
    delete_playlist = DeletePlaylist.Field()
    remove_song_from_playlist = RemoveSongFromPlaylist.Field()
