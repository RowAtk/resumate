from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation

# import prompter
from resumate.iengines.prompter import prompter
# Make Question Queue
# Question Queue - LIFO queue designed to accept questions to send to the prompter
# This queue could take a question and a argument to specify what property the question comes from
# OR we can add this value to the question obj
# OR
# Property Queue
# This could be a queue (same as question queue) but for the properties in order to associate properties to questions


# Engine provides a question
# then added to the queue

# res = prompter.prompt(questionQ.pop())

# doc = nlp(res)

# Education
# Question

# queue item = 3-tuple (q, engine, object)
# target = (enginename, obj_index)
question_queue = []

engines = [ieducation]
results = {} # prof_obj

def run():
    # prompter.meeting()
    for engine in engines:
        while not engine.finished:
            # store object decides how to ask question really
            question, target = engine.ask()
            # question_queue.append((question, target))
            # res = prompter.prompt(question_queue.pop()[0])
            res = prompter.prompt(question)

            # analyze
            doc = nlp(res)
            analyze(doc, target)
            # engine.satisfiable()

    debug(results, pretty=True)

def analyze(doc, target):
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



    