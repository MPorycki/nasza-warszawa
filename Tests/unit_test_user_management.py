from Models.db import session
from Models.user_management import UMAccounts, UMSessions
from Modules.user_management import register_user, login, logout

"""
Tests TODO
1. Checking created_at for registration
"""


# Registration tests
def test_can_register():
    # GIVEN
    test_email = 'testinek@gmail.com'
    test_password = '123456789'

    # WHEN
    test_register = register_user(test_email, test_password)

    # THEN
    try:
        assert test_register == 'registered'
    finally:
        # CLEANUP
        session.query(UMAccounts).filter(UMAccounts.email == test_email).delete()
        session.commit()


def test_cant_register_again_with_existing_mail():
    # GIVEN
    test_email = 'testinek@gmail.com'
    test_password = '123456789'
    # WHEN
    test_register1 = register_user(test_email, test_password)
    test_register2 = register_user(test_email, test_password)
    # THEN
    try:
        assert test_register1 == 'registered'
        assert test_register2 == 'email_already_in_db'
    finally:
        # CLEANUP
        session.query(UMAccounts).filter(UMAccounts.email == test_email).delete()
        session.commit()


def test_password_is_hashed_when_registering():
    # GIVEN
    test_email = 'testinek@gmail.com'
    test_password = '123456789'

    # WHEN
    test_register = register_user(test_email, test_password)

    # THEN
    created_user = session.query(UMAccounts).filter(UMAccounts.email == test_email).first()
    hashed_password = created_user.hashed_password
    try:
        assert test_register == 'registered'
        assert hashed_password != test_password
    finally:
        # CLEANUP
        session.query(UMAccounts).filter(UMAccounts.email == test_email).delete()
        session.commit()  # TODO make deletion a method


def test_check_pass_returns_correct_sessionid():
    # GIVEN
    test_email = 'testinek@gmail.com'
    test_password = '123456789'
    register_user(test_email, test_password)

    # WHEN
    test_login = login(test_email, test_password)

    # THEN
    created_user = session.query(UMAccounts).filter(UMAccounts.email == test_email).first()
    user_id = created_user.id
    created_session_id = session.query(UMSessions).filter(
        UMSessions.um_accounts_id == user_id).first().session_id
    try:
        assert test_login == created_session_id
    finally:
        session.query(UMSessions).filter(UMSessions.session_id == created_session_id).delete()
        session.query(UMAccounts).filter(UMAccounts.email == test_email).delete()
        session.commit()


def test_logout_removes_session():
    # GIVEN
    test_email = 'testinek@gmail.com'
    test_password = '123456789'
    register_user(test_email, test_password)
    login(test_email, test_password)
    user_id = session.query(UMAccounts).filter(UMAccounts.email == test_email).first().id

    # WHEN
    test_logout = logout(user_id)

    # THEN
    session_for_test_user = session.query(UMSessions).filter(
        UMSessions.um_accounts_id == user_id).exists()
    exists = session.query(session_for_test_user).scalar()
    assert exists == False
    assert test_logout == 'logout_successful'
