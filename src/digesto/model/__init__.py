import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@contextlib.contextmanager
def obtener_session(echo=False):
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASSWORD'],
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT',5432),
        os.environ['DB_NAME']
    ), echo=echo)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
