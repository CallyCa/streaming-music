import graphene
from models.user import User as UserModel
from models.auth import Auth
from extensions.extensions import db
from extensions.decorators import jwt_required_mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
from routes.graphql.types.user_type import UserType
from routes.graphql.inputs.user_inputs import UserInput

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(lambda: UserType)

    @jwt_required_mutation
    def mutate(self, info, input):
        if UserModel.query.filter_by(email=input.email).first() or Auth.query.filter_by(email=input.email).first():
            raise Exception("Email already registered")

        user = UserModel(name=input.name, email=input.email)
        db.session.add(user)
        db.session.commit()

        auth = Auth(email=input.email, password=input.password, user_id=user.id)
        db.session.add(auth)
        db.session.commit()

        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput()

    user = graphene.Field(lambda: UserType)

    @jwt_required_mutation
    def mutate(self, info, id, input):
        user = UserModel.query.get(id)
        if not user:
            raise Exception('User not found')

        if 'name' in input and input.name != user.name:
            user.name = input.name
        if 'email' in input and input.email != user.email:
            if UserModel.query.filter_by(email=input.email).first() or Auth.query.filter_by(email=input.email).first():
                raise Exception("Email already registered")
            user.email = input.email

        if 'password' in input:
            auth = Auth.query.filter_by(user_id=id).first()
            if auth and not auth.check_password(input.password):
                auth.password = auth.set_password(input.password)

        db.session.commit()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @jwt_required_mutation
    def mutate(self, info, id):
        user = UserModel.query.get(id)
        if not user:
            raise Exception('User not found')

        db.session.delete(user)
        db.session.commit()
        return DeleteUser(ok=True)

class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
