from resumate import nlp

from pprint import pprint
from resumate.iengines.utils import *
from resumate.iengines.core import Pipe, IProperty

"""
The Skills Finder will work using keyword matching for the following areas: (w examples)
# Programming Languages: Python, Java  
# Web Technologies & Frameworks: Angular 4, HTML5, CSS3.0, Kendo UI, PHP
# Scripts/UI: JavaScript, OOJS, JQuery, AJAX, BootStrap
# Database and ORM: MySQL
# Design Tools: Figma, Photoshop + Dream Weave
# Versioning and other tools: Git, Bitbucket, Jira
"""

# Sample Texts
text = ["I know Python and Javascript. I've used Django, with MySQL as the database tool.",
        "I'm a designer. I like Figma and Photoshop.",
        "When I'm programming, I use Git and Bitbucket for version control."
]

skillsDict = {
    "Prog Lang": ["Python", "Java", "PHP", "Ruby", "C", "C++", "Go"],
    "Web Tech & Framework": ["Angular 4, HTML5, CSS3.0, Kendo UI, Laravel", "Flask", "Django", "Spring Boot"],
    "Scripts": ["JavaScript", "OOJS", "JQuery", "AJAX", "BootStrap"],
    "DB Tools": ["MySQL", "PostgreSQL", "SQLite"],
    "Design": ["Figma", "Photoshop", "Dream Weave", "Bootstrap Studio"],
    "Version": ["Git", "Bitbucket", "Jira"]
}

# Idea: if person tells you a framework
frame_Lang_Pair = {
    ("Flask", "Django"): "Python",
    ("Laravel"): "PHP",
    ("Ruby on Rails"): "Ruby",
    ("Spring Boot"): "Java"
}

def progLangFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any programming languages in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="Prog Lang")

def webTechFrameworkFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any framework in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="Web Tech & Framework")
    
def scriptFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any Scripts in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="Scripts")

def dbFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any DB in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="DB Tools")

def designFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any Design Tools in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="Design")

def versCtrlFinder(doc=None, txt=''):
    """Takes a doc object (or string) and finds any Version Control Tools in the string. Returns a list of strings"""
    if not doc:
        doc = nlp(txt)
    
    return skillFinder(doc, srch="Version")


# General Skill Finder Script
def skillFinder(doc=None, srch=""):
    """Takes a doc object, and a search key and attempts to interpret skills implied in the string. Returns a list, or 
    None if no skill found"""
    if not doc:
        doc = nlp(text)

    res = []
    keywords = skillsDict[srch] if srch else skillsDict.values()
    debug(f'KEYWORDS: {keywords}')
    for token in doc:
        for val in keywords:
            if val.lower() == token.text.lower():
                res.append(val)
    
    debug(f'Skill Result: {res}')
    if res:
        return res
    return None

# Properties
progLangProp = IProperty(
    name='programming language',
    pipes=[
        Pipe(progLangFinder, name='progLangFinder')
    ],
    questions=[
        'what programming languages do you know'
    ],
    followups=[
        ''
    ]
)

webTechFrameworkProp = IProperty(
    name='web tech framework',
    pipes=[
        Pipe(webTechFrameworkFinder, name='webTechFrameworkFinder')
    ],
    questions=[
        'what web technologies and frameworks do you know'
    ],
    followups=[
        ''
    ]
)

scriptProp = IProperty(
    name='script',
    pipes=[
        Pipe(scriptFinder, name='scriptFinder')
    ],
    questions=[
        'what web scripts (eg Javascript, jQuery) do you know'
    ],
    followups=[
        ''
    ]
)

dbProp = IProperty(
    name='database and ORM',
    pipes=[
        Pipe(dbFinder, name='dbFinder')
    ],
    questions=[
        'what Database and ORM tools do you know'
    ],
    followups=[
        ''
    ]
)

designProp = IProperty(
    name='design',
    pipes=[
        Pipe(designFinder, name='designFinder')
    ],
    questions=[
        'what design tools do you know'
    ],
    followups=[
        ''
    ]
)

versCtrlProp = IProperty(
    name='version control',
    pipes=[
        Pipe(versCtrlFinder, name='versCtrlFinder')
    ],
    questions=[
        'what Version Control software do you know'
    ],
    followups=[
        ''
    ]
)
