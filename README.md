# Back-end for TODO list

This is a simple API-server for a TODO list app which I developed as my assignment for Integrify Full Stack program December 2022.


Tech Stack: Python, Flask, PostgreSQL.

## Setup & Installation

Python version for this app should be at least 3.9.7.

```bash
git clone <repo-url>
```
The project uses pipenv for dependency management. Install pipenv before proceeding.

Run pipenv install inside the project directory.

```bash
pipenv install 
```
In addition to source code a PostgreSQL instance is required.

## Running The App

Add file .env with the following lines in the project directory:

```bash
# add random gibberish as the value for TOKEN_SECRET
TOKEN_SECRET=<token secret>
# <postgresql URL> in format postgresql://username:password@hostname/db_name
POSTGRESQL_URL=<postgresql URL>
```

Now you can start the development server by running:
```bash
pipenv run devserver
```
## Using the API

The Dev server starts the API at `http://localhost:5000`
Repository includes [Postman collection](Todo_API.postman_collection.json) for testing the APIs.

The back-end app is also deployed at:
https://todo-list-python.azurewebsites.net

### Implemented features

The backend application exposes a set of REST APIs for the following endpoints:

- **POST** */api/v1/signup*: Sign up as an user of the system, using email & password. The response will be:
    - HTTP 201 with an empty body when the user was created successfully
    - HTTP 403 if a user with the email is already registered
- **POST** */api/v1/signin*: Sign in using email & password. The response will be:
    - HTTP 200 OK with encoded token if authentication was successful
    - HTTP 403 if authentication failed
- **PUT** */api/v1/changePassword*: Change user’s password.The response will be:
    - HTTP 204 NO CONTENT if password change was successful
    - HTTP 403 if authentication failed
- **GET** */api/v1/todos?status=[status]*: Get a list of todo items. Optionally, a status query param can be included to return only items of specific status. If not present, return all items.The response will be:
    - HTTP 200 OK with list of TODOs for the current user in the body
    - HTTP 403 if authentication failed
- **POST** */api/v1/todos*: Create a new todo item.The response will be:
    - HTTP 200 OK with added TODO item in the body including generated id and timestamps
    - HTTP 403 if authentication failed
- **PUT** */api/v1/todos/:id*: Update a todo item.The response will be:
    - HTTP 200 OK with changed TODO item in the body including updated timestamp
    - HTTP 403 if authentication failed
- **DELETE** */api/v1/todos/:id*: Delete a todo item.The response will be:
    - HTTP 200 OK with id of deleted TODO item
    - HTTP 403 if authentication failed

### Planned further development

- Add Unit tests and flask endpoint tests using SQLLite
- Add experation time to the authentication tokens
- Write a simple Front-End in React

