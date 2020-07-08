from resumate import nlp

from pprint import pprint
from resumate.iengines.utils import *
from resumate.iengines.core import Pipe, IProperty
from word2number import w2n #for converting text numbers to digits
from datetime import datetime, timedelta
from resumate.iengines.education.dateFinder import dateFinder_basic, dateFormatter

"""
Projects would have a definitive start date. Ideally, we want to have an optional end date attached.

"""

dateProjProp = IProperty(
    name='date proj',
    pipes=[
        Pipe(dateFinder_basic, name="Date Finder")
    ],
    questions=[
        'when did you do this project',
        'when did you start this project'
    ],
    followups=[
        'is # when you finished your ! project',
        'did you get that ! degree in #'
    ]
)