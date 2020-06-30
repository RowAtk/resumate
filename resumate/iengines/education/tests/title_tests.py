import spacy
import unittest
from resumate.utils import *

from resumate.iengines.education.titleFinder import titleFinder_basic

nlp = spacy.load("en_core_web_sm")



class TitleTests(unittest.TestCase):
    """Identifying titles in text"""


if __name__=="__main__":
    unittest.main()