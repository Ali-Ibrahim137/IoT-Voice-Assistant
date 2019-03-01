import speech_recognition as sr
import os
#from gtts import gTTS
import requests
import json

r = sr.Recognizer()
audio = sr.AudioFile("output.wav")
with audio as source:
    ali = r.record(source)

t = r.recognize_google(ali)
print(t)
