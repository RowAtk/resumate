import spacy
import unittest
from resumate.utils import *

from resumate.resumate.iengines.education.dateFinder import dateFinder_basic

nlp = spacy.load("en_core_web_sm")

class TitleTests(unittest.TestCase):
    """Identifying titles in text"""

class DateTests(unittest.TestCase):
    """Test the datefinder module"""

    def test_date_year_only(self):
        text = "I got my first degree two years ago"
        expect = "two years ago"

        response = dateFinder_basic(nlp(text))
        print(response)
        self.assertIn(expect, response)

if __name__=="__main__":
    unittest.main()