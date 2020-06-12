class PipeLine():

    def __init__(self, doc=None, pipes=[]):
        self.pipes = pipes
        self.doc = doc

    def set_doc(self, doc):
        self.doc = doc
    
    def run(self):
        if self.doc:
            for pipe in self.pipes:
                output = pipe.run(self.doc)
                if output:
                    return output
            print("HEY! PipeLine unable to produce truthy result!")
            return None
        raise Exception("Error! no doc input given")

class Pipe():

    def __init__(self, func, name=None):
        self.func = func
        self.name = name

    def run(self, doc):
        output = self.func(doc)
        if output:
            print(f'Output: {output} Found by: {self.name}')
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
        if match: print(f"{token.text} matches with {self.text}")
        return match

def isNoun(token):
    # print(token.pos_)
    return token.pos_ in ['NOUN', 'PROPN', 'PRON']