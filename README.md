# dialogue-resume
Interview Based Resume Builder - driven by text input

## Virtual Environment

### Install pipenv
>$ pip install pipenv

#### or
>$ pip3 install pipenv

### start virtualenv / shell (from project root)
>$ pipenv shell

### install packages required
>$ pipenv install

### to deactivate
>$ deactivate

#### if this fails try 
>$ exit

## Deep Speech
### Install pre-trained model
Download deepspeech dsmodels folder from shared capstone folder: [here](https://drive.google.com/drive/folders/1Zu-GzAYfaY_jzwTvmgf-2-ujZNR8cT1Y)

Place dsmodels folder in dr/ directory... 
path to models should be: dialoue-resume/dr/dsmodels

### Run deepspeech on sample wav file
>$ deepspeech --model dsmodels/output_graph.pbmm --lm dsmodels/lm.binary --trie dsmodels/trie --audio dr/samples/PATH_TO_WAV_FILE.wav

#### NOTE: !!!!!!!Deepseech samples must be of high quality. Noise in BG severly affects results. Try it for yourself if you wish...!!!!!

## NLTK PLAYGROUND
### python command might be different depending on version and installation. Please use python 3.7 
>$ python3.7 dr/nltk-testing/playground.py

### To run in interactive mode:
>$ python3.7 -i dr/nltk-testing/playground.py
