from flask_jwt_extended import jwt_required
import graphene
from models.song import Song as SongModel
from extensions.extensions import db
from extensions.decorators import jwt_required_mutation
from routes.graphql.types.song_type import SongType

class SongInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    artist = graphene.String(required=True)
    album = graphene.String(required=True)
    duration = graphene.Int(required=True)

class CreateSong(graphene.Mutation):
    class Arguments:
        input = SongInput(required=True)

    song = graphene.Field(lambda: SongType)

    @jwt_required_mutation
    def mutate(self, info, input):
        song = SongModel(
            title=input.title,
            artist=input.artist,
            album=input.album,
            duration=input.duration
        )
        db.session.add(song)
        db.session.commit()
        return CreateSong(song=song)

class UpdateSong(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = SongInput()

    song = graphene.Field(lambda: SongType)

    @jwt_required_mutation
    def mutate(self, info, id, input):
        song = SongModel.query.get(id)
        if not song:
            raise Exception('Song not found')

        for key, value in input.items():
            setattr(song, key, value)

        db.session.commit()
        return UpdateSong(song=song)

class DeleteSong(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @jwt_required_mutation
    def mutate(self, info, id):
        song = SongModel.query.get(id)
        if not song:
            raise Exception('Song not found')

        db.session.delete(song)
        db.session.commit()
        return DeleteSong(ok=True)

class SongMutations(graphene.ObjectType):
    create_song = CreateSong.Field()
    update_song = UpdateSong.Field()
    delete_song = DeleteSong.Field()
