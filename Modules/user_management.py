import uuid
import datetime

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
    # TODO add passing through user id
    if check:
        session_to_return = create_session_for_user(email)
    return session_to_return


def send_recovery_email(email):
    pass


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
    # what is being stored in cookie? because I can check and tell, that this session ID belongs
    # to a given user, do we want to verify that this user is the one passing the request,
    # or is just the fact of sending the session ID being enough to login the user to that
    # given account?
    # need to make this a decorator that checks the authorization header for session_id
    pass


def logout(user_id):
    try:
        session.query(UMSessions).filter(UMSessions.um_accounts_id == user_id).delete()
        session.commit()
    except Exception as e:
        return 'logout_unsuccessful'
    return 'logout_successful'
