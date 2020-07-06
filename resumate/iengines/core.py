import random
from textblob import TextBlob
from resumate.iengines.utils import *

class Pipe():
    def __init__(self, func, name=None):
        self.func = func
        self.name = name

    def run(self, doc):
        output = self.func(doc)
        if output:
            debug(f'Output: {output} Found by: {self.name}')
        return output

class Keywords():

    def __init__(self, *args):
        self.keywords = [Keyword(arg) for arg in args]
    
    def __contains__(self, token):
        for keyword in self.keywords:
            if keyword == token:
                return True
        return False

class Keyword():

    def __init__(self, text, pos=None, tag=None, dep=None, head=None, root=None, match_case=True):
        self.text = text
        self.pos = pos
        self.tag = tag
        self.dep = dep
        self.head = head
        self.root = root
        self.match_case = match_case

    def __eq__(self, token):
        match = (self.text == token.text if self.match_case else self.text.lower() == token.text.lower()) and \
        (self.pos == token.pos_ if self.pos else True) and \
        (self.tag == token.tag_ if self.tag else True) and \
        (self.dep == token.dep_ if self.dep else True) and \
        (self.head == token.head.text if self.head else True)
        if match: debug(f"{token.text} matches with {self.text}")
        return match

class Question():
    """ 
    class representing a question. Types include:
    q = question
    f = follow-up Question
    """
    def __init__(self, text, type='q'):
        self.text = text
        self.type = type

class QuestionPool():
    """ class representing a pool or group of questions for an engine to send to the prompter """
    MARKER = '#'
    CMARKER = '!'
    def __init__(self, questions, followups):
        self.questions = self.consumeQuestions(questions)
        self.followups = self.consumeQuestions(followups)
        self.last = None
    
    def getQuestion(self, candidates, questions=None):
        if not questions: questions = self.questions
        debug(questions)
        if questions:
            chooseCount = 0
            q = random.choice(questions[len(candidates)])
            while q == questions['last'] and chooseCount < 3:
                q = random.choice(questions[len(candidates)])
                chooseCount += 1
            questions['last'] = q
            for i in range(len(candidates)):
                candidates = [str(candidate) for candidate in candidates]
                q = q.replace(QuestionPool.MARKER, candidates[i], 1)
            
            return Question(q)
        raise Exception("Error! unable to get question. no questions provided")

    def getFollowup(self, candidates):
        return self.getQuestion(candidates, questions=self.followups)

    def consumeQuestions(self, questions):
        questionDict = {}
        for question in questions:  
            varCount = question.split().count(QuestionPool.MARKER)
            if varCount in questionDict:
                questionDict[varCount].append(question)
            else:
                questionDict[varCount] = [question]
        questionDict['last'] = None       
        debug(questionDict)
        return questionDict

    def __repr__(self):
        return f'QuestionPool for {self.property}'
        

class IProperty():
    """ Base class for properties in an inference Engine """

    def __init__(self, name, pipes=[], questions=[], followups=[]):
        self.name = name
        self.pipes = pipes
        self.questionPool = QuestionPool(questions, followups) if questions else None

    def set_doc(self, doc):
        """ set input (spacy doc object) to be analyzed """
        self.doc = doc

    def set_pipes(self, pipes):
        """ set pipes to analyze doc """
        self.pipes = pipes

    def set_questionPool(self, questions, followups=[]):
        """ set question pool """
        self.questionPool = QuestionPool(questions, followups)

    def ask(self, candidates):
        """ return question to ask user """
        if self.questionPool:
            return self.questionPool.getQuestion(candidates)
        raise Exception("Error! No questionpool provided!")

    def followup(self, candidates):
        """ return follow-up question to ask user """
        if self.questionPool:
            return self.questionPool.getFollowup(candidates)
        raise Exception("Error! No questionpool provided!")

    def analyze(self, doc):
        if doc and self.pipes:
            for pipe in self.pipes:
                output = pipe.run(doc)
                if output:
                    # if len(output) > 1, here is where you would ask a follow-up question for clarification
                    self.value = output
                    return output
            debug(f"HEY! {self.name} IProperty unable to produce truthy result!")
            return []
        raise Exception("Error! doc object provided is null") if not doc else Exception("Error! no pipeline provided input given")

    def __repr__(self):
        return f'<IPropertyEngine name={self.name}>'
     

class IEngine():
    """ Base class for Inference Engines """

    def __init__(self, name, questions, confirmations, properties, objType, quota):
        self.name = name # unique identifier for an Inference engine
        self.properties = properties # inference propert engines to analyze and ask questions
        self.questionPool = QuestionPool(questions, confirmations) if questions else None
        self.OBJTYPE = objType # IObject class to instantiate new iobjects
        self.quota = quota # acceptable object quota
        self.finished = False # do we stop asking questions from this IEngine
        self.iobjects = [] # actual information colected from analysis

    def analyze(self, doc):
        """ analyse doc response using properties """
        results = {}
        for prop in self.properties:
            # debug(prop.analyze(doc))
            results[prop.name] = prop.analyze(doc)
        # debug(results)
        return results

    def ask(self):
        """ get general question to ask """
        return self.questionPool.getQuestion([]), None

    def confirm(self, prompter):
        """ Take over prompter and ask a confirmation question """
        unsure = True
        while unsure and not self.finished:
            confirmation = self.questionPool.getFollowup([])
            res = TextBlob(prompter.prompt(confirmation))
            debug(f'Response polarity: {res.polarity}')
            debug(res.raw)
            # Neg - means user does not want to continue talking with this engine
            if res.sentiment.polarity == 0:
                if 'no' in res.raw.lower(): # negative response
                    debug("NO DETECTED") 
                    self.finished = True
                elif 'yes' in res.raw.lower():
                    debug("YES DETECTED") 
                    unsure = False
            elif res.polarity <= 0: # negative response 
                self.finished = True 

    def isAcceptable(self):
        """ has the quota for acceptable onjects been met """
        completeCount = 0
        for obj in self.iobjects:
            debug(obj)
            if obj.isAcceptable():
                completeCount += 1
        debug(completeCount)
        return completeCount >= self.quota

    def findProperty(self, name):
        """ find inference property engine by name """
        for prop in self.properties:
            if name == prop.name:
                return prop
        return None

    def makeInferences(self, doc, target, prompter):
        """ make inferences from a doc object and self evaluate based on information collected thus far """
        # debug(f'ACCEPTED target: {target}')
        results = self.analyze(doc)
        iobjs = self.makeObjects(results)
        if iobjs and target and target[0] == self.name:
            # this engine is target
            target_data = iobjs.pop(0)
            self.iobjects[target[1]].merge(target_data)
        else:
            self.iobjects += iobjs
        followup, target = self.evaluate(prompter)
        return followup, target

    def makeObjects(self, results):  
        """ Make IObjects from analysis results """    
        maxLen = max([len(val) for val in results.values()])
        newResults ={key : val + [None] * (maxLen - len(val)) for key, val in results.items()}
        iobjs = []
        for i in range(maxLen):
            # make obect
            obj = {}
            for key in newResults:
                obj[key] = newResults[key][i]
            iobj = self.OBJTYPE(obj)
            iobjs.append(iobj)
        return iobjs

    def evaluate(self, prompter):
        """ Evaluate info collected and ask followups if missing data exists """
        if self.isAcceptable():
            self.confirm(prompter)
        
        if not self.finished:
            debug("Searching for followups")
            # look for missing data
            for i, obj in enumerate(self.iobjects):
                missing = obj.missingValues()
                existing = obj.existingValues()
                debug(f"Missing props: {missing}")
                for prop in missing:
                    iprop = self.findProperty(prop)
                    debug(iprop)
                    candidates = [existing[0]] if existing else []
                    debug(candidates)
                    followup = iprop.ask(candidates=candidates)
                    target = (self.name, i)
                    # debug(f'target_index: {target}')
                    return followup, target
        return None, None


class IObject():
    """ Class to represent information stored of an IE """

    def __init__(self, properties):
        self.properties = properties
        self.qcount = 1

    def isAcceptable(self):
        """ Does object meet minimum criteria """
        raise Exception("Error! Unimplemented method")

    def merge(self, obj):
        """ merge two storage objects together """
        if self.isSame(obj):
            for prop, val in self.properties.items():
                if not val:
                    self.properties[prop] = obj.properties[prop]
        else:
            raise Exception("Two Objects are of different types! Can't Megre!")

    def isSame(self, obj):
        """ are two objects the same class """
        return type(self) == type(obj)

    def isComplete(self):
        """ Does object have all values satisfied """
        for val in self.properties.values():
            if not val:
                return False
        return True

    def exhausted(self):
        if self.qcount > 3:
            return True
        return False 
    
    def missingValues(self):
        """ return names of missing properties """
        missing = []
        if not self.exhausted():
            for prop, val in self.properties.items(): 
                if not val:
                    missing.append(prop)
        if missing: self.qcount += 1
        return missing

    def existingValues(self):
        """ return actual existing values """
        exisitng = []
        for prop, val in self.properties.items(): 
            if val:
                exisitng.append(val)
        return exisitng

"""
#########
# Title #
#########

Question Pool
--------------------
1) what academic degrees have you attained
2) what degrees do you have
3) what degrees are you proud of

Follow-Ups
----------
Clarification - when engine is unsure
1) is ___ the name of your degree?
2*) is ___ or ___ the name of your degree?
3) 
"""

"""
Ask question

Engines submit follow ups

Need Question Queue
"""