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

questions = [
    "tell me about some of your technical skills",
    "what technical skills do you have"
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
        return True

    def default_candidates(self):
        return []

    def merge(self, obj):
        for prop in self.properties:
            self.properties[prop] += obj.properties[prop]
    
    def __repr__(self):
        lang = self.properties[progLangProp.name]
        frameW = self.properties[webTechFrameworkProp.name]
        scripts = self.properties[scriptProp.name]
        dbms = self.properties[dbProp.name]
        des = self.properties[designProp.name]
        ver = self.properties[versCtrlProp.name]
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