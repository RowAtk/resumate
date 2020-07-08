from resumate import nlp

from pprint import pprint
from resumate.iengines.utils import *
from resumate.iengines.core import Pipe, IProperty

"""
Level 0
Simply accepts all the User has said, remove stop words and regurgitates for project description & achievements. 
Separates sentences into lists

"""

def desc_achFinder(doc=None, txt=""):
    if not doc:
        doc = nlp(txt)

    t = []

    stopWords = nlp.Defaults.stop_words
    stopWords.add("it")
    stopWords.add("I")

    for token in doc:
        if ((token.lemma_ in stopWords or token.pos_ in ["PRON"]) and token.dep_ not in ["prep"]):
            continue
        else:
            
            t.append(token.text)

            
            
    t = " ".join(t)
    return [t]

descProp = IProperty(
    name='description',
    pipes=[
        Pipe(desc_achFinder, name='descFinder')
    ],
    questions=[
        'describe what your project is about'
    ],
    followups=[
        'tell me what # is about'
    ]
)

achieveProp = IProperty(
    name='achieve',
    pipes=[
        Pipe(desc_achFinder, name='achieveFinder')
    ],
    questions=[
        'what did you accomplish in this project'
    ],
    followups=[
        'is # something you accomplished on this project'
    ]
)