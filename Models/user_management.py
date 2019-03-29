from sqlalchemy import Column, String, TIMESTAMP, ForeignKey

from .db import base


class UMAccounts(base):
    __tablename__ = 'um_accounts'

    id = Column(String(length=32), primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=True)


class UMSessions(base):
    __tablename__ = 'um_sessions'

    UM_accounts_id = Column(String(length=32),
                            ForeignKey(UMAccounts.id, onupdate='CASCADE', ondelete='CASCADE'))
    session_id = Column(String(length=32), primary_key=True)
    created_at = Column(TIMESTAMP)


class UM_sent_messages(base):
    __tablename__ = 'UM_sent_messages'

    UM_accounts_id = Column(String(length=32),
                            ForeignKey(UMAccounts.id, onupdate='CASCADE', ondelete='CASCADE'))
    id = Column(String(length=32), primary_key=True)
    message_type = Column(String(length=16))
    message_body_plaintext = Column(String)
    created_at = Column(TIMESTAMP)
