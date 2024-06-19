from graphene_sqlalchemy import SQLAlchemyObjectType
from models.song import Song as SongModel

class SongType(SQLAlchemyObjectType):
    class Meta:
        model = SongModel
