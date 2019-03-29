from flask import Flask, request, render_template
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

from Models.db import session_scope
from Models.user_management import UMAccounts

app = Flask(__name__)
app.config["PREFERRED_URL_SCHEME"] = "https"
api = Api(app)

# Enable CORS on all endpoints
CORS(app)

@app.route('/')
def main():
    return jsonify('Elo')

class Account(Resource):
    def get(self, user_id=None):
        if user_id is None:
            with session_scope() as session:
                for element in session.query(UMAccounts):
                    result = element.email
                return jsonify(result)
        else:
            pass


api.add_resource(Account, "/account/<user_id>", "/account/")




