from flask_sqlalchemy import SQLAlchemy
import os

database_path = os.environ['DATABASE_URL']

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

    def __repr__(self):
        return '<name %r>' % self.name


