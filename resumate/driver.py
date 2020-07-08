from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines
from resumate.iengines.education.ie_eduction import ieducation
from resumate.iengines.skill.ie_skill import ieskills
from resumate.iengines.project.ie_project import ieproject 

# import prompter
from resumate.iengines.prompter import prompter

# target = (enginename, obj_index)

engines = [ieproject]  # list all engines in order to be executed
# globalengines = [engine for engine in engines if engine.isGlobal]

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


def analyze(res, mainengine, target):
    """ relevant engines analyze response """
    doc = nlp(res)
    # question, target = engine.makeInferences(doc, target, prompter)
    for engine in engines:
        engine.makeInferences(doc, target)
    
    question, target = mainengine.evaluate(prompter)
    if question and target:
        res = prompter.prompt(question)
        analyze(res, mainengine, target)