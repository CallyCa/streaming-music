import graphene
from models.user import User as UserModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from extensions.decorators import jwt_required_mutation

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class UserQueries(graphene.ObjectType):
    all_users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int())

    @jwt_required_mutation
    def resolve_all_users(self, info):
        query = User.get_query(info)
        return query.all()

    @jwt_required_mutation
    def resolve_user(self, info, id):
        query = User.get_query(info)
        return query.get(id)
