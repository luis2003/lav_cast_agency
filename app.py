import os
from flask import Flask, request, abort, jsonify
from models import setup_db, db, Movie, Actor
from flask_cors import CORS
import logging
from auth.auth import AuthError, requires_auth

database_path = os.environ['DATABASE_URL']

'''from jose import jwt
import json
from urllib.request import urlopen
from functools import wraps

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')


class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    details:
    get the header from the request.
    raise an AuthError if no header is present.
    split bearer and the token.
    raise an AuthError if the header is malformed.
    return the token part of the header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """
        @INPUTS
            permission: string permission (i.e. 'post:drink')
            payload: decoded jwt payload

        raise an AuthError if permissions are not included in the payload.
        raise an AuthError if the requested permission string is not in the payload permissions array.
        return true otherwise.
    """
    if 'permissions' not in payload:
        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def verify_decode_jwt(token):
    """
        @INPUTS
            token: a json web token (string)

        check it is Auth0 token with key id (kid)
        Verify the token using Auth0 /.well-known/jwks.json
        Decode the payload from the token
        Validate the claims.
        Return the decoded payload.

        !!NOTE urlopen has a common certificate error described here:
        https://stackoverflow.com/questions/50236117/
        scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    """
    decorator method
        @INPUTS
            permission: string permission (i.e. 'post:drink')

        Use the get_token_auth_header method to get the token.
        Use the verify_decode_jwt method to decode the jwt.
        Use the check_permissions method validate claims and check the requested permission.
        Return the decorator which passes the decoded payload to the decorated method.
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)

            except Exception as e:
                logging.exception('An exception occurred while in wrapper internal function')
                # print(repr(e))
                abort(401)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator'''

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
    @requires_auth('view:actors')
    def get_movies(jwt):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        movies_dict = {movie.id: movie.title for movie in movies}

        return jsonify({
            'movies': movies_dict
        })

    @app.route('/actors')
    @requires_auth('view:movies')
    def get_actors(jwt):
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        actors_dict = {actor.id: actor.name for actor in actors}

        return jsonify({
            'actors': actors_dict
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def create_movie(jwt):
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
    @requires_auth('add:actors')
    def create_actor(jwt):
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
    @requires_auth('modify:movies')
    def patch_movie(jwt, movie_id):
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
    @requires_auth('modify:actors')
    def patch_actor(jwt, actor_id):
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
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        selection = Movie.query.filter(Movie.id == movie_id).all()
        if len(selection) == 0:
            abort(404)
        selection[0].delete()
        return jsonify({"success": True,
                        "deleted": movie_id})

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
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

    @app.errorhandler(403)
    def permissions_not_found(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found"
        }), 403

    @app.errorhandler(AuthError)
    def autherror_handler(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)