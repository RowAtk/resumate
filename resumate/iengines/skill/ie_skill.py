# Make IEngine with IProperties
from resumate.iengines.core import IEngine, IObject
from resumate.iengines.skill.skillFinder \
    import progLangProp, webTechFrameworkProp, scriptProp, dbProp, designProp, versCtrlProp
from resumate.iengines.utils import *

properties = [
    progLangProp,
    webTechFrameworkProp,
    scriptProp,
    dbProp,
    designProp,
    versCtrlProp
]
# eg. Programming Languages, DBMS or ORM technologies used, Deisgn Tools used
questions = [
    "tell me about some of your technical skills (eg. Programming Languages, DBMS or ORM technologies used, Deisgn Tools used)",
    "what technical skills do you have (eg. Programming Languages, DBMS or ORM technologies used, Deisgn Tools used)"
]

mquestions = [
    
]

confirmations = [
    "would you like to continue talking about how skillful you are",
    "keep talking about these skills? If you say no we will move on"
]

class Skills(IObject):
    """ Class representing a user's set of skills collected from an IE """

    def __init__(self, properties):
        super().__init__(properties)
        self.quota = 10

    def isAcceptable(self):
        c = 0
        for key, val in self.properties.items():
            c += len(val)
        return c > 5

    def default_candidates(self):
        return []

    def merge(self, obj):
        for prop in self.properties:
            self.properties[prop] += obj.properties[prop]
    
    def __repr__(self):
        lang = set(self.properties[progLangProp.name])
        frameW = set(self.properties[webTechFrameworkProp.name])
        scripts = set(self.properties[scriptProp.name])
        dbms = set(self.properties[dbProp.name])
        des = set(self.properties[designProp.name])
        ver = set(self.properties[versCtrlProp.name])
        return f'<Skills languages={lang}\nframeworks={frameW}\nscripts={scripts}\ndbms={dbms}\ndesign={des}\nversion={ver}>'


class IE_Skills(IEngine):
    """ Inference Engine for Skills """

    def __init__(self, name, questions, confirmations, properties, objType, quota):
        super().__init__(name, questions, confirmations, properties, objType, quota)

    def makeObjects(self, results):
        obj = Skills(results)
        return [obj]



ieskills = IE_Skills(
    name='skills',
    questions = questions, 
    confirmations = confirmations,
    properties = properties,
    objType=Skills,
    quota=1
)