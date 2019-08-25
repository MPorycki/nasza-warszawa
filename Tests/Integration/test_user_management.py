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


def um_accounts_teardown(email):
    with session_scope() as session:
        session.query(UMAccounts).filter(UMAccounts.email == email).delete()


# Registration tests
def test_can_register():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    um_accounts_teardown(test_email)

    # WHEN
    new_session_id, account_id = register_user(test_email, test_password)

    # THEN
    um_accounts_teardown(test_email)
    assert new_session_id is not None


def test_cant_register_again_with_existing_mail():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"

    # WHEN
    new_session_id1, user_id1 = register_user(test_email, test_password)
    new_session_id2, user_id2 = register_user(test_email, test_password)

    # THEN
    um_accounts_teardown(test_email)
    assert new_session_id1 is not None
    assert new_session_id2 is None


def test_password_is_hashed_when_registering():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"

    # WHEN
    new_session_id, user_id = register_user(test_email, test_password)

    # THEN
    with session_scope() as session:
        created_user = (
            session.query(UMAccounts)
            .filter(UMAccounts.email == test_email)
            .first()
        )
        um_accounts_teardown(test_email)
        assert new_session_id is not None
        assert created_user.hashed_password != test_password


def test_login_returns_correct_data(monkeypatch):
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    monkeypatch.setattr(
        "Modules.user_management.register_user", lambda x, y: login(x, y)
    )

    # WHEN
    test_login, test_id = register_user(test_email, test_password)

    # THEN
    with session_scope() as session:
        user_id = (
            session.query(UMAccounts)
            .filter(UMAccounts.email == test_email)
            .first()
            .id
        )
        created_session_id = (
            session.query(UMSessions)
            .filter(UMSessions.um_accounts_id == user_id)
            .first()
            .session_id
        )
        um_accounts_teardown(test_email)
        assert test_login == created_session_id
        assert test_id == user_id


def test_logout_removes_session():
    # GIVEN
    test_email = "testinek@gmail.com"
    test_password = "123456789"
    test_session_id, test_account_id = register_user(test_email, test_password)

    # WHEN
    test_logout = logout(test_session_id, test_account_id)

    # THEN
    with session_scope() as session:
        session_for_test_user = (
            session.query(UMSessions)
            .filter(
                UMSessions.um_accounts_id == test_account_id,
                UMSessions.session_id == test_session_id,
            )
            .exists()
        )
        exists = session.query(session_for_test_user).scalar()
        um_accounts_teardown(test_email)
        assert test_logout == "logout_successful"
        assert exists is False


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
    new_session_id, account_id = register_user(test_email, test_password)
    new_password = "abecadlo"

    # WHEN
    test_change = change_password(account_id, new_password)

    # THEN
    with session_scope() as session:
        current_password = (
            session.query(UMAccounts)
            .filter(UMAccounts.email == test_email)
            .first()
            .hashed_password
        )
        assert sha256_crypt.verify(test_password, current_password) is False
        assert sha256_crypt.verify(new_password, current_password) is True
        assert test_change == "password_changed"
        um_accounts_teardown(test_email)
