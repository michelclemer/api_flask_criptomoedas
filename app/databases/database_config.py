from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from api_flask_criptomoedas.app import db

engine = db.create_engine("mysql+pymysql://root:admin@localhost/candles", {})
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
