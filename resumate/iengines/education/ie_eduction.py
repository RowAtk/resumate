# Make IEngine with IProperties
from resumate.iengines.core import IEngine, Storage
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
    "what academic degrees have you attained"
]

confirmations = [
    "are there any other degrees you would like to mention",
    "any other degrees"
]

# Make Degree class - store all data and the logic to assess it
class Degree(Storage):
    """ Class to represent information stored on a degree """

    def __init__(self, title=None, source=None, date=None):
        # stored as a list: 0 -> key 1 -> value
        self.title = ['title', title]
        self.source = ['source', source]
        self.date = ['date', date]
        self.qcount = 1
        # values = {} 

    def findTarget(self):
        pass

    def exhausted(self):
        if self.qcount > 3:
            return True
        return False

    def merge(self, obj):
        if self.isSame(obj):
            if self.title[1] == None:
                self.title[1] = obj.title[1]
                obj.title = None
            
            if self.source[1] == None:
                self.source[1] = obj.source[1]
                obj.source = None

            if self.date[1] == None:
                self.date[1] = obj.date[1]
                obj.date = None
            return obj
        raise Exception("Two Objects are of different types! Can't Megre!")

    def missingValues(self):
        missing = []
        existing = []
        if self.title[1] == None:
            missing.append(self.title[0])

        if self.source[1] == None:
            missing.append(self.source[0])

        if self.date[1] == None:
            missing.append(self.date[0])

        if missing: self.qcount += 1
        return missing

    def isAcceptable(self):
        """ Does object meet minimum criteria """
        return self.title[1] != None and self.source[1] != None

    def isComplete(self):
        """ Does object have all values satisfied """
        return self.title[1] != None and self.source[1] != None and self.date[1] != None

    def __repr__(self):
        return f'<Degree title={self.title}, source={self.source}, date={self.date}>'

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

    def analyze(self, doc):
        """ analyse doc response using properties """
        results = {}
        for prop in self.properties:
            # debug(prop.analyze(doc))
            results[prop.name] = prop.analyze(doc)
        # debug(results)
        return results

    def makeInferences(self, doc, target):
        # debug(f'ACCEPTED target: {target}')
        results = self.analyze(doc)
        degrees = self.makeObjects(results)
        if degrees and target and target[0] == self.name:
            # this engine is target
            target_data = degrees.pop(0)
            self.degrees[target[1]].merge(target_data)
        else:
            self.degrees += degrees
        followup, target = self.evaluate()
        return followup, target

    def evaluate(self):
        target = None
        followup = None
        completeCount = 0
        for degree in self.degrees:
            debug(degree)
            if degree.isAcceptable():
                completeCount += 1
        debug(completeCount)

        if completeCount >= 1:
            self.satisfiable()
        
        if not self.finished:
            debug("Searching for followups")
            # look for missing data
            for i, degree in enumerate(self.degrees):
                missing = degree.missingValues()
                debug(f"Missing props: {missing}")
                for prop in missing:
                    iprop = self.findProperty(prop)
                    followup = iprop.ask(candidates=[degree.title])
                    target = (self.name, i)
                    # debug(f'target_index: {target}')
                    return followup, target
        return followup, target
    
    def makeObjects(self, results):
        # I have a degree in CS and a MBA
        # {
            # 'title': ["CS", "MBA"],
            # 'source': [None, None],
            # 'date': [None, None]
        # }
        # when did you get your CS degree?
        # 2015. And I got my other CS degree in 2016 from UWI
        # {
        #     'date': [2015, 2016],
        #     'title': ['Accounts'],
        #     'source': ['UWI']
        # }
        
        maxLen = max([len(val) for val in results.values()])
        newResults ={key : val + [None] * (maxLen - len(val)) for key, val in results.items()}
        degrees = []
        for i in range(maxLen):
            # make obect
            degree = Degree(
                title=newResults['title'][i],
                source=newResults['source'][i],
                date=newResults['date'][i]
            )
            degrees.append(degree)
        return degrees



ieducation = IE_Education(
    name = 'education' ,
    questions = questions, 
    confirmations = confirmations,
    properties = properties
)
# ieducation.ask(confirmation = True) # 