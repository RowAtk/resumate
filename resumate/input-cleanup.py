import spacy, pprint

inputs = [
    "I have a Masters in User Experience Design from Stanford. I also have a BSc. in Software Engineering",
    "Oh No. I got that from UWI.",
    "Around 2015 I think."
]

try1 = "Amazon Web Certificate"
try2 = "Blake got his degree 4 years ago"
q1 = "What are some degrees/certificates you have attained?"


doc = nlp(q1)

# for token in doc:
#     if not token.is_stop and not token.pos_ == "PUNCT":
#         print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_stop, sep="\t\t")

# for chunk in doc.noun_chunks:
#     print(chunk.text, chunk.root.text, chunk.root.dep_,
#             chunk.root.head.text, sep="\t\t")

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)