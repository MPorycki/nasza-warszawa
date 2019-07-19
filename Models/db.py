from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine(
    "postgresql+psycopg2://MCAdmin:uwq8SZYxC<V6HR2et["
    ":c5gW!wtC4Hm%e@responsible-citizen-db.cqtzg8fun5lr.us-east-2.rds.amazonaws"
    ".com:5432/responsible_citizen")  # TODO make it more secure
base = declarative_base()
Session = sessionmaker(db)
session = Session()


@contextmanager
def session_scope(_session=None):
    if _session is None:
        _session = Session()

    try:
        yield _session
        _session.commit()
    except Exception:
        _session.rollback()
        raise
    finally:
        _session.close()
