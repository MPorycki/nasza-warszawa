from flask import Flask, request, render_template, make_response
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

from Modules.user_management import check_password, register_user, send_recovery_email

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
        # Login
        if user_id is None:
            try:
                raw_password = request.headers.get('raw_password')
                email = request.headers.get('email')
            except Exception as e:
                return make_response(e, 400)
            check_result = check_password(email, raw_password)
            if check_result:
                return make_response(str(check_result), 200)
            else:
                return make_response('Wrong password', 400)
        else:
            pass

    def post(self):
        # Register
        email = request.headers.get('email')
        raw_password = request.headers.get('raw_password')
        registration_result = register_user(email, raw_password)
        if registration_result == 'registered':
            return make_response(registration_result, 200)
        else:
            return make_response(registration_result, 400)

    def patch(self):
        # Password recovery
        email = request.headers.get('email')
        confirmation = send_recovery_email(email)
        return make_response(confirmation, 200)


api.add_resource(Account, "/account/<user_id>", "/account/")
