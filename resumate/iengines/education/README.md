#Resumate

## Objective  
Resumate, a Dialog-to-Resume Generator (dtrg), is designed to facilitate
human-like converstion between a human and the system. Based on the responses from the
user, the system learns new facts about the user and stores it to eventually be turned into
a resume for the user.

Our resume will be focused for a web developer position and will have the following main sections:  
1. Resume Objective
2. Name & Contact Info: this will be typed in by the user rather than collected via conversation
3. Skills
4. Education (The focus of this module)
5. Projects

Under the Education section of the resume, these are the areas of interest:
* Schooling:
	* Source/University
	* Degree Type eg. Bachelors, Masters
	* Field eg. Computer Science
* Special Certifications earned by the user
* When these certifications were earned

![Expert System](https://miro.medium.com/max/2694/1*7KOUq-ORxgMnkZxeOC8SYQ.jpeg "Expert System Module")

Starter Questions:
* Do you have any academic degrees/What academic degrees have you attained?
    * In what field?
    * When did you get your {degree}?\ What year did you get the degree?
    * What type of Degree\To confirm: was the degree a BSc.
    * Where? At which institution?
* Have you gotten any notable certifications or awards you’re proud of?

## Useful Links
Types of Degrees: <https://study.com/different_degrees.html>

## Development Timeline
### April 6, 2020:  
* Module created; README drafted.

### April 18, 2020:
* Main classes outlined
    * 

----

# Resumate Experiments with Spacy

## Title Finder - Basic
Designed to extract title from sentences in the form '...{Degree Type} in {Subject}...' using simple keyword matching