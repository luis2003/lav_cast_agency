import os
from flask import Flask, request, abort, jsonify
from models import setup_db, db, Movie, Actor
from flask_cors import CORS
import logging
from auth.auth import AuthError, requires_auth


database_path = os.environ['DATABASE_URL']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    @requires_auth()
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

            new_movie.insert()
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

            new_actor.insert()
            return jsonify({
                'success': True
            })

        except ValueError as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    # @requires_auth('patch:movies')
    def patch_movie(movie_id):
        body = request.get_json()

        try:
            movie_to_patch = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie_to_patch is None:
                abort(404)

            if 'title' in body:
                movie_to_patch.title = str(body.get('title'))

            if 'release_date' in body:
                movie_to_patch.release_date = body.get('release_date')

            movie_to_patch.update()
            updated_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            return jsonify({"success": True,
                            "movie": [updated_movie.format()]})

        except Exception as E:
            logging.exception('An exception occurred while updating movie')
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    def patch_actor(actor_id):
        body = request.get_json()

        try:
            actor_to_patch = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor_to_patch is None:
                abort(404)

            if 'name' in body:
                actor_to_patch.name = str(body.get('name'))

            if 'age' in body:
                actor_to_patch.age = body.get('age')

            if 'gender' in body:
                actor_to_patch.gender = body.get('gender')

            actor_to_patch.update()
            updated_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            return jsonify({"success": True,
                            "actor": [updated_actor.format()]})

        except Exception as E:
            logging.exception('An exception occurred while updating actor')
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    # @requires_auth('delete:movies')
    def delete_movie(movie_id): # def delete_drink(jwt, drink_id):
        selection = Movie.query.filter(Movie.id == movie_id).all()
        if len(selection) == 0:
            abort(404)
        selection[0].delete()
        return jsonify({"success": True,
                        "deleted": movie_id})

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    def delete_actor(actor_id): # def delete_drink(jwt, drink_id):
        selection = Actor.query.filter(Actor.id == actor_id).all()
        if len(selection) == 0:
            abort(404)
        selection[0].delete()
        return jsonify({"success": True,
                        "deleted": actor_id})

    # Error Handling
    '''
    Utilize the @app.errorhandler decorator to format error responses as 
    JSON objects for at least four different status codes
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    @TODO (DONE) implement error handler for AuthError
        error handler should conform to general task above
    

    @app.errorhandler(AuthError)
    def autherror_handler(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response'''

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)