# Make IEngine with IProperties
from resumate.iengines.core import IEngine
from resumate.iengines.education.source import sourceProp
from resumate.iengines.education.titleFinder import titleProp
from resumate.iengines.education.dateFinder import dateProp

properties = [
    titleProp,
    sourceProp,
    dateProp
]

questions = [
    "what academic degrees have you attained"
]

confirmations = [
    "are there any other degrees you would like to mention",
    "any other degrees"
]

# Make Degree class - store all data and the logic to assess it

class IE_Education(IEngine):
    """ Inference Engine for Education """

    def __init__(self, name, questions, confirmations, properties):
        super().__init__(name, questions, confirmations, properties) 
        self.finished = False
        self.degrees = []

    def satisfiable(self):
        ans = input("Are you finished?")
        if ans == 'yes':
            self.finished = True   


ieducation = IE_Education(
    name = 'education' ,
    questions = questions, 
    confirmations = confirmations,
    properties = properties
)
# ieducation.ask(confirmation = True) # 


# get 2 titles