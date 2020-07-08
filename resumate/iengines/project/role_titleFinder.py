from resumate import nlp

from pprint import pprint
from resumate.iengines.utils import *
from resumate.iengines.core import Pipe, IProperty

"""
Remove stop words from the user's response to the title question and returns a list with a String of the title
Simple Case: "It is called {title}" 

Also includes the Role Finder

"""

def projTitleFinder(doc=None, txt=""):
    if not doc:
        doc = nlp(txt)

    t = []

    stopWords = nlp.Defaults.stop_words
    stopWords.add("it")

    for token in doc:
        if (token.lemma_ in stopWords or token.pos_ in ["PRON"]):
            if token.text.lower() in ["and"]:
                # separate compound phrases with a full stop
                t.append(".")
            continue
        else:
            t.append(token.text)

            
            
    t = " ".join(t)
    return [t]

projTitleProp = IProperty(
    name='proj title',
    pipes=[
        Pipe(projTitleFinder, name='projTitleFinder')
    ],
    questions=[
        'what is the name of your project'
    ],
    followups=[
        'is # the name of your project'
    ]
)

roleProp = IProperty(
    name='role',
    pipes=[
        Pipe(projTitleFinder, name='roleFinder')
    ],
    questions=[
        'what was your role on this project'
    ],
    followups=[
        'is # your role on this project'
    ]
)