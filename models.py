from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

user_name = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

database_name = "lav_cast_agency"
# database_path = "postgresql://" + user_name + ":" + password + "@{}/{}".format('localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
database_path.replace('postgres://', 'postgresql://', 1)  # workaround to make it work in heroku

db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def create_test_data():
    a_movie = Movie(
        title='TestDune',
        release_date='1984-1-1'
    )
    a_movie.insert()
    an_actor = Actor(
        name='TestPaul',
        age=15,
        gender='male'
    )
    an_actor.insert()


'''
Actor_Movie
helper table
'''

actor_movie = db.Table('actor_movie',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)

'''
Movie
Have title and release date
'''


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    actors = db.relationship('Actor', secondary=actor_movie, lazy='subquery',
                             backref=db.backref('movies', lazy=True))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return '<Title %r>' % self.title


'''
Actor
Have name, age and gender
'''


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(25), nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return '<name %r>' % self.name



