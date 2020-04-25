from resumate.knowledge import Session, Base, engine
# import resumate.knowledge
from resumate.knowledge.models import Major, CertAbv
from resumate.knowledge.file_cleaner import tsv_cleaner


def create_database():
    # create database schema
    Base.metadata.create_all(engine)

def destroy_database():
    # create database schema
    Base.metadata.drop_all(engine)


def recreate_database():
    destroy_database()
    create_database()

#recreate db
recreate_database()

# create new session
session = Session()

# get data (DF)
data = tsv_cleaner('certabv.tsv')

data.to_sql('cert_abbreviations', con=engine, if_exists='replace')

session.query(CertAbv)


# for record in data:
#     certabv = Cer








