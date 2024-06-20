from extensions.extensions import db

class User(db.Model):
    """
    User model for storing user details.
    ---
    components:
      schemas:
        User:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
            password:
              type: string
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(128), nullable=True)
    auth = db.relationship('Auth', backref='user', uselist=False, cascade='all, delete-orphan')

    def __init__(self, name, email, nickname=None):
        self.name = name
        self.email = email
        self.nickname = nickname 

    def to_dict(self):
        """
        Convert User object to dictionary.

        :return: Dictionary representation of User.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'nickname': self.nickname
        }
