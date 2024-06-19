import graphene
from models.auth import Auth
from models.user import User as UserModel
from extensions.extensions import db
from flask_jwt_extended import create_access_token
from routes.graphql.inputs.auth_inputs import AuthInput
from routes.graphql.inputs.user_inputs import UserInput
from routes.graphql.types.user_type import UserType

class RegisterUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(self, info, input):
        if Auth.query.filter_by(email=input.email).first():
            raise Exception("Email already registered")

        new_user = UserModel(name=input.name, email=input.email)
        db.session.add(new_user)
        db.session.commit()

        new_auth = Auth(email=input.email, password=input.password, user_id=new_user.id)
        db.session.add(new_auth)
        db.session.commit()

        return RegisterUser(user=new_user)

class LoginUser(graphene.Mutation):
    class Arguments:
        input = AuthInput(required=True)

    access_token = graphene.String()

    def mutate(self, info, input):
        auth = Auth.query.filter_by(email=input.email).first()

        if auth and auth.check_password(input.password):
            access_token = create_access_token(identity=auth.user_id)
            return LoginUser(access_token=access_token)

        raise Exception("Invalid credentials")

class AuthMutations(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
