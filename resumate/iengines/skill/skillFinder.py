import spacy

from pprint import pprint
from resumate.iengines.utils import *

nlp = spacy.load("en_core_web_sm")


# def skillFinder(doc=None, txt=''):
#     """Takes a doc object (or string) and attempts to interpret skills implied in the string."""
#     if not doc:
#         doc = nlp(txt)

#     pass

def hardSkillFinder(doc=None, txt=''):
    """Takes a doc object (or string) and attempts to interpret the hard technical skills implied in the string"""
    if not doc:
        doc = nlp(txt)

    pass

def softSkillFinder(doc=None, txt=''):
    """Takes a doc object (or string) and attempts to interpret the soft skills implied in the string"""
    if not doc:
        doc = nlp(txt)

    pass