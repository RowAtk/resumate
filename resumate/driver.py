from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation
from resumate.iengines.skill.ie_skill import ieskills
from resumate.docgen import createDoc

# import prompter
from resumate.iengines.prompter import prompter

# import docgen

# target = (enginename, obj_index)

engines = [ieducation, ieskills] # list all engines in order to be executed

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
    
    createDoc("gendocs\TestRes.docx")

def analyze(res, engine, target):
    """ relevant engines analyze response """
    doc = nlp(res)
    question, target = engine.makeInferences(doc, target, prompter)
    if question and target:
        res = prompter.prompt(question)
        analyze(res, engine, target)    

"""
Fill out education quick
I have a Bachelors of Economics and a Masters of Social Science. I got one in 2018 and I got the other in 2019. I got one from UWI and the 
other from UWI
"""