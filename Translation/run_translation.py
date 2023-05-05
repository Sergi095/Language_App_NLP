from utils import get_text_from_audio, load_model
import speech_recognition as sr
import sys
import os
import numpy as np
import tensorflow as tf
import pickle
from utils import get_text_from_audio, load_model, decode_sequence
sys.path.append('../Neural_Network')
from helpers import custom_standardization






def get_text_mic(t: int = 1) -> str:

    # print('starting main')
    # print('loading model at {model_path}'.format(model_path=model_path))

    # model = load_model(model_path)

    # print(model.summary())
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    text_to_translate = ''

    time = 0
    while time < t:
        # print('you have {t} times to speak'.format(t=t-time))
        # print('you can speak now')
        speech = get_text_from_audio(recognizer, microphone)
        # print(f'you said: {speech}')
        text_to_translate += speech
        time += 1
        break
    
    # print(f'this is the text to translate: {text_to_translate}')

    # max_decoded_sentence_length = 20
    # translation = decode_sequence(text_to_translate, max_decoded_sentence_length, model)
    # print(f'this is the translation: {translation}')

    return text_to_translate


def do_translation(input_sentence: str, model_path: str = '../Neural_Network/saved_model/model.h5') -> str:

    model = load_model(model_path)

    max_decoded_sentence_length = 20
    translation = decode_sequence(input_sentence, max_decoded_sentence_length, model)

    return translation

if __name__ == "__main__":
    # main()

    print('running')