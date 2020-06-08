from spacy import displacy
from tabulate import _table_formats, tabulate

def noun_chunks(doc):
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append((chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text))
    return chunks

def to_tree(token):
    """Returns a flat list of the children of a token"""
    children = list(token.children)
    if children == []:
        return token.text
    else:
        result = [token.text]
        result.append(list(map(to_tree, children)))
        return result

def token_info(doc, view=False):
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
    if view:
        print(tabulate(results, headers=headers, tablefmt='fancy_grid'))
    return results

def dependencyDiagram(doc):
    """Visually display relationships between words of a sentence"""
    displacy.serve(doc, style='dep')