from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation
from resumate.iengines.skill.ie_skill import ieskills
# from resumate.iengines.project.ie_project import iproject - needs fixing

# Doc Generator
from docx import Document


"Takes Knowledge from the Various IE and outputs them to a doc file"

def createDoc(filename):
    name = "Nathaniel Christie"
    document = Document()
    document.add_heading(f'Resume for {name}', 0)
    document.add_heading('Education', 1)

    degrees = ieducation.iobjects

    for d in degrees:
        nl = "-"
        p = document.add_paragraph(str(d))
        # document.add_paragraph(f'{d.properties["title"]}{nl}{d.properties["date"]}{nl}{d.properties["source"]}')
        print(str(d))

    print("We out here")
    document.add_heading('Skills', 1)

    document.add_heading('Projects', 1)

    document.save(filename)
    print("Up late")