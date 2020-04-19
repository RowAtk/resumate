from resumate import config
# from resumate.knowledge import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

print(config.DevConfig.SQLALCHEMY_DATABASE_URI)
engine = create_engine(config.DevConfig.SQLALCHEMY_DATABASE_URI) # connection

Session = sessionmaker(bind=engine) # db.session

Base = declarative_base() # eqv to db.Model

