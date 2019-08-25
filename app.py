from functools import wraps

from flask import Flask, request, make_response, send_file
from flask.json import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

from Modules.Documenter.PDFDocument import PDFDocument
from Modules.Documenter.views import fetch_all_templates
from Modules.user_management import (
    login,
    register_user,
    send_recovery_email,
    logout,
    change_password,
    session_exists,
)

app = Flask(__name__)
app.config.from_object("config_flask.SandboxConfig")
api = Api(app)

# Enable CORS on all endpoints
CORS(app)


def main():
    return jsonify("Elo")


def verify_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            session_id = request.headers.get("session_id")
            account_id = request.headers.get("account_id")
        except Exception as e:
            print(e)
            return make_response(401, "Invalid session")
        if session_exists(session_id, account_id):
            return func(**kwargs)
        else:
            return make_response(401, "Invalid session")

    return wrapper()


class AccountRegister(Resource):
    def post(self):
        try:
            email = request.form.get("email")
            raw_password = request.form.get("raw_password")
        except Exception as e:
            print(e)
            return make_response("Not enough data provided", 400)
        session_id, account_id = register_user(email, raw_password)
        if session_id and account_id:
            response = {"session_id": session_id, "account_id": account_id}
            return make_response(jsonify(response), 200)
        else:
            return make_response("registration_failed", 401)


api.add_resource(AccountRegister, "/account/register")


class AccountLogin(Resource):
    def post(self):
        try:
            raw_password = request.form.get("raw_password")
            email = request.form.get("email")
        except Exception as e:
            print(e)
            return make_response("Not enough data provided", 400)
        new_session_id, account_id = login(email, raw_password)
        if new_session_id:
            response = {"session_id": new_session_id, "account_id": account_id}
            return make_response(jsonify(response), 200)
        else:
            return make_response("Wrong password", 403)


api.add_resource(AccountLogin, "/account/login")


class AccountResetPassword(Resource):
    def post(self):
        # Password recovery email sending
        try:
            email = request.form.get("email")
        except Exception as e:
            print(e)
            return make_response("no_email_provided", 400)
        confirmation = send_recovery_email(email)
        if confirmation == "email_sent":
            return make_response(confirmation, 200)
        return make_response(confirmation, 500)

    @verify_session
    def patch(self):
        # Password change handling
        new_password = request.form.get("new_password")
        account_id = request.headers.get("account_id")
        password_change = change_password(account_id, new_password)
        if password_change == "password_changed":
            return make_response(password_change, 200)
        elif password_change == "user_does_not_exist":
            return make_response(password_change, 403)
        elif password_change == "message_not_sent":
            return make_response(password_change, 400)


api.add_resource(AccountResetPassword, "/account/reset")


class AccountLogout(Resource):
    @verify_session
    def delete(self):
        # Logout
        account_id = request.headers.get("account_id")
        session_id = request.headers.get("session_id")
        logout_result = logout(session_id, account_id)
        if logout_result == "logout_successful":
            return make_response(logout_result, 200)
        elif logout_result == "logout_unsuccessful":
            return make_response(logout_result, 400)
        else:
            return make_response(None, 500)


api.add_resource(AccountLogout, "/account/logout")


class Main(Resource):
    @verify_session
    def get(self):
        return make_response("True", 200)


api.add_resource(Main, "/")


class CreatePDF(Resource):
    @verify_session
    def get(self):
        return jsonify(fetch_all_templates())

    @verify_session
    def post(self):
        """
        Endpoint that handles the creation of PDF document based on
        form data given
        """
        template_id = request.headers.get("template_id")
        account_id = request.headers.get("account_id")
        custom_field = request.headers.get("custom_fields")
        document = PDFDocument(template_id, account_id, custom_field)
        try:
            with document.create_file() as pdf_name:
                return send_file(pdf_name, attachment_filename=pdf_name)
        except KeyError:
            return make_response("Invalid form data", 400)


api.add_resource(CreatePDF, "/documents")
