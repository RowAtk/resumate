import nltk, spacy
from resumate.knowledge import Session
from resumate.knowledge.models import NERLabelWords
from resumate.prompter import Question

session = Session()

class PromptSubject():

    def __init__(self, name, nlid, tags, plural=False):
        super().__init__()
        self.name = name
        self.nlid = nlid
        self.pos = nltk.pos_tag(name)
        self.tags = tags
        self.plural = plural


title_p_subj = PromptSubject(
    name = "title", 
    nlid ="degree/cretifications", 
    tags = ['gift', 'award', 'goal', 'reward', 'present'], 
    plural = True
)

list_of_stuff = [
    "police station", 
    "Google", 
    "to", 
    "Rowan E. Atkinson", 
    "U.S.",
    "I received my Bachelor of Science at the", 
    "University of South Florida"
]

# NLTK TRY
# sent = nltk.corpus.treebank.tagged_sents()[22]
# print(nltk.ne_chunk(sent))

# pos = nltk.pos_tag(list_of_stuff)
# ne = nltk.ne_chunk(pos)
# print(pos)
# print(ne)

# title_question = Question(title_p_subj)
# print(title_question)


#spaCy TRY
nlp = spacy.load("en_core_web_sm")
text = " ".join(list_of_stuff)
doc = nlp("Apple")

def getLabel(words):
    words = words if type(words) == list else [words]
    labels = []
    for word in words:
        if doc.ents:
            labels.append(doc.ents[0].label_)
        else:
            labels.append([0].pos_)
    return labels if len(labels) > 1 else labels[0]
        

label = getLabel(" ".join(list_of_stuff))
print(label)
# query = session.query(NERLabelWords).filter(NERLabelWords.label == label).one()

# label_word = query.words.split()[0]
# print(label_word)


# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop, sep="\t")

