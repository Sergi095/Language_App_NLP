from utils import get_text_from_audio, load_model
import speech_recognition as sr
import sys
import os
import numpy as np
import tensorflow as tf
from keras.models import load_model
import pickle
from typing import List
from utils import get_text_from_audio, load_model, decode_sequence
sys.path.append('../Neural_Machine_Translator')
from get_model import *
from preprocess import *




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


def do_translation(input_sentence: List[str],
                    input_language: str,
                    raw_data_path: str = '../Neural_Machine_Translator/raw_data/spa.txt',
                    path: str = '../Neural_Machine_Translator/data/') -> str:

    
    dataset, train, test = build_data_set(raw_data_path, path)
    # prepare english tokenizer
    eng_tokenizer = create_tokenizer(dataset[:, 0])
    eng_vocab_size = len(eng_tokenizer.word_index) + 1
    eng_length = get_max_length(dataset[:, 0])


    spa_tokenizer = create_tokenizer(dataset[:, 1])
    spa_vocab_size = len(spa_tokenizer.word_index) + 1
    spa_length = get_max_length(dataset[:, 1])

    # spanish to english
    if input_language == 'Spanish':
        model_path = '../Neural_Machine_Translator/saved_model/model.h5'
        model = load_model(model_path)
        input_sentence_encoded = encode_sequences(spa_tokenizer, spa_length, input_sentence)   
        translation = predict_sequence(model, eng_tokenizer, input_sentence_encoded)
        return translation
    # english to spanish
    elif input_language == 'English':
        model_path = '../Neural_Machine_Translator/saved_model_en_es/model_en_es.h5'
        model = load_model(model_path)
        input_sentence_encoded = encode_sequences(eng_tokenizer, eng_length, input_sentence)   
        translation = predict_sequence(model, spa_tokenizer, input_sentence_encoded)
        return translation
    else:
        raise ValueError('input_language must be either Spanish or English')
        exit(1)


if __name__ == "__main__":
    # main()

    print('running')
    input_sentence = ['she bit him']
    input_language = 'English'
    translation = do_translation2(input_sentence, input_language)
    print(f'this is the translation: {translation}')