from resumate import nlp
from pprint import pprint
from spacy import displacy
from tabulate import _table_formats, tabulate

class Keywords():

    def __init__(self, keywords):
        self.keywords = keywords
    
    def __contains__(self, token):
        match = True
        for keyword in self.keywords:
            if keyword == token:
                return True
        return False

class Keyword():

    def __init__(self, text, pos=None, tag=None, dep=None, head=None, root=None):
        self.text = text
        self.pos = pos
        self.tag = tag
        self.dep = dep
        self.head = head
        self.root = root

    def __eq__(self, token):
        match = self.text == token.text and \
        (self.pos == token.pos_ if self.pos else True) and \
        (self.tag == token.tag_ if self.tag else True) and \
        (self.dep == token.dep_ if self.dep else True) and \
        (self.head == token.head.text if self.head else True)

        return match

sentence = "I have a Masters in User Experience Design from the University of Florida from 3 years ago"
sentence = "I got my degree from the University of Technology in Kingston Jamaica about 5 years ago"
output = "[the ]University of Florida" # expected output

doc = nlp(sentence)

def visualization(style='dep'):
    displacy.serve([doc], style=style)

def noun_clusters(doc):
    """ return noun chunks of text. in the form of: Text, Root.text, Root.Dep tag, Root.Head """
    headers = ['Text', 'Root Text', 'Root Dep', 'Root Head Text']
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append((
            chunk.text, 
            chunk.root.text, 
            chunk.root.dep_,
            chunk.root.head.text
        )) 
    print(tabulate(chunks, headers=headers, tablefmt='fancy_grid'))

# words to look for: at, from
def token_info(doc):
    headers = ['Text', 'Lemma', 'POS', 'Tag', 'Dep', 'Head text', 'Head POS', 'Children']
    results = []
    for token in doc:
        results.append([
            token.text, 
            token.lemma_, 
            token.pos_, 
            token.tag_,
            token.dep_, 
            token.head.text, 
            token.head.pos_, 
            [child for child in token.children]])
    print(tabulate(results, headers=headers, tablefmt='fancy_grid'))

def ne_info(doc):
    """ return info of named entities in doc in the form of:  """
    headers = ['Text', 'NE Label', 'Start', 'End']
    ents = []

    for ent in doc.ents:
        ents.append((
            ent.text, 
            ent.label_, 
            ent.start_char,
            ent.end_char
        )) 
    print(tabulate(ents, headers=headers, tablefmt='fancy_grid'))

def isNoun(token):
    print(token.pos_)
    return token.pos_ in ['NOUN', 'PROPN', 'PRON']

# token_info(doc, view=True)
# noun_clusters(doc, view=True)

# doc = nlp("the University of Florida")
# token_info(doc, view=True)
# noun_clusters(doc, view=True)
# displacy.serve([doc], style='dep')
                
        # check if head is 
    # if token.dep_ == 'prep'

# named entity search
NELABELS = ['ORG']
ne_info(doc)

def entitySearch(doc):
    """ Identify possible sources using NE labels """
    ents = []
    for ent in doc.ents:
        if ent.label_ in NELABELS:
            ents.append(ent)
    return ents

def entityCleaner(entities):
    """ clean raw entity from pipe """
    ents = []
    for entity in entities:
        ents.append(stripTokens(entity, side='left'))       
    return ents

def entityChooser(entities):
    """ choose suitable entity from list """
    return entities[0]

def entityPipe(doc):
    entities = entitySearch(doc)
    if entities:
        entities = entityCleaner(entities)
        entity = entityChooser(entities)
    return entity

def stripTokens(tokenlist, blacklist=['DET'], side='left'):
    # left strip
    if side == 'left' or side == 'both':
        x = 0 
        dirty = True
        while dirty and x < len(tokenlist):
            if tokenlist[x].pos_ not in blacklist:
                tokenlist = tokenlist[x:]
                dirty = not dirty
            x += 1

    if side == 'right' or side == 'both':
        x = len(tokenlist) - 1
        dirty = True
        while dirty and x > -1:
            if tokenlist[x].pos_ not in blacklist:
                tokenlist = tokenlist[x:]
                dirty = not dirty
            x -= 1
    
    return tokenlist

entity = entityPipe(doc)
print(entity)

# knowledge base search
# have to gather data... skipping....

# Sentence Analyzer Pipe


""" SEQUENCE PIPE """
def sequencePipe(doc):
    """ steps to find source using sequence hunting """

    # keywords to aid find search start
    keywords = Keywords([
        Keyword('at', pos='ADP', dep='prep'), 
        Keyword('from', pos='ADP', dep='prep')
    ])

    # find start point to begin search
    start = startSearh(doc, keywords)

    # find possible sequences(sources in this case)
    sources = findSequence(doc[start])

    # choose correct sequence(source)
    source = chooseSequence(sources)
    return source



def startSearh(doc, keywords):
    """ determine where to start search for sequence using keywords """
    starts = []
    for index, token in enumerate(doc):
        if token in keywords:
            starts.append(index)
            print(token)
    return chooseStart(starts) if starts else None

def chooseStart(starts):
    """ choose correct starting point """
    return starts[0]

def makeSequence(token, seq=[], temp=[]):
    """ make sequence starting with Noun child of token and ending with a leaf """
    children = [child for child in token.children]
    print("TOKEN:", token)
    print("CHILDREN:", children)
    if children == []:
        print("\nCOMPLETE SEQUENCE\n\n")
        return seq
    
    seqs = []
    for child in children:
        print("CHILD:", child)
        temp.append(child.text)
        if isNoun(child):
            print("is a noun")
            seq += temp
            temp = []
        
        print("TEMP:",temp)
        print("CURRENT SEQUENCE:", seq, end="\n\n")
        seqs.append(" ".join(makeSequence(child, seq, temp)))
        print("SEQUENCES:",seqs)
    print(seqs) 
    return seqs   

def findSequence(token):
    """ find sequences starting at the children at designated token """
    seqs = []
    print("INIT CHILDREN:", list(token.children))
    for child in token.children:
        s = sequenceSearch(child, seq=[], temp=[])
        print("SEARCH RES:",s, end="\n\n")
        seqs.append(" ".join(s))
    print(seqs)
    return seqs

def sequenceSearch(token, seq, temp):
    """ search children for sequence N*N """
    print("\n\n",token)
    print("PRE SEQ:", seq)
    pre_seq = seq
    if not token:
        print("HIT LEAF\n")
        return seq
    
    temp.append(token.text)
    if isNoun(token):
        seq += temp
        temp = []    
    
    print("SEQ", seq)
    print("TEMP", temp)
    print("CHILDREN:", list(token.children))

    for child in token.children:
        pre_seq = seq
        print("CHILDREN EXIST:", child)
        print("PRE VALS:\n",child, pre_seq,seq, temp)
        sequenceSearch(child, pre_seq, temp)
        print("POST VALS:\n",child, pre_seq,seq, temp)
        temp = []
    else:
        print("NO CHILLUN")
        #sequenceSearch(None, seq, temp)
    return seq 

def chooseSequence(sequences):
    return sequences[0]
    
# doc = nlp("Harry is a Firetruck stuck in denial")
# token_info(doc)
# start = startSearh(doc, keywords)
# # makeSequence(doc[1])
# findSequence(doc[start])

# print("ENTITY SOURCE:", entityPipe(doc))
print("SEQUENCE SOURCE:", sequencePipe(doc))

# token_info(doc)


# def fs(token)