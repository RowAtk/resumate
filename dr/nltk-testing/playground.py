import nltk
import os
# import nltk.book as book
from dr.sample import getText

# sunset = open(os.path.join(os.getcwd(), 'dr/nltk-testing/sunset.txt'), 'r').read();
# sunset2 = open('sunset.txt', 'r').read();
# sunset = "Sunset is the time of day when our sky meets the outer space solar winds. " + \
#         "There are blue, pink, and purple swirls, spinning and twisting, like clouds of balloons caught in a whirlwind. " + \
#             "The sun moves slowly to hide behind the line of horizon, while the moon races to take its place in prominence atop the night sky. " + \
#             "People slow to a crawl, entranced, fully forgetting the deeds that must still be done. There is a coolness, a calmness, when the sun does set. " 

def download():
    nltk.download()

def sent_tokenize(text):
    return nltk.sent_tokenize(text)

sunset = getText('sunset')
# print(sunset)
# print("\n\n")
sunset_tokns = sent_tokenize(sunset)
# print(sunset_tokns)

response = "I have a bachelors in computer science that I fought very hard for"
response2 = "I am a certified java developer and an aws solution architect"
response_words = nltk.word_tokenize(response2)

tagged_words = nltk.pos_tag(response_words)

print(tagged_words)

