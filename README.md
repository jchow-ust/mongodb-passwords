# Customised NoSQL database for storing login credentials with REST API endpoints
---

Created a cluster in MongoDB Atlas (free tier) to store NoSQL database consisting of login credentials and associated information, such as birth dates, security questions and answers, etc. For websites which were used to submit job applications, further information such as job requirements, date applied, expected salary, and follow-up information can also be saved for ease of access during interviews or future applications with the same organisation.

Access to the database is only granted with my specific IP address and with proper authentication (username & password of user with `readWriteAnyDatabase@admin` permissions.)

## How to use

Requires Python3.9+. First, clone the repo with
```
git clone https://github.com/jchow-ust/mongodb-passwords.git
```

Move to the parent directory containing `mongodb-passwords`. Run these commands to create a virtual environment in the directory containing `mongodb-passwords`.
```
python3 -m venv env-pymongo-fastapi-crud
source env-pymongo-fastapi-crud/bin/activate
python -m pip install 'fastapi[all]' 'pymongo[srv]' python-dotenv
```

You should now see a new directory `env_pymongo_fastapi_crud`. The last line will have installed the required FastAPI and PyMongo packages into this virtual environment. With the environment activated, `cd` into `mongodb-passwords`. You will need to prepare a `.env` file containing your connection string (get it from your MongoDB Atlas cluster) in this directory.

Run the application (`main.py`) with uvicorn (should come pre-installed with fastAPI):
```
python3 -m uvicorn main:app --reload
```

You may view the server at [http://127.0.0.1:8000](http://127.0.0.1:8000) and documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Schema

It should be noted that the desired use case of this database favours fast read operations over fast write/update operations.

## Tutorials and References

[MongoDB tutorial with PyMongo](https://www.mongodb.com/languages/python/pymongo-tutorial)

[FastAPI tutorial with multiple routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/#path-operations-with-apirouter)
