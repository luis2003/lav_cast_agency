import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor
from flask_cors import CORS

database_path = os.environ['DATABASE_URL']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        first_movie = Movie.query.first()
        return 'Hola Capstone! The first movie in the DB is: ' + first_movie.title

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        movies_dict = {movie.id: movie.title for movie in movies}

        return jsonify({
            'movies': movies_dict
        })

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        actors_dict = {actor.id: actor.name for actor in actors}

        return jsonify({
            'actors': actors_dict
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)