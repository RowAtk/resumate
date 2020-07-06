from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation

# import prompter
from resumate.iengines.prompter import prompter

# target = (enginename, obj_index)

engines = [ieducation] # list all engines in order to be executed

def run():
    # prompter.meeting()
    for engine in engines:
        while not engine.finished:
            # store object decides how to ask question really
            question, target = engine.ask()
            res = prompter.prompt(question)
            
            # analyze
            analyze(res, engine, target)
        debug(engine.iobjects, pretty=True)

def analyze(res, engine, target):
    """ relevant engines analyze response """
    doc = nlp(res)
    question, target = engine.makeInferences(doc, target, prompter)
    if question and target:
        res = prompter.prompt(question)
        analyze(res, engine, target)    