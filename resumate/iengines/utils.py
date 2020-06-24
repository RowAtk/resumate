from spacy import displacy
from tabulate import _table_formats, tabulate

#========== TABULATION & VISUALIZATION ==========#
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

def noun_chunks(doc):
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append((chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text))
    return chunks

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

def visualization(doc, style='dep'):
    """Visually display relationships between words of a sentence"""
    displacy.serve([doc], style=style)


#========== TOKEN STUFF ==========#
def to_tree(token):
    """Returns a flat list of the children of a token"""
    children = list(token.children)
    if children == []:
        return token.text
    else:
        result = [token.text]
        result.append(list(map(to_tree, children)))
        return result

def entitySearch(doc, ne_labels=[]):
    """ Identify possible sources using NE labels """
    ents = []
    for ent in doc.ents:
        if ent.label_ in ne_labels:
            ents.append(ent)
    return ents

# POS Identifiers
def isNoun(token):
    print(token.pos_)
    return token.pos_ in ['NOUN', 'PROPN', 'PRON']

def isPOS(token, pos_list):
    return token.pos_ in pos_list


def stripTokens(tokenlist, blacklist=['DET'], side='left'):
    """ Strip specifed token from left and/or right of token list """
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