from resumate import nlp
from resumate.iengines.utils import *

# import and register all IEngines 
from resumate.iengines.education.ie_eduction import ieducation
from resumate.iengines.skill.ie_skill import ieskills
# from resumate.iengines.project.ie_project import iproject - needs fixing

# Doc Generator
from docx import Document


"Takes Knowledge from the Various IE and outputs them to a doc file"

def createDoc(filename, name="Nathaniel Christie"):
    document = Document()
    document.add_heading(f'Resume for {name}', 0)

    # EDUCATION
    document.add_heading('Education', 1)

    degrees = ieducation.iobjects

    for d in degrees:
        nl = "\n"
        # p = document.add_paragraph(str(d))
        document.add_paragraph(f'{d.properties["title"]}{nl}{d.properties["date"]}{nl}{d.properties["source"]}')
        print(str(d))

    # SKILLS
    document.add_heading('Skills', 1)

    skills = ieskills.iobjects[0]
    print(skills)
    for key, vals in skills.properties.items():
        if vals:
            p = document.add_paragraph('', style="List Bullet")
            p.add_run(f'{key.title()}: ').bold = True
            p.add_run(", ".join(vals)).italic = True
    


    # PROJECTS
    document.add_heading('Projects', 1)

    document.save(filename)