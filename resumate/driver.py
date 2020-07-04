from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation

# import prompter
from resumate.iengines.prompter import prompter

# target = (enginename, obj_index)

engines = [ieducation]

def run():
    # prompter.meeting()
    for engine in engines:
        while not engine.finished:
            # store object decides how to ask question really
            question, target = engine.ask()
            res = prompter.prompt(question)
            
            # analyze
            analyze(res, engine, target)
        debug(engine.degrees, pretty=True)

def analyze(res, engine, target):
    """ relevant engines analyze response """
    doc = nlp(res)
    question, target = engine.makeInferences(doc, target)
    if question and target:
        res = prompter.prompt(question)
        analyze(res, engine, target) 


def analyze2(doc, target):
    results = []
    for engine in engines:
        followup, target = engine.makeInferences(doc, target)
        if followup:
            res = prompter.prompt(followup)
            # analyze
            doc = nlp(res)
            analyze(doc, target)

        # merge(data)
    return results     


def merge(data):
    for key, val in data.items():
        if key in results:
            results[key].append(val)
        else:
            results[key] = [val]



    