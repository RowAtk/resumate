from resumate.iengines.core import IEngine, IObject
from resumate.iengines.project.dateFinder import dateProjProp
from resumate.iengines.utils import *

properties = [
    dateProjProp
]

questions = [
    "Tell me about a project you've worked on",
    "Okay I'd love to hear about any projects you've worked on. Tell me about one"
]

mquestions = [

]

confirmations = [
    "Alright great work on that project. Are there any others you want me to know",
    "Excellent stuff. Would you like to tell me about another project?"
]


# Make Project class - store all data and the logic to assess it
class Project(IObject):
    """ Class to represent information stored on a project """

    def __init__(self, properties):
        super().__init__(properties)        

    def isAcceptable(self):
        """ Does object meet minimum criteria """
        needed = ['title', 'source'] # @rowan to help tweak this
        for need in needed:
            if not self.properties[need]:
                return False
        return True

    def default_candidates(self):
        return [self.properties['title']] if self.properties['title'] else []

    def __repr__(self):
        return f'<Degree title={self.properties[titleProp.name]}, source={self.properties[sourceProp.name]}, date={self.properties[dateProp.name]}>'

class IE_Project(IEngine):
    """ Inference Engine for Projects """

    def __init__(self, name, questions, confirmations, properties, objType=Degree, quota=1):
        super().__init__(name, questions, confirmations, properties, objType, quota)

iproject = IE_Projects(
    name = 'project',
    questions = questions, 
    confirmations = confirmations,
    properties = properties,
    objType=Project,
    quota=1
)
# ieducation.ask(confirmation = True) # 