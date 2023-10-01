# Flask Code Challenge - Superheroes

For this assessment, you'll be working on an API for tracking heroes and their
superpowers.

In this repo, there is a Flask application with some features built out. There
is also a fully built React frontend application, so you can test if your API is
working.

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Setup

To download the dependencies for the frontend and backend, run:

```sh
pipenv install
npm install --prefix client
```

There is some starter code in the `app/seed.py` file so that once you've
generated the models, you'll be able to create data to test your application.

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by running:

```sh
python app.py
```

You can run your React app on [`localhost:4000`](http://localhost:4000) by running:

```sh
npm start --prefix client
```

You are not being assessed on React, and you don't have to update any of the React
code; the frontend code is available just so that you can test out the behavior
of your API in a realistic setting.

There are also tests included which you can run using `pytest -x` to check your work.

Depending on your preference, you can either check your progress by:

- Running `pytest -x` and seeing if your code passes the tests
- Running the React application in the browser and interacting with the API via
  the frontend
- Running the Flask server and using Postman to make requests

## Models

You need to create the following relationships:

- A `Hero` has many `Power`s through `HeroPower`
- A `Power` has many `Hero`s through `HeroPower`
- A `HeroPower` belongs to a `Hero` and belongs to a `Power`

Start by creating the models and migrations for the following database tables:

![domain diagram](domain.png)

Add any code needed in the model files to establish the relationships.

Then, run the migrations and seed file:

```sh
flask db upgrade
python app/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

## Validations

Add validations to the `HeroPower` model:

- `strength` must be one of the following values: 'Strong', 'Weak', 'Average'

Add validations to the `Power` model:

- `description` must be present and at least 20 characters long

## Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

### GET /heroes

Return JSON data in the format below:

```json
[
  { "id": 1, "name": "Kamala Khan", "super_name": "Ms. Marvel" },
  { "id": 2, "name": "Doreen Green", "super_name": "Squirrel Girl" },
  { "id": 3, "name": "Gwen Stacy", "super_name": "Spider-Gwen" }
]
```

### GET /heroes/:id

If the `Hero` exists, return JSON data in the format below:

```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "powers": [
    {
      "id": 1,
      "name": "super strength",
      "description": "gives the wielder super-human strengths"
    },
    {
      "id": 2,
      "name": "flight",
      "description": "gives the wielder the ability to fly through the skies at supersonic speed"
    }
  ]
}
```

If the `Hero` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Hero not found"
}
```

### GET /powers

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  },
  {
    "id": 1,
    "name": "flight",
    "description": "gives the wielder the ability to fly through the skies at supersonic speed"
  }
]
```

### GET /powers/:id

If the `Power` exists, return JSON data in the format below:

```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

If the `Power` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Power not found"
}
```

### PATCH /powers/:id

This route should update an existing `Power`. It should accept an object with
the following properties in the body of the request:

```json
{
  "description": "Updated description"
}
```

If the `Power` exists and is updated successfully (passes validations), update
its description and return JSON data in the format below:

```json
{
  "id": 1,
  "name": "super strength",
  "description": "Updated description"
}
```

If the `Power` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Power not found"
}
```

If the `Power` is **not** updated successfully (does not pass validations),
return the following JSON data, along with the appropriate HTTP status code:

```json
{
  "errors": ["validation errors"]
}
```

### POST /hero_powers

This route should create a new `HeroPower` that is associated with an
existing `Power` and `Hero`. It should accept an object with the following
properties in the body of the request:

```json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

If the `HeroPower` is created successfully, send back a response with the data
related to the `Hero`:

```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "powers": [
    {
      "id": 1,
      "name": "super strength",
      "description": "gives the wielder super-human strengths"
    },
    {
      "id": 2,
      "name": "flight",
      "description": "gives the wielder the ability to fly through the skies at supersonic speed"
    }
  ]
}
```

If the `HeroPower` is **not** created successfully, return the following
JSON data, along with the appropriate HTTP status code:

```json
{
  "errors": ["validation errors"]
}
```

## Technologies Used

The following have been used on this project:

- [Python3](https://docs.python.org/3.10/)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Pytest](https://docs.pytest.org/en/latest/contents.html)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/)
- [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask Restx](https://readthedocs.org/projects/flask-restx/)
- [React](https://react.dev/)

## Database

This project uses SQLit3:

[SQLite](https://www.sqlite.org/docs.html) - Acording to [SimpleLearn](https://www.simplilearn.com/tutorials/sql-tutorial/what-is-sqlite) SQLite is one of the most popular and easy-to-use relational database systems. It possesses many features over other relational databases. Many big MNCs such as Adobe, use SQLite as the application file format for their Photoshop Lightroom product. Airbus, a European multinational aerospace corporation, uses SQLite in the flight software for the A350 XWB family of aircraft. You will learn various concepts and get hands-on practice in this SQLite tutorial.

## Project Setup (SERVER)

- Clone the repository: `git clone <repository-url>`
- Navigate to cloned repository: `cd phase-4-w2-code-challange`
- Create pipenv environment and Install dependencies: `pipenv install`
- Activate environment: ` pipenv shell`
- Then run this commands ON `/app`: `export FLASK_APP=run.py && export FLASK_RUN_PORT=5555`
- Create db with flask migrate on `/app`: `flask db updgrade head`
- Populate db with seed file: `python3 seed.py`
- Then, start flask applcation: `python run.py` or `flask run` or `gunicorn app:app`

## Project Setup (CLIENT)

- On root direct change directory to `client`: `cd client`
- Install required packages: `npm install`
- Run react app: `npm start`

## Authors

- [John Maluki](https://github.com/john-maluki)

## Copyright

Released under the MIT License. See the [LICENSE](https://github.com/john-maluki/phase-4-w2-code-challange/blob/main/LICENSE) file.
