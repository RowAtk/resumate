from resumate import nlp

from pprint import pprint
from resumate.iengines.utils import *
from resumate.iengines.core import Pipe, IProperty

"""
Remove stop words from the user's response to the title question and returns a list with a String of the title
Simple Case: "It is called {title}" 

"""

def projTitleFinder(doc=None, txt=""):
    if not doc:
        doc = nlp(txt)

    t = []

    stopWords = nlp.Defaults.stop_words
    stopWords.add("it")

    for token in doc:
        if token.lemma_ in stopWords or token.pos_ in ["PRON"]:
            continue
        else:
            t.append(token.text)
            
    t = " ".join(t)
    return [t]