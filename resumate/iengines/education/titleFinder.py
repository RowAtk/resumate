import spacy

from pprint import pprint
from utils import *

# kinda lazy: don't want to have to run multiple files. Hence the import of dateFinder here
from dateFinder import dateFinder_basic


nlp = spacy.load("en_core_web_sm")

# text = "I have a Masters in User Experience Design from Stanford. I also got a BSc in Software Engineering"
# text = "I went to Stanford and got a Masters Degree."
# text = "I got my AWS Cert two years ago."
# text = "I have my Bachelors in Economics and my Masters in Social Sciences."
# text = "My masters degree was in Economics and I got it in two years"

# Target text format for basic title finder
text_basic = ["I have a Masters in User Experience Design from Stanford",
              "I have a BSc in Software Engineering",
              "I have a PhD in Psychology",
              "I have an Associate Degree in Web Design",
              "I have a Masters Degree in Web Design and a Bachelors in Computer Science"
]

# The last one is an experiment to consider later

title_words = ["masters", "bsc", "bachelors", "degree", "doctorate", "phd", "associate"]

"""
Task List - Basic Title Finder:
1) Only degree titles. Extract from sentences in the form ...{Degree Title} in {Subject}.
"""

doc = nlp(text_basic[0])


def titleFinder_basic(doc):
    
    # title_words = ["masters", "bsc", "bachelors", "associate", "doctorate", "phd"]
    title = []
    watch = 0

    for token in doc:
        if token.lemma_.lower() in title_words:
            watch = 1
            title.append(token)
            # Consideration here could be to skip the work 'degree' from adding to this list
        elif watch == 1 and token.dep_ == "prep":
            watch = 2
        elif watch == 2 and token.dep_ in ["compound", "pobj"]:
            title.append(token)
        else:
            watch = 0

    return title
        


def titleFinder(doc):
    """Returns a list of tuples, in the form (title: spacy.doc.token, toQuery: Bool). - Idea, could also be a dict
    toQuery dictates if Resumate needs to confirm with the user 
    if the identified title is a title"""
    titles = []

    # KB - simulated
    possessVerbs = ["have", "obtain", "get"]

    # focus on using these hit words over the possessive verb. Hit a particular family of keywords/vocab/thesaurus
    # good heuristic would look for these strong trigger words
    # once we get a hit, do a tree search
    # Additionally, check relationships of links between tokens to ensure hit is relevant
    certs = ["masters", "bsc", "bachelors", "assosciate", "certificate", "degree", "diploma", "qualification"]

    # see if we can find a "thesaurus" tool to check if a word is similar to one of the hot words

    """When you hit a key word, navigate to the appropriate descendants to get the full title"""
    """Figuring out references to 'it'?"""

    for token in doc:
        if token.lemma_ in possessVerbs:
            for c in token.children:
                if c.dep_ not in ["nsubj", "punct", "advmod"]:
                    if c.lemma_.lower() in certs:
                        titles.append((c, False))
                    else:
                        titles.append((c, True))
    print(titles)
    return titles






