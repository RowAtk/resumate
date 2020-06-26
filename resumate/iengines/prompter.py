import random
from time import sleep
from resumate.user import User
from resumate.iengines.core import Question
from resumate.iengines.utils import *
from colorama import init, Fore, Back, Style

init()


class Prompter():
    """ class to ask the real questions and get the real responses! """

    ABORTCUES = ['exit', 'bye', 'abort', 'go away']

    def __init__(self, user=None, interesting=True):
        """ init prompter """
        self.user = user if user else User(firstname='', lastname='', title='', gender='')
        self.interesting = interesting
        self.setup()
        self.speaker = None

    def prompt(self, question):
        """ ask question then collect and return response """
        # ask question
        self.talk(self.makePrompt(question))

        # listen to answer
        response = self.listen()
        return response

    def greeting(self):
        """ send user greetings! """
        self.talk("Hello! I am resumate! I want to get to know you.")

    def talk(self, text):
        """ makes the prompter talk """
        if self.speaker == 'user' or not self.speaker: # set speaker name
            print(f'{Fore.RED}Resumate: {Style.RESET_ALL}')
            self.speaker = 'prompter'

        for letter in text:
            print(letter, end="", flush=True)
            sleep(0.05)
        print()

    def listen(self):
        """ hear what the user has to say """
        name = 'You' # other logic to inlcude maybe the user's name can be placed here
        print()
        self.speaker = 'user'
        res = input(f'{Fore.RED}{name}: {Style.RESET_ALL}')
        print()
        for cue in Prompter.ABORTCUES:
            if cue == res:
                self.salutation()
        return res

    def salutation(self):
        """ Tell em goodbye! """
        name = self.user.fullname if self.user.fullname else ' '
        self.talk(f"It was a pleasure speaking with you. Goodbye{name}.")
        exit(0)

    def setup(self):
        """ setup the prompter. display a cool header """
        pad = "\t" * 2
        header = f"""
        {pad}******************************\n
        {pad}**** RESUMATE ~ Interview ****\n
        {pad}******************************\n
        """
        print(header)

    def meeting(self):
        """ gather user details """
        self.greeting() # greeting first!
        if not self.user.exists():
            # gather details here
            firstname = self.prompt("what is your firstname")
            lastname = self.prompt("what is your lastname")
            title = self.prompt("are you Mr/Ms/Mrs/Dr.. etc")
            gender = self.prompt("are u a male or female")
        self.user = User(
            firstname=firstname,
            lastname=lastname,
            title=title,
            gender=gender
        )
        debug(self.user)
        self.talk("Ok. I feel like I know you 10% more now!")

    def makePrompt(self, question):
        """ add your own spin to the boring IE question """
        qstarts = [
            
        ]

        fstarts = [

        ]

        starter = ''
        ending = ''
        if type(question) == str:
            question = Question(question)
        if self.interesting:
            if question.type == 'q' and qstarts:
                starter = random.choice(qstarts) + ' '
            elif question.type == 'f' and fstarts:
                starter = random.choice(fstarts) + ' '
        
        prompt = starter + question.text + ending + '?'
        return prompt[0].upper() + prompt[1:]


p = Prompter()
p.meeting()