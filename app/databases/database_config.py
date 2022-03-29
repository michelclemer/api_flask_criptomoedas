from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from .. import db

engine = db.create_engine("mysql+pymysql://root:127001@localhost/candles", {})
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
