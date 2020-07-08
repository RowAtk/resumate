from resumate.iengines.core import IEngine, IObject
from resumate.iengines.project.dateFinder_proj import dateProjProp
from resumate.iengines.project.role_titleFinder import projTitleProp, roleProp
from resumate.iengines.project.desc_achieveFinder import descProp, achieveProp
from resumate.iengines.utils import *
from resumate import nlp

properties = [
    projTitleProp,
    dateProjProp,
    descProp,
    roleProp,
    achieveProp,    
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
        needed = ['proj title', 'description'] # @rowan to help tweak this
        needed = list(self.properties.keys())
        for need in needed:
            if not self.properties[need]:
                return False
        return True

    def merge(self, obj):
        if self.isSame(obj):
            for prop, val in self.properties.items():
                if not val:
                    print("IN LOOOOOOOOOOOOOOooP")
                    self.properties[prop] = obj.properties[prop]
                    break
        else:
            raise Exception("Two Objects are of different types! Can't Megre!")

    def default_candidates(self):
        return [self.properties['proj title']] if self.properties['proj title'] else []

    def __repr__(self):
        title = self.properties['proj title']
        desc = self.properties['description']
        role = self.properties['role']
        achieve = self.properties['achieve']
        date = self.properties['date proj']
        return f'<Project title={title}\ndescription={desc}\nrole={role}\nachievements={achieve}\ndate={date}>'

class IE_Project(IEngine):
    """ Inference Engine for Projects """

    def __init__(self, name, questions, confirmations, properties, objType, quota=1):
        super().__init__(name, questions, confirmations, properties, objType, quota)
        print(self.makeObjects(self.analyze(nlp('the'))))
        self.iobjects += self.makeObjects(self.analyze(nlp('the')))

    def ask(self):
        """ get general question to ask - projects only ask followups """
        prop = self.properties[0]
        return prop.ask([]), [self.name, -1]

    def analyze(self, doc):
        return super().analyze(doc)
    

ieproject = IE_Project(
    name = 'project',
    questions = questions, 
    confirmations = confirmations,
    properties = properties,
    objType=Project,
    quota=1
)
# ieducation.ask(confirmation = True) # 