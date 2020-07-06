from resumate import nlp
from resumate.iengines.core import Pipe, Keywords, Keyword, isNoun, IProperty
from resumate.iengines.utils import *


sentence = "I have a Masters in User Experience Design from the University of Florida from 3 years ago"
# sentence = "I got my degree from Northern Caribbean University in Kingston Jamaica about 5 years ago"
# sentence = "UTECH"
output = "[the ]University of Florida" # expected output

doc = nlp(sentence)

def knowledgeBaseFinder(doc):
    """ find source based on knowledge base """
    return None

#### ENTITY FINDER #####
def entityFinder(doc):
    """ Find source using NE Labels """
    NELABELS = ['ORG']
    BLACKLIST = ['bachelor', 'master', 'marine life biology']

    # search for entities in key labels
    entities = entitySearch(doc, NELABELS, BLACKLIST)

    # clean entities of any unwanted tokens
    entities = entityCleaner(entities)

    # choose appropriate entity
    entity = entityChooser(entities)
    return entity

def entityCleaner(entities):
    """ clean raw entity from pipe """
    ents = []
    for entity in entities:
        ents.append(stripTokens(entity, side='left'))       
    return ents

def entityChooser(entities):
    """ choose suitable entity from list """
    return entities if entities else []

### SEQUENCE FINDER ######
# keywords to aid find search start
keywords = Keywords([
    Keyword('at', pos='ADP', match_case=False), 
    Keyword('from', pos='ADP', match_case=False)
])

""" SEQUENCE PIPE """
def sequenceFinder(doc):
    """ steps to find source using sequence hunting """
    # find start point to begin search
    starts = startSearh(doc)
    if starts:
        # choose approppriate start point
        start = chooseStart(starts)

        # find possible sequences(sources in this case)
        sources = sequenceSearch(doc[start])
        # debug(sources, pretty=True)

        # choose correct sequence(source)
        source = chooseSequence(sources)
        return source
    return None

def startSearh(doc):
    """ determine where to start search for sequence using keywords """
    starts = []
    for index, token in enumerate(doc):
        if token in keywords:
            starts.append(index)
    return starts if starts else None

def chooseStart(starts):
    """ choose correct starting point """
    return starts[0]

def chooseSequence(sequences):
    # return sequences
    choice = sequences[0] if sequences else None
    for seq in sequences:
        if len(seq) > len(choice):
            return seq
    return choice

def sequenceSearch(token, seqs=[], seq=[], temp=[]):
    """ Find source based on some sentence analysis """
    if not token:
        return seqs.append(" ".join(seq))
    
    if temp == [] and seq == []: 
        if isPOS(token, ['PROPN']): temp += [token.text] 
    else: temp += [token.text]

    lt = seq[:]
    if isPOS(token, ['PROPN']):
        lt += temp
        temp = []

    for child in token.children:
        sequenceSearch(child, seqs, lt, temp)
        temp=[]
    else:
        sequenceSearch(None, seqs, lt, temp)
    return [s for s in seqs if s!= '']

# make IE Property
sourceProp = IProperty(
    name='source',
    pipes=[
        Pipe(knowledgeBaseFinder, name="KB FINDER"),
        Pipe(entityFinder, name="ENTITY FINDER"),
        Pipe(sequenceFinder, name="SEQUENCE FINDER")
    ],
    questions=[
        'where did you get your degree',
        'where did you get your # degree'
    ],
    followups=[
        'was it ! where you got your # degree',
        'did you get your # degree from !',
    ]
)
