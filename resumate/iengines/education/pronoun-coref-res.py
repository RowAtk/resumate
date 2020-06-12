import spacy

from pprint import pprint
from utils import *


"""
One of our biggest challenges, which spaCy doesn't solve by default, is pronoun coreference resolution: determining
what noun a pronoun is mapped to. The functions below attempt a best guess attempt to do this with the following
heuristics
"""

nlp = spacy.load("en_core_web_sm")

