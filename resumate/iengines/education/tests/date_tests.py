import spacy
import unittest
from resumate.utils import *

from resumate.iengines.education.dateFinder import dateFinder_basic

nlp = spacy.load("en_core_web_sm")

text = ["I got my Masters in User Experience Design last September",
        "I got a BSc in Software Engineering a year ago",
        "I got it October 2014",
        "I was certified on the 22nd of March, 2020",
        "I was certified March 21, 2020"
]


class DateTests(unittest.TestCase):
    """Test the datefinder module"""

    def setUp(self):
        """Run before each test"""
        pass

    def tearDown(self):
        """Run after each test"""
        pass

    def test_date_year_only(self):
        text = "I got my first degree two years ago"
        expect = "two years ago"

        response = dateFinder_basic(nlp(text))
        print(response)
        self.assertIn(expect, response[0].text)

    def test_in_yyyy_format_only(self):
        """Tests for the year they receive the degree"""
        text = "I completed my degree in 2015"
        expect = "2015"

        response = dateFinder_basic(nlp(text))
        print(response)
        self.assertIn(expect, response[0].text)

    def test_full_date_mdy(self):
        """Tests for date in format Month dd, yyyy"""
        text = "I graduated on November 3, 2019"
        expect = "November 3, 2019"

        response = dateFinder_basic(nlp(text))
        print(response)
        self.assertIn(expect, response[0].text)

if __name__=="__main__":
    unittest.main()