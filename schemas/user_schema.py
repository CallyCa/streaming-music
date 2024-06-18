from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """
    Schema for serializing and deserializing User objects.
    
    Attributes:
        id (fields.Int): The user's ID.
        name (fields.Str): The user's name. Must be at least 1 character long.
        email (fields.Email): The user's email.
        password (fields.Str): The user's password. Must be at least 6 characters long.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
