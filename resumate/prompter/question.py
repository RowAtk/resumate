# from resumate import nltk
from resumate.knowledge import Session

""" What are some degrees/certificates you have attained? """
""" 
BREAKDOWN
------------
WHAT - article
IS/ARE - singular/plural
degrees/cert - NL identifier of prompt subject
you - user
have - ??
attained - action associated with prompt subject

Prompt Subject - real topic on which the question is gathering info 
"""

session = Session()
USER = "You"

def user(subj=False):
    if subj:
        return USER
    return USER.lower()

class Question():
    """ class representing a question """
    
    def __init__(self, p_subj):
        """ p_subj : PromptSubject """
        super().__init__()
        self.p_subj = p_subj
    
    def article(self): # What
        """ find the articles related to p_subj POS """
        # session.query()
        pass

    def number(self): #some
        """ Find number (sing/plur) article of pp_subj """
        # session
        pass

    def action(self): # have attained / attained
        """ return action related to p_subj w/ aid of knowledge base or model """
        pass

    def __repr__(self):
        # return f"{self.article()} {self.number()} {34} {self.p_subj.nlid} {user()} {self.action()}"
        return f"{self.article()} {self.number()} {34} {self.p_subj.nlid} {user()}"

        
""" 
class PromptSubject():

    def __init__(self, name, nlid, tags):
        super().__init__()
        self.name = name
        self.nlid = nlid
        self.pos = nltk.pos_tag(name)
        self.tags = tags
"""