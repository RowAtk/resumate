import spacy

from pprint import pprint
from datetime import datetime
from resumate.iengines.utils import *

nlp = spacy.load("en_core_web_sm")

text = ["I got my Masters in User Experience Design last September",
        "I got a BSc in Software Engineering a year ago",
        "I got it in October, 2014",
        "I was certified on the 22nd of March, 2020",
        "I was certified on March 21, 2020"
]

def dateFinder_basic(doc):
    dates = []
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            dates.append(ent)
    return dates

    # can now use datetime module to make sense of all these different date presentations
    # can then convert to a standard datetime object.

def dateFormatter(span):
    """Function takes a spacy span that correspond to a date and attempts to return a 
    datetime object representing the text captured in the span. Returns None if unable to create
    a datetime object
    """

    """
    Comments
    Lvl 1 - transform tokens in the following form
    * {Month} {Day}, {Year}
    * {Month}, {Year}
    * {Year}
    Lvl 2
    timeframe eg: last, next, five, 10, a
    * '{timeframe} year(s)/month(s)/week(s)/day(s)'
    * '{timeframe} year(s) ago'
    Lvl 3
    * the {ordinal} of {Month}, {year}
    * Month (no year stated, assume this year intended)
    Brawta - since people probably won't say dates like this
    * MM/DD/YY (like, who says dates like this)
    * DD/MM/YY
    * YY/MM/DD
    """
    lvl1_formats = [
        "%B %d, %Y",
        "%B, %Y",
        "%B %Y",
        "%Y"
    ]

    # Basic date time checks
    for frm in lvl1_formats:
        try:
            date = datetime.strptime(span.text, frm)
            return date
        except:
            pass
    
    # returns None if no datetime can be found
    return None


# Trial Tests - not actual tests, but functions that make repeated test tasks easier
def test_dateFormatter(index=0, txt=""):
    if not txt:
        span = dateFinder_basic(nlp(text[index]))[0]
    else:

        span = dateFinder_basic(nlp(txt))[0]

    print(dateFormatter(span))
    return dateFormatter(span)

