from flask import Flask, request, render_template, make_response
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

import config_flask

from Modules.user_management import (login, register_user, send_recovery_email, logout,
                                     change_password, verify_session)

app = Flask(__name__)
app.config.from_object('config_flask.SandboxConfig')
# app.config["PREFERRED_URL_SCHEME"] = "https"
api = Api(app)

# Enable CORS on all endpoints
CORS(app)


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
            new_session_id, user_id = login(email, raw_password)
            if new_session_id:
                response = {'session_id': new_session_id, 'user_id': user_id}
                return make_response(jsonify(response), 200)
            else:
                return make_response('Wrong password', 400)
        else:
            pass

    def post(self):
        # Register
        email = request.form.get('email')
        raw_password = request.form.get('raw_password')
        registration_result = register_user(email, raw_password)
        if registration_result == 'registered':
            return make_response(registration_result, 200)
        else:
            return make_response(registration_result, 400)

    def patch(self, user_id=None):
        if user_id == None:
            # Password recovery email sending
            email = request.headers.get('email')
            confirmation = send_recovery_email(email)
            return make_response(confirmation, 200)
        else:
            # Password change handling
            new_password = request.headers.get('new_password')
            password_change = change_password(user_id, new_password)
            if password_change == 'password_changed':
                return make_response(password_change, 200)
            else:
                return make_response(password_change, 400)

    def delete(self):
        # Logout
        user_id = request.headers.get('user_id')
        logout_result = logout(user_id)
        if logout_result == 'logout_successful':
            return make_response(logout_result, 200)
        elif logout_result == 'logout_unsuccessful':
            return make_response(logout_result, 400)
        else:
            return make_response(None, 400)


api.add_resource(Account, "/account/<user_id>", "/account")


class Main(Resource):
    def get(self):
        session_id = request.headers.get('session_id')
        verification = verify_session(session_id)
        if verification:
            return make_response('True', 200)
        else:
            return main()


api.add_resource(Main, "/")
