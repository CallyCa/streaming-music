from graphene_sqlalchemy import SQLAlchemyObjectType
from models.user import User as UserModel

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
