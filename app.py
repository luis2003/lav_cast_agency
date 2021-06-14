import os
from flask import Flask, request, abort, jsonify
from models import setup_db, db, Movie, Actor
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

    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()

        for value in body:
            if value == "":
                abort(422)

        new_movie_title = body.get('title', None)
        new_movie_release_date = body.get('release_date', None)

        if not new_movie_title:
            abort(422)

        try:
            new_movie = Movie(title=new_movie_title,
                              release_date=new_movie_release_date)

            db.session.add(new_movie)
            db.session.commit()
            return jsonify({
                'success': True
            })

        except ValueError as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        for value in body:
            if value == "":
                abort(422)

        new_actor_name = body.get('name', None)
        new_actor_age = body.get('age', None)
        new_actor_gender = body.get('gender', None)

        if not new_actor_name:
            abort(422)

        try:
            new_actor = Actor(name=new_actor_name,
                              age=new_actor_age,
                              gender=new_actor_gender)

            db.session.add(new_actor)
            db.session.commit()
            return jsonify({
                'success': True
            })

        except ValueError as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)