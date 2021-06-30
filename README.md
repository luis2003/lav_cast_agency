# CAPSTONE PROJECT: lav_cast_agency

##Deployment
Application is hosted live at following URL: https://lav-cast-agency.herokuapp.com/
tested 6/29/2021 8pmEST
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
1. GET /
2. GET /actors 
3. GET /movies
4. DELETE /actors/<int:actor_id> 
5. DELETE /movies/<int:movie_id>
6. POST /actors 
7. POST /movies
8. PATCH /actors/<int:actor_id> 
9. PATCH /movies/<int:movie_id>

### 1. GET /
#### Description
index. basic sample endpoint
#### Request Arguments
None
#### Returns
a text message including the first movie entry in database
#### Sample Request
```bash
curl http://localhost:5000/
```
#### Sample Response
"Hola Capstone! The first movie in the DB is: King Kong"

### 2. GET /actors 
#### Description
Endpoint to see the names of all actors in the database.
#### Request Arguments
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING ASSISTANT,
CASTING DIRECTOR or EXECUTIVE PRODUCER roles).
#### Returns
#### Sample Request
```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://localhost:5000/actors
```
#### Sample Response
{
  "actors": {
    "1": "Tom",
    "2": "Mary",
    "3": "Ken",
    "4": "Will Patton",
    "5": "Will Patton"
  }
}

### 3. GET /movies
#### Description
Endpoint to see the title of all movies in the database.
#### Request Arguments
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING ASSISTANT,
CASTING DIRECTOR or EXECUTIVE PRODUCER roles).
#### Returns
A dictionary of key/value pairs with movie_id as key and title as value.
#### Sample Request
```bash
curl -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://localhost:5000/movies
```
#### Sample Response
{
  "movies": {
    "1": "King Kong",
    "2": "Godzilla",
    "3": "Shrek",
    "4": "Dune",
    "5": "PatchedDune"
  }
}

### 4. DELETE /actors/<int:actor_id>  
#### Description
Removes a specific actor from the database.
#### Request Arguments
Actor ID as an integer as part of the URL.
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING DIRECTOR or 
EXECUTIVE PRODUCER roles).
#### Returns
A jsonify response containing if action was successful and id of the deleted item.
#### Sample Request
```bash
curl -s -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" -X DELETE http://localhost:5000/actors/5
```
#### Sample Response
{
  "deleted": 5,
  "success": true
}

### 5. DELETE /movies/<int:movie_id>
#### Description
Removes a specific actor from the database.
#### Request Arguments
Movie ID as an integer as part of the URL.
Requires a JWT from a user with a role/permission authorized to use this API (i.e. EXECUTIVE PRODUCER role).
#### Returns
A jsonify response containing if action was successful and id of the deleted item.
#### Sample Request
```bash
curl -s -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" -X DELETE http://localhost:5000/movies/5
```
#### Sample Response
{
  "deleted": 5,
  "success": true
}

### 6. POST /actors 
#### Description
Adds a new actor to the database.
#### Request Arguments
A dictionary with actor name, age(optional) and gender(optional).
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING DIRECTOR or 
EXECUTIVE PRODUCER roles).
#### Returns
A jsonify response containing if action was successful.
#### Sample Request
```bash
curl -s -d '{"name":"Will Patton", "age":67, "gender":"male"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X POST http://localhost:5000/actors
```
#### Sample Response
{
  "success": true
}

### 7. POST /movies
#### Description
Adds a new movie to the database.
#### Request Arguments
A dictionary with movie title, and release date(optional).
Requires a JWT from a user with a role/permission authorized to use this API (i.e. EXECUTIVE PRODUCER role).
#### Returns
A jsonify response containing if action was successful.
#### Sample Request
```bash
curl -s -d '{"title":"Dune", "release_date":"1984-12-14"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X POST http://localhost:5000/movies
```
#### Sample Response
{
  "success": true
}

### 8. PATCH /actors/<int:actor_id>
#### Description
Modifies the data of an existing actor in the database.
#### Request Arguments
Actor ID as an integer as part of the URL.
A dictionary with actor data to modify and new values: name, age or gender.
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING DIRECTOR or 
EXECUTIVE PRODUCER roles).
#### Returns
A jsonify response containing if action was successful and a list containing a dictionary of the modified actor and
its new data.
#### Sample Request
```bash
curl -s -d '{"name":"PatchedWill Patton", "age":68, "gender":"male"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X PATCH http://localhost:5000/actors/6
```
#### Sample Response
{
  "actor": [
    {
      "age": 68,
      "gender": "male",
      "id": 6,
      "name": "PatchedWill Patton"
    }
  ],
  "success": true
}


### 9. PATCH /movies/<int:movie_id>
#### Description
Modifies the data of an existing movie in the database.
#### Request Arguments
Movie ID as an integer as part of the URL.
A dictionary with movie data to modify and new values: title or release_date.
Requires a JWT from a user with a role/permission authorized to use this API (i.e. CASTING DIRECTOR or 
EXECUTIVE PRODUCER roles).
#### Returns
A jsonify response containing if action was successful and a list containing a dictionary of the modified movie and
its new data.
#### Sample Request
```bash
curl -s -d '{"title":"PatchedDune", "release_date":"1985-12-14"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -X PATCH http://localhost:5000/movies/6
```
#### Sample Response
{
  "movie": [
    {
      "id": 6,
      "release_date": "Sat, 14 Dec 1985 00:00:00 GMT",
      "title": "PatchedDune"
    }
  ],
  "success": true
}
