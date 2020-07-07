# Make IEngine with IProperties
from resumate.iengines.core import IEngine, IObject
from resumate.iengines.education.source import sourceProp
from resumate.iengines.education.titleFinder import titleProp
from resumate.iengines.education.dateFinder import dateProp
from resumate.iengines.utils import *

properties = [
    titleProp,
    sourceProp,
    dateProp
]

questions = [
    "what academic degrees have you attained",
    "tell me about some of your degrees"
]

mquestions = [

]

confirmations = [
    "i have some more questions about your education, but we could stop here. Do you want to continue",
    # "are there any other degrees you would like to mention",
    # "any other degrees you might have forgotten"
    "do you wish to keep talking about education",
    "i have more to ask about your education, can we continue"
]

# Make Degree class - store all data and the logic to assess it
class Degree(IObject):
    """ Class to represent information stored on a degree """

    def __init__(self, properties):
        super().__init__(properties)        

    def isAcceptable(self):
        """ Does object meet minimum criteria """
        needed = ['title', 'source']
        for need in needed:
            if not self.properties[need]:
                return False
        return True

    def default_candidates(self):
        return [self.properties['title']] if self.properties['title'] else []

    def __repr__(self):
        return f'<Degree title={self.properties[titleProp.name]}, source={self.properties[sourceProp.name]}, date={self.properties[dateProp.name]}>'

class IE_Education(IEngine):
    """ Inference Engine for Education """

    def __init__(self, name, questions, confirmations, properties, objType=Degree, quota=1):
        super().__init__(name, questions, confirmations, properties, objType, quota)

ieducation = IE_Education(
    name = 'education',
    questions = questions, 
    confirmations = confirmations,
    properties = properties,
    objType=Degree,
    quota=2
)
# ieducation.ask(confirmation = True) # 