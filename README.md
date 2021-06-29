#README REQUIREMENTS FROM RUBRIC

Deployment:
    Application is hosted live at student provided URL::
        URL is provided in project README

Code Quality and Documentation:
    Project includes thorough documentation::
        hosting instructions,
		○ Documentation of API behavior

# CAPSTONE PROJECT: lav_cast_agency
##Motivation
this is the capstone final project based on casting agency specifications. 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors 
to those movies. 
This system is created to simplify and streamline the process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

Ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
setup.sh
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Authentication with Auth0
valid JWT are provided as part of setup.sh to test endpoints

## Roles & Permissions
• Roles:
	• Casting Assistant
		○ Can view actors and movies
	• Casting Director
		○ All permissions a Casting Assistant has and…
		○ Add or delete an actor from the database
		○ Modify actors or movies
	• Executive Producer
		○ All permissions a Casting Director has and…
        ○ Add or delete a movie from the database

• Permissions:
view:actors	(to read actors)	
view:movies	(to read movies)
add:actors	(to add an actor)	
delete:actors	(to delete an actor)	
modify:actors	(to edit an actor)
modify:movies	(to edit a movie)	
add:movies	(to add a movie)
delete:movies	(to delete a movie)

## Testing
To run the tests, run
```bash
python test_app.py
```

##Endpoints
GET /
GET /actors 
GET /movies
DELETE /actors/<int:actor_id> 
DELETE /movies/<int:movie_id>
POST /actors 
POST /movies
PATCH /actors/<int:actor_id> 
PATCH /movies/<int:movie_id>

### GET / 
#### Description
index. basic sample endpoint
#### Request Arguments
None
#### Returns

#### Sample Request
#### Sample Response
