from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import SQLALCHEMY_DATABASE_URI

#import all table-files
from model import MatchStatistics

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)

def save_to_database():

    MatchStatistics.__table__.create(engine)

    session.commit()

    session.remove()

save_to_database()