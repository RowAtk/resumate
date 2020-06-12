from resumate import nlp
from pprint import pprint
from spacy import displacy
from resumate.iengines.core import PipeLine, Pipe, Keywords, Keyword, isNoun
from resumate.iengines.utils import *


# sentence = "I have a Masters in User Experience Design from the University of Florida from 3 years ago"
sentence = "I got my degree from Northern Caribbean University in Kingston Jamaica about 5 years ago"
sentence = "Computer"
output = "[the ]University of Florida" # expected output

doc = nlp(sentence)
print(doc)

def knowledgeBaseFinder(doc):
    """ find source based on knowledge base """
    return None

#### ENTITY FINDER #####
def entityFinder(doc):
    """ Find source using NE Labels """
    NELABELS = ['ORG']

    # search for entities in key labels
    entities = entitySearch(doc, NELABELS)

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
    return entities[0] if entities else []

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

    # choose approppriate start point
    start = chooseStart(starts)

    # find possible sequences(sources in this case)
    sources = sequenceSearch(doc[start])
    pprint(sources)

    # choose correct sequence(source)
    source = chooseSequence(sources)
    return source

def startSearh(doc):
    """ determine where to start search for sequence using keywords """
    starts = []
    for index, token in enumerate(doc):
        # print(token)
        if token in keywords:
            starts.append(index)
            # print(token)
    return starts if starts else [0]

def chooseStart(starts):
    """ choose correct starting point """
    return starts[0]

def chooseSequence(sequences):
    choice = sequences[0] if sequences else None
    for seq in sequences:
        if len(seq) > len(choice):
            return seq
    return choice

def sequenceSearch(token, seqs=[], seq=[], temp=[]):
    """ Find source based on some sentence analysis """
    if not token:
        return seqs.append(" ".join(seq))
    # print("TOKEN:", token)
    # print("POS:",token.pos_)
    # print(f"PRE VALS: {seqs} {seq} {temp}")
    # print("CHILDREN:", [child for child in token.children], end="\n\n")
    
    if temp == [] and seq == []: 
        if isPOS(token, ['PROPN']): temp += [token.text] 
    else: temp += [token.text]

    lt = seq[:]
    if isPOS(token, ['PROPN']):
        lt += temp
        temp = []

    for child in token.children:
        # print("CHild:", child)
        # print(f"PRE VALS for child {child}: {seqs} {lt} {temp}\n")
        sequenceSearch(child, seqs, lt, temp)
        # print(f"POST VALS for child {child}: {seqs} {lt} {temp}\n")
        temp=[]
    else:
        # print("HIT LEAF")
        sequenceSearch(None, seqs, lt, temp)
    return [s for s in seqs if s!= '']


sourcePipe = PipeLine(doc=doc, pipes=[
    Pipe(knowledgeBaseFinder, name="KB FINDER"),
    Pipe(entityFinder, name="ENTITY FINDER"),
    Pipe(sequenceFinder, name="SEQUENCE FINDER")
])

# how to envoke source inferencing
sourcePipe.run()
