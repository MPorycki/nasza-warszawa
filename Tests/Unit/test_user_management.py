from passlib.hash import sha256_crypt

from Models.db import session_scope
from Models.user_management import UMAccounts, UMSessions, UMSentMessages
from Modules.user_management import (
    register_user,
    login,
    logout,
    change_password,
    send_recovery_email,
)

"""
Tests TODO
1. Checking created_at for registration
"""


# Registration tests
def test_can_register():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    with session_scope() as session:
        account = session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).first()
        session.query(UMSessions).filter(
            UMSessions.um_accounts_id == account.id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()

    # WHEN
    new_session_id, account_id = register_user(test_email, test_password)

    # THEN
    with session_scope() as session:
        session.query(UMSessions).filter(
            UMSessions.session_id == new_session_id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        assert new_session_id is not None


def test_cant_register_again_with_existing_mail():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    # WHEN
    new_session_id1, user_id1= register_user(
        test_email, test_password
    )
    new_session_id2, user_id2 = register_user(
        test_email, test_password
    )
    # THEN
    try:
        assert new_session_id1 is not None
        assert new_session_id2 is None
    finally:
        # CLEANUP
        session.query(UMSessions).filter(
            UMSessions.session_id == new_session_id1
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()


def test_password_is_hashed_when_registering():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"

    # WHEN
    new_session_id, user_id, message = register_user(test_email, test_password)

    # THEN
    created_user = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
    )
    hashed_password = created_user.hashed_password
    try:
        assert message == "registered"
        assert hashed_password != test_password
    finally:
        # CLEANUP
        session.query(UMSessions).filter(
            UMSessions.session_id == new_session_id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()  # TODO make deletion a method


def test_login_returns_correct_sessionid():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    new_session_id, user_id, message = register_user(test_email, test_password)
    # Removing assigned session_id aka hard logout
    session.query(UMSessions).filter(
        UMSessions.session_id == new_session_id
    ).delete()

    # WHEN
    test_login, test_id = login(test_email, test_password)

    # THEN
    created_user = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
    )
    user_id = created_user.id
    created_session_id = (
        session.query(UMSessions)
        .filter(UMSessions.um_accounts_id == user_id)
        .first()
        .session_id
    )
    try:
        assert test_login == created_session_id
    finally:
        # CLEANUP
        session.query(UMSessions).filter(
            UMSessions.session_id == created_session_id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()


def test_login_returns_correct_userid():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    new_session_id, user_id, message = register_user(test_email, test_password)
    # Removing assigned session_id aka hard logout
    session.query(UMSessions).filter(
        UMSessions.session_id == new_session_id
    ).delete()

    # WHEN
    test_login, test_id = login(test_email, test_password)

    # THEN
    created_user = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
    )
    user_id = created_user.id
    try:
        assert test_id == user_id
    finally:
        # CLEANUP
        session.query(UMSessions).filter(
            UMSessions.um_accounts_id == user_id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()


def test_logout_removes_session():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    register_user(test_email, test_password)
    user_id = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
        .id
    )

    # WHEN
    test_logout = logout(user_id)

    # THEN
    session_for_test_user = (
        session.query(UMSessions)
        .filter(UMSessions.um_accounts_id == user_id)
        .exists()
    )
    exists = session.query(session_for_test_user).scalar()
    try:
        assert exists == False
        assert test_logout == "logout_successful"
    finally:
        # CLEANUP
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()


"""
def test_recovery_email_is_sent(monkeypatch):
    # GIVEN
    monkeypatch.setattr("Modules.user_management.smtplib.sendmail", "")
    test_email = 's15307@pjwstk.edu.pl'
    test_password = '123456789'
    new_session_id, user_id, message = register_user(test_email, test_password)

    # WHEN
    test_send = send_recovery_email(test_email)
x
    # THEN
    try:
        assert test_send == 'email_sent'

    finally:
        # CLEANUP
        session.query(UMSentMessages).filter(UMSentMessages.um_accounts_id == user_id).delete()
        session.query(UMSessions).filter(UMSessions.um_accounts_id == user_id).delete()
        session.query(UMAccounts).filter(UMAccounts.email == test_email).delete()
        session.commit()
"""


def test_can_change_password():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    new_session_id, user_id, message = register_user(test_email, test_password)
    new_password = "abecadlo"
    test_id = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
        .id
    )
    # TODO randomize passwords for security reasons???
    # WHEN
    test_change = change_password(test_id, new_password)

    # THEN
    current_password = (
        session.query(UMAccounts)
        .filter(UMAccounts.email == test_email)
        .first()
        .hashed_password
    )
    try:
        assert sha256_crypt.verify(test_password, current_password) == False
        assert sha256_crypt.verify(new_password, current_password) == True
        assert test_change == "password_changed"
    finally:
        # CLEANUP
        session.query(UMSessions).filter(
            UMSessions.um_accounts_id == user_id
        ).delete()
        session.query(UMAccounts).filter(
            UMAccounts.email == test_email
        ).delete()
        session.commit()
