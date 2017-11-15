from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
    
            #Define a base way to jsonify models, dealing with datetime objects
    
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class User(BaseModel, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column('name', db.Text, unique=True, nullable=False)
    email = db.Column('email', db.Text, unique=True, nullable=False)
    password = db.Column('password', db.Text, nullable=False)
    gender = db.Column('gender', db.Text, nullable = False)
    phone = db.Column('phone', db.Text, nullable = False)
    created_at = db.Column('created_at', db.Text, nullable=True)
    user_region = db.Column('user_region', db.Text, nullable=False)
    user_description = db.Column('user_description', db.Text, nullable=False)
    posts_number = db.Column('posts_number', db.Integer, nullable=False)
    follow_number = db.Column('follow_number', db.Integer, nullable=False)
    follower_number = db.Column('follower_number', db.Integer, nullable=False)



    
    def __repr__(self):
        return "<User(name='%s', email='%s', password='%s')>" % (self.name, self.email, self.password)

    #gender = db.Column(db.Text)
    #phone = db.Column(db.Text)
    def __init__(self, _name, _email, _password):
        #super().__init__(args)
        self.name = _name
        self.email = _email
        self.password = _password

        self.gender = "male"
        self.phone = "0000000"
        self.created_at = None
        self.user_region = "le cul"
        self.user_description = "prout"
        self.posts_number = 0
        self.follower_number = 0
        self.follower_number = 0

    #mettre le reste des champs