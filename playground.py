from resumate.iengines.utils import *
from resumate import nlp
from textblob import TextBlob

doc = nlp("UTECH")
ne_info(doc)

while True:
    break
    res = TextBlob(input("Insert text: "))
    debug(f'Response polarity: {res.sentiment.polarity}')
    debug(f'Response subjectivity: {res.sentiment.subjectivity}')
    