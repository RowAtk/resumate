# import resumate.knowledge
from resumate import nlp
from pprint import pprint
from spacy import displacy

# 1. find noun clusters (chunks)
# 2. query KB with chunks
# 3. use dependency parsing to make inferences: seeing if the noun chunk is related 
#    to having/obtaining/getting some ceritification
# 4. confirm inferences with user (using follow-ups)

text = "I have a Masters in User Experience Design from Stanford. I also have a BSc. in Software Engineering"
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

displacy.serve(doc, style='dep')


# chunks = noun_clusters(doc)
# pprint(chunks)