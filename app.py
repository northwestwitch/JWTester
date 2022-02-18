import os
from functools import wraps

import jwt
from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecretkey"
app.config["MONGO_URI"] = os.getenv("MONGO_URI") or "mongodb://localhost:27017/jwtesterdb"
mongo = PyMongo(app)


@app.route("/")
def health_check():
    return {"message": "Server is live!"}


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = mongo["user"].find_one({"public_id": data["public_id"]})
        except:
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route("/add")
def create_user():
    """Create a test user to be used in later tests"""


# main driver function
if __name__ == "__main__":
    app.run()
