import sys
import os
sys.path.append('../Transcription') 
from get_text import recognize_speech_from_mic

import speech_recognition as sr
import tensorflow as tf
from tensorflow import keras
from langdetect import detect

import pickle
from keras.layers import Input
from keras.models import Model




def get_text_from_audio(recognizer: sr.Recognizer(),
                        microphone: sr.Microphone()) -> str:

    transcription = ''
    speech = recognize_speech_from_mic(recognizer, microphone)

    if speech["success"]:
        transcription = speech["transcription"] + ' '
        return transcription
    else:
        transcription = ' '
        return transcription
    







if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    count = 5
    while count > 0:
        print(count)
        print(get_text_from_audio(recognizer, microphone))
        count -= 1