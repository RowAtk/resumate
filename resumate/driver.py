from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines
from resumate.iengines.education.ie_eduction import ieducation
from resumate.iengines.skill.ie_skill import ieskills
from resumate.iengines.project.ie_project import ieproject 
from resumate.docgen import createDoc

# import prompter
from resumate.iengines.prompter import prompter

# import docgen

# target = (enginename, obj_index)

engines = [ieducation, ieskills, ieproject]  # list all engines in order to be executed
globalengines = [engine for engine in engines if engine.isGlobal]

def run():
    # prompter.meeting()
    for mainengine in engines:
        while not mainengine.finished:
            # store object decides how to ask question really
            question, target = mainengine.ask()
            res = prompter.prompt(question)

            # analyze
            analyze(res, mainengine, target)
        debug(mainengine.iobjects, pretty=True)
    
    user = prompter.user
    if user.exists():
        pre = user.firstname
    else:
        pre = ""
    createDoc(f"gendocs\{pre}TestRes.docx", user = user)


def analyze(res, mainengine, target):
    """ relevant engines analyze response """
    doc = nlp(res)
    # question, target = engine.makeInferences(doc, target, prompter)
    for engine in globalengines + [mainengine]:
        engine.makeInferences(doc, target)
        debug(engine.iobjects, pretty=True)
    
    question, target = mainengine.evaluate(prompter)
    if question and target:
        res = prompter.prompt(question)
        analyze(res, mainengine, target)    

"""
Fill out education quick
I have a Bachelors in Economics and a Masters in Social Science. I got one in 2018 and I got the other in 2019. I got one from UWI and the other from UWI

Some Skillz
I know Django, Flask, PHP, Javascript, HTML5, MySQL, and Git
"""
