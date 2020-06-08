# import resumate.knowledge
from resumate import nlp
from pprint import pprint
from spacy import displacy
from tabulate import _table_formats, tabulate
# 1. find noun clusters (chunks)
# 2. query KB with chunks
# 3. use dependency parsing to make inferences: seeing if the noun chunk is related 
#    to having/obtaining/getting some ceritification
# 4. confirm inferences with user (using follow-ups)

text = "I have a Masters in User Experience Design from Stanford. I also have a BSc. in Software Engineering"
text = "I have a Masters in User Experience Design" # from my favourite place, the University of the West Indies."
text2 = "a Masters in User Experience Design" # from my favourite place, the University of the West Indies."

output = "Masters [in] User Experience Design" #expected output
doc = nlp(text)

def noun_clusters(doc):
    """ return noun chunks of text. in the form of: Text, Root.text, Root.Dep tag, Root.Head """
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append((
            chunk.text, 
            chunk.root.text, 
            chunk.root.dep_,
            chunk.root.head.text
        )) 
    return chunks  

mock_db = {
    "keywords": ["Bachelor", "Master", "Certificate"],
    "subject": []
}

def title(doc): 
    """ title returns a list of tuples in the form: (titleName: Str, toQuery: Bool)  """
    titles = []
    chunks = noun_clusters(doc)
    # method 1 - knowledge base matching
    keywords = mock_db["keywords"]
    for chunk in chunks:
        if chunk.root.text in keywords:
            titles.append(chunk.root.text)
    # method 2

def token_children(doc, view=False):
    headers = ['Text',	'Dep', 'Head text',	'Head POS', 'Children']
    results = []
    for token in doc:
        results.append([token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children]])
    if view:
        print(tabulate(results, headers=headers, tablefmt='fancy_grid'))
    return results      

token_children(doc, view=True)
# displacy.serve([doc, nlp('I have my CCNA and various other CISCO certificates.')], style='dep')
displacy.serve([doc, nlp(text2)], style='dep')




# format_list = list(_table_formats.keys())
# # current format list in tabulate version 0.8.3:
# # ['simple', 'plain', 'grid', 'fancy_grid', 'github', 'pipe', 'orgtbl', 'jira', 'presto', 'psql', 'rst', 'mediawiki', 'moinmoin', 'youtrack', 'html', 'latex', 'latex_raw', 'latex_booktabs', 'tsv', 'textile']


# # Each element in the table list is a row in the generated table
# table = [["spam",42], ["eggs", 451], ["bacon", 0]]
# headers = ["item", "qty"]

# for f in format_list:
#     print("\nformat: {}\n".format(f))
#     print(tabulate(table, headers, tablefmt=f))


# chunks = noun_clusters(doc)
# pprint(chunks)