import spacy

from pprint import pprint
from word2number import w2n #for converting text numbers to digits
from datetime import datetime, timedelta
from resumate.iengines.utils import *

nlp = spacy.load("en_core_web_sm")

text = ["I got my Masters in User Experience Design last September",
        "I got a BSc in Software Engineering a year ago",
        "I got it in October, 2014",
        "I was certified on the 22nd of March, 2020",
        "I was certified on March 21, 2020"
]

def dateFinder_basic(doc=None, txt=""):
    if not doc:
        doc = nlp(txt)

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
    * {Year} - Prepend "In" to the text if sentence is only a year. Else spacy will assume a number & not a time
    Lvl 2
    timeframe eg: last, next, five, 10, a
    * '{timeframe} year(s)/month(s)/week(s)/day(s)'
    * '{timeframe} year(s) ago'
    Lvl 3
    * the {ordinal} of {Month}, {year}
    * next/last {month Name}
    * Month (no year stated, assume this year intended) - idea for this: prepend "In" to the text
    Brawta - since people probably won't say dates like this
    * '{timeframe} year(s) from now' - Future case
    * next {timeframe} year(s)
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

    lvl2_formats = [
        "year",
        "month",
        "week"
    ]

    # Basic date time checks
    for frm in lvl1_formats:
        try:
            date = datetime.strptime(span.text, frm)
            return date
        except:
            pass
    
    # More nuanced time checks:
    dr = -1
    num = 1
    for frm in lvl2_formats:
        if frm in span.text:
            # Scan span for relevant info
            for tkn in span:
                if tkn.pos_ == 'NUM':
                    try:
                        num = int(tkn.text)
                    except:
                        num = w2n.word_to_num(tkn.text)
                elif tkn.lemma_ in ['next', 'now']:
                    dr = 1 # event in future
                elif tkn.lemma_ in ['ago']:
                    dr = -1 # event in past
            if frm == 'year':
                tmD = timedelta(days=num*365)
            elif frm == 'month':
                tmD = timedelta(days=num*30)
            elif frm == 'week':
                tmD = timedelta(weeks=num)
            
            output = datetime.now()
            output = output + tmD * dr
            return output


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

