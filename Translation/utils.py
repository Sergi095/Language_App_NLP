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

sys.path.append('../Neural_Network')
from helpers import custom_standardization
from modules import *



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
    

def load_model(model_path: str) -> keras.Model:
    '''
    unzip model.h5 in file saved_model/
    '''
    custom_layer_objects = {
        "PositionalEmbedding": PositionalEmbedding,
        "TransformerEncoder": TransformerEncoder,
        "TransformerDecoder": TransformerDecoder,
    }

    model = keras.models.load_model(model_path, compile=False, custom_objects=custom_layer_objects)
    return model





def decode_sequence(input_sentence: str,
                    max_decoded_sentence_length: int = 20,
                    transformer: keras.Model = None) -> str:


    # Load the vectorizer
    with open('../Neural_Network/vectorization/eng_vectorization.pkl', 'rb') as handle:
        config = pickle.load(handle)
        eng_vectorization = tf.keras.layers.TextVectorization.from_config(config)
    
    with open('../Neural_Network/vectorization/spa_vectorization.pkl', 'rb') as handle:
        config = pickle.load(handle)
        spa_vectorization = tf.keras.layers.TextVectorization.from_config(config)
    
    with open('../Neural_Network/vectorization/train_eng_texts.pkl', 'rb') as handle:
        eng_texts = pickle.load(handle)
    
    with open('../Neural_Network/vectorization/train_spa_texts.pkl', 'rb') as handle:
        spa_texts = pickle.load(handle)
    
    eng_vectorization.adapt(eng_texts)
    spa_vectorization.adapt(spa_texts)

    spa_vocab = spa_vectorization.get_vocabulary()
    spa_index_lookup = dict(zip(range(len(spa_vocab)), spa_vocab))

    eng_vocab = eng_vectorization.get_vocabulary()
    eng_index_lookup = dict(zip(range(len(eng_vocab)), eng_vocab))

    lang_detect = detect(input_sentence)
    print(lang_detect)
    # if sentence is in english, translate to spanish
    if lang_detect == 'en':
        tokenized_input_sentence = eng_vectorization([input_sentence])
        decoded_sentence = "[start]"
        for i in range(max_decoded_sentence_length):
            tokenized_target_sentence = spa_vectorization([decoded_sentence])[:, :-1]
            predictions = transformer([tokenized_input_sentence, tokenized_target_sentence])

            sampled_token_index = np.argmax(predictions[0, i, :])
            sampled_token = spa_index_lookup[sampled_token_index]
            decoded_sentence += " " + sampled_token

            if sampled_token == "[end]":
                break
        return decoded_sentence
    elif lang_detect == 'es':
        tokenized_input_sentence = spa_vectorization([input_sentence])
        decoded_sentence = "[start]"
        for i in range(max_decoded_sentence_length):
            tokenized_target_sentence = eng_vectorization([decoded_sentence])[:, :-1]
            predictions = transformer([tokenized_input_sentence, tokenized_target_sentence])

            sampled_token_index = np.argmax(predictions[0, i, :])
            sampled_token = eng_index_lookup[sampled_token_index]
            decoded_sentence += " " + sampled_token

            if sampled_token == "[end]":
                break
        return decoded_sentence
    else:
        raise Exception('Language not supported')



if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    count = 5
    while count > 0:
        print(count)
        print(get_text_from_audio(recognizer, microphone))
        count -= 1