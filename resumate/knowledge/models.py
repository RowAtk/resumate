from resumate.knowledge import Base
from sqlalchemy import Column, Integer, String

class Major(Base):
    __tablename__ = "majors"
    
    id = Column(Integer, primary_key=True)
    major = Column(String)
    major_category = Column(String)

    def __init__(self, major, category):
        self.major = major
        self.major_category = category

    def __repr__(self):
        return f"<Major(major={self.major}, major_category={self.major_category} )>"



class CertAbv(Base):
    __tablename__ = "cert_abbreviations"

    certification = Column(String, primary_key=True)
    abbreviation = Column(String(20))

    def __init__(self, certification, abbreviation):
        self.certification = certification
        self.abbreviation = abbreviation

    def __repr__(self):
        return f"<CertAbv(certification={self.certification}, abbreviation={self.abbreviation})>"



class NERLabelWords(Base):
    __tablename__ = "ner_label_words"

    # labelid = Column(Integer, primary_key=True)
    label = Column(String, primary_key=True)
    words = Column(String)

    def __init__(self, labelid, label, words):
        self.labelid = labelid
        self.label = label
        self.words = words

    def __repr__(self):
        return f"<NERLabelWords(label={self.label}, words={self.words.split()})>"
