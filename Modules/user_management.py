import uuid
import datetime
import smtplib
import ssl

from passlib.hash import sha256_crypt
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from Models.user_management import UMAccounts, UM_sent_messages, UMSessions
from Models.db import session_scope, session


def register_user(email, raw_password):
    created_at = datetime.datetime.now()
    user_id = uuid.uuid4().hex
    password = sha256_crypt.hash(raw_password)
    new_user = UMAccounts(id=user_id, email=email, hashed_password=password,
                          created_at=created_at)
    session.add(new_user)
    try:
        session.commit()
    except (InvalidRequestError, IntegrityError) as e:
        # Error thrown, when some of the db requirements are not met
        session.rollback()
        return "email_already_in_db"
    # session.close()
    return "registered"


def login(email, raw_password):
    encrypted_from_db = str(session.query(UMAccounts.hashed_password).filter(
        UMAccounts.email == email).first()[0])
    check = sha256_crypt.verify(raw_password, encrypted_from_db)
    session_to_return = None
    user_id = None
    # TODO add passing through user id
    if check:
        session_to_return = create_session_for_user(email)
        user_id = session.query(UMAccounts).filter(UMAccounts.email == email).first().id
    return session_to_return, user_id


def send_recovery_email(email):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "poryckimarcin@gmail.com"
    password = "s@>-88bQ~[uhkp'd"

    context = ssl.create_default_context()

    message = "Here's your recovery link!!"

    response = 'message_not_sent'
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email,email,message)
        response = 'email_sent'
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
        return response


def change_password(user_id, new_password):
    user= session.query(UMAccounts).filter(UMAccounts.id == user_id).first()
    new_password_hash = sha256_crypt.hash(new_password)
    user.hashed_password = new_password_hash
    try:
        session.commit()
    except Exception as e:
        return "password_not_changed"
    return 'password_changed'


def create_session_for_user(email):
    user_id = session.query(UMAccounts.id).filter(UMAccounts.email == email).first()[0]
    session_id = uuid.uuid4().hex
    created_at = str(datetime.datetime.now())
    try:
        new_session = UMSessions(um_accounts_id=user_id, session_id=session_id,
                                 created_at=created_at)
        session.add(new_session)
        session.commit()
    except Exception as e:
        session.rollback()
        return e
    session.close()
    return session_id


def verify_session(session_id):
    session_for_test_user = session.query(UMSessions).filter(
        UMSessions.session_id == session_id).exists()
    return  session.query(session_for_test_user).scalar()
    # TODO need to make this a decorator that checks the authorization header for session_id


def logout(user_id):
    try:
        session.query(UMSessions).filter(UMSessions.um_accounts_id == user_id).delete()
        session.commit()
    except Exception as e:
        return 'logout_unsuccessful'
    return 'logout_successful'
