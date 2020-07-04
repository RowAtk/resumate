import random
from resumate.iengines.utils import *

class PipeLine():

    def __init__(self, doc=None, pipes=[]):
        self.pipes = pipes
        self.doc = doc

    def set_doc(self, doc):
        self.doc = doc
    
    def run(self, doc=None):
        if doc:
            for pipe in self.pipes:
                output = pipe.run(doc)
                if output:
                    return output
            debug("HEY! PipeLine unable to produce truthy result!")
            return None
        raise Exception("Error! no doc input given")

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
    """ class representing a question """
    # titleQPool = ('title', [questions], [followups])

    MARKER = '#'
    def __init__(self, questions, followups):
        self.questions = self.consumeFollowups(questions)
        
        self.followups = self.consumeFollowups(followups)
    
    def getQuestion(self, candidates):
        if self.questions:
            q = random.choice(self.questions[len(candidates)])
            # q = self.questions[len(candidates)][0]
            for i in range(len(candidates)):
                candidates = [str(candidate) for candidate in candidates]
                q = q.replace(QuestionPool.MARKER, candidates[i], 1)
            return Question(q)
        raise Exception("Error! unable to get followup question. no followups provided")

    def getFollowup(self, candidates):
        if self.followups:
            q = random.choice(self.followups[len(candidates)])
            for i in range(len(candidates)):
                q = q.replace(QuestionPool.MARKER, candidates[i], 1)
            return Question(q, 'f')
        raise Exception("Error! unable to get followup question. no followups provided")

    def consumeFollowups(self, followups):
        followDict = {}
        for followup in followups:
            varCount = followup.split().count(QuestionPool.MARKER)
            followDict[varCount] = followDict[varCount].append(followup) if varCount in followDict else [followup]
        return followDict

    def __repr__(self):
        return f'QuestionPool for {self.property}'
        

class IProperty():
    """ Base class for properties in an inference Engine """

    def __init__(self, name, doc=None, pipes=[], questions=[], followups=[]):
        self.name = name
        self.value = None # actual value inferred
        self.pipes = pipes
        self.doc = doc
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
        return self.questionPool.getQuestion(candidates)

    def followup(self, candidates):
        """ return follow-up question to ask user """
        return self.questionPool.getFollowup(candidates)

    def analyze(self, doc=None):
        if doc and self.pipes:
            for pipe in self.pipes:
                output = pipe.run(doc)
                if output:
                    # if len(output) > 1, here is where you would ask a follow-up question for clarification
                    self.value = output
                    return output
            debug(f"HEY! {self.name} IProperty unable to produce truthy result!")

            # Here is where the Property may ask another question (a repeat)
            return []
        raise Exception("Error! no doc input given") if not doc else Exception("Error! no pipeline provided input given")
     

class IEngine():
    """ Base class for Inference Engines """

    def __init__(self, name, questions, confirmations, properties):
        self.name = name
        self.properties = properties
        self.questionPool = QuestionPool(questions, []) if questions else None
        self.confirmations = QuestionPool(confirmations, []) if confirmations else None

    def analyze(self, doc):
        """ analyse doc response using properties """
        results = {}
        for prop in self.properties:
            results[prop.name] = prop.analyze(doc)
        return results
        raise Exception("Error! need to implement this method")

    def ask(self, confirmation=False):
        if confirmation:
            return self.confirmations.getQuestion([]), None
        return self.questionPool.getQuestion([]), None

    def findProperty(self, name):
        for prop in self.properties:
            if name == prop.name:
                return prop
        return None

    def isWhole(self):
        """ have i collected all my data """
        raise Exception("Error! need to implement this method")


class Storage():
    """ Class to represent information stored of an IE """

    def isAcceptable(self):
        """ Does object meet minimum criteria """
        raise Exception("Error! Unimplemented method")

    def merge(self, obj):
        """ merge two storage objects together """ 
        raise Exception("Error! Unimplemented method")

    def isSame(self, obj):
        return type(self) == type(obj)

    def isComplete(self):
        """ Does object have all values satisfied """
        raise Exception("Error! Unimplemented method") 


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