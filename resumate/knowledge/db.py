from resumate.knowledge import Session, Base, engine
# import resumate.knowledge
from resumate.knowledge.models import Major, CertAbv
from resumate.utils.file_cleaner import abv_cleaner, fileToDF


# INSTANTIATE KNOWLEDGE BASE OF RESUMATE

def create_database():
    # create database schema
    Base.metadata.create_all(engine)

def destroy_database():
    # create database schema
    Base.metadata.drop_all(engine)

def recreate_database():
    destroy_database()
    create_database()

def insertDataFrame(data, tablename):
    data.to_sql(tablename, con=engine, if_exists='replace')

def fillWithKnowledge():

    # certification abbreviations
    data = abv_cleaner('certabv.tsv')
    insertDataFrame(data, 'cert_abbreviations')

    # NER label words
    data = fileToDF('ner-label-words.csv')
    insertDataFrame(data, 'ner_label_words')


#recreate db
recreate_database()

# create new session
session = Session()
fillWithKnowledge()
session.close()
