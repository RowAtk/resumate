import spacy

from pprint import pprint
from utils import *

nlp = spacy.load("en_core_web_sm")

text = ["I got my Masters in User Experience Design last September",
        "I got a BSc in Software Engineering a year ago",
        "I got it October 2014",
        "I was certified on the 22nd of March, 2020",
        "I was certified March 21, 2020"
]

def dateFinder_basic(doc):
    dates = []
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            dates.append(ent)
    return dates

    # can now use datetime module to make sense of all these different date presentations
    # can then convert to a standard datetime object.