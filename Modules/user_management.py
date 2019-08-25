import datetime
import smtplib
import ssl
import uuid

from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError

from Models.user_management import UMAccounts, UMSentMessages, UMSessions
from Models.db import session_scope


def register_user(email: str, raw_password: str):
    """
    Registers the user by creating an account record in the database
    :param email: email of the user
    :param raw_password: direct password inputted by the user into the form
    :return: triggering the login with given data -
    """
    created_at = datetime.datetime.now()
    account_id = uuid.uuid4().hex
    password = sha256_crypt.hash(raw_password)
    new_user = UMAccounts(
        id=account_id,
        email=email,
        hashed_password=password,
        created_at=created_at,
    )
    try:
        with session_scope() as session:
            session.add(new_user)
    except IntegrityError:
        return None, None
    return login(email, raw_password)


def login(email: str, raw_password: str) -> (str, str):
    """
    Log ins the user based on the email and password they provide
    :param email: email of the user
    :param raw_password:direct password inputted by the user into the form
    :return: Session_id and the corresponding account_id or None, None if failed
    """
    with session_scope() as session:
        encrypted_from_db = str(
            session.query(UMAccounts.hashed_password)
            .filter(UMAccounts.email == email)
            .first()[0]
        )
        account_id = (
            session.query(UMAccounts.id)
            .filter(UMAccounts.email == email)
            .first()[0]
        )
    if sha256_crypt.verify(raw_password, encrypted_from_db):
        session_id = create_session_for_user(account_id)
        return session_id, account_id
    return None, None


def create_session_for_user(account_id: str) -> str:
    """
    Creates session for the given user
    :param account_id:
    :return: newly created session_id
    """
    session_id = uuid.uuid4().hex
    created_at = str(datetime.datetime.now())
    new_session = UMSessions(
        um_accounts_id=account_id, session_id=session_id, created_at=created_at
    )
    with session_scope() as session:
        session.add(new_session)
    return session_id


def send_recovery_email(email: str) -> str:
    """
    Sens an email to the user with a link to the recover password page.
    :param email: email of the user
    :return:
    """
    if not user_with_given_email_exists(email):
        return "user_does_not_exist"
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "poryckimarcin@gmail.com"
    password = "s@>-88bQ~[uhkp'd"  # TODO move outside of code

    context = ssl.create_default_context()

    message = "Here's your recovery link!!"  # TODO make into a real link
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)
        log_sending(email, message, "password_reset")
        return "email_sent"
    except Exception as e:
        print(e)
        return "message_not_sent"


def user_with_given_email_exists(email: str) -> bool:
    """
    Verifies whether the provided email belongs to an existing user
    :param email: Provided email
    :return: Boolean with the result of the check of email existence
    """
    with session_scope() as session:
        return (
            session.query(UMAccounts)
            .filter(UMAccounts.email == email)
            .exists()
        )


def log_sending(email: str, message: str, send_event_type: str):
    """
    Saves the log of sending a message in the db
    :param email: Email of the user we had sent the email to
    :param message: Body of the message
    :param send_event_type: Type of sending event
    """
    with session_scope() as session:
        account_id = (
            session.query(UMAccounts)
            .filter(UMAccounts.email == email)
            .first()
            .id
        )
        id = uuid.uuid4().hex
        created_at = datetime.datetime.now()
        sending_log = UMSentMessages(
            um_accounts_id=account_id,
            id=id,
            message_type=send_event_type,
            message_body_plaintext=message,
            created_at=created_at,
        )
        session.add(sending_log)


def change_password(account_id: str, new_password: str) -> str:
    """
    Changes the password for the user
    :param account_id: user's account_id
    :param new_password: user's new password
    :return:
    """
    with session_scope() as session:
        user = (
            session.query(UMAccounts)
            .filter(UMAccounts.id == account_id)
            .first()
        )
        new_password_hash = sha256_crypt.hash(new_password)
        user.hashed_password = new_password_hash
        return "password_changed"
    return "password_not_changed"


def session_exists(session_id: str, account_id: str) -> bool:
    """
    Verifies whether a particular session exists for a particular user
    :return: Boolean value confirming whether the session exists or not
    """
    with session_scope() as session:
        exists_object = (
            session.query(UMSessions)
            .filter(
                UMSessions.session_id == session_id,
                UMSessions.um_accounts_id == account_id,
            )
            .exists()
        )
        return session.query(exists_object).scalar()


def logout(session_id: str, account_id: str) -> str:
    """
    Logouts the user based on session_id and account_id
    :return: string with the information about the logout status
    """
    if session_exists(session_id, account_id):
        with session_scope() as session:
            session.query(UMSessions).filter(
                UMSessions.session_id == session_id
            ).delete()
            return "logout_successful"
    return "logout_unsuccessful"
