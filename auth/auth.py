from flask import g
from flask_httpauth import HTTPBasicAuth
from models.user import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    """
    Verify the password for a given email.

    :param email: User email
    :param password: User password
    :return: Boolean indicating whether the verification was successful
    """
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        g.user = user
        return True
    return False
