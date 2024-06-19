from graphene_sqlalchemy import SQLAlchemyObjectType
from models.playlist import Playlist as PlaylistModel

class PlaylistType(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistModel
