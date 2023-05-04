'''
English-to-Spanish translation with a sequence-to-sequence Transformer
'''

import pathlib
import random
import string
import re
import pickle
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import TextVectorization


def get_file()-> pathlib.Path:
    text_file = keras.utils.get_file(
        fname="spa-eng.zip",
        origin="http://storage.googleapis.com/download.tensorflow.org/data/spa-eng.zip",
        extract=True,
    )
    text_file = pathlib.Path(text_file).parent / "spa-eng" / "spa.txt"
    return text_file


def parsing(text_file: str, encoding: str = "utf-8")-> list:

    with open(text_file, mode='r', encoding=encoding) as f:
        lines = f.read().split("\n")[:-1]
    text_pairs = []
    for line in lines:
        eng, spa = line.split("\t")
        spa = "[start] " + spa + " [end]"
        text_pairs.append((eng, spa))
    return text_pairs


def split_data(text_pairs: list,
            train_ratio: float = 0.7,
            val_ratio: float = 0.15,
            test_ratio: float = 0.15)-> tuple:
    
    random.shuffle(text_pairs)
    num_val_samples = int(val_ratio * len(text_pairs))
    num_train_samples = len(text_pairs) - 2 * num_val_samples
    train_pairs = text_pairs[:num_train_samples]
    val_pairs = text_pairs[num_train_samples : num_train_samples + num_val_samples]
    test_pairs = text_pairs[num_train_samples + num_val_samples :]
    return train_pairs, val_pairs, test_pairs


def format_dataset(eng,
                  spa):

    eng = eng_vec(eng)
    spa = spa_vec(spa)
    return ({"encoder_inputs": eng, "decoder_inputs": spa[:, :-1],}, spa[:, 1:])


def make_dataset(pairs: tuple,
                eng_vectorization: TextVectorization, 
                spa_vectorization: TextVectorization, 
                batch_size: int = 64)-> tf.data.Dataset:

    global eng_vec, spa_vec

    eng_vec, spa_vec = eng_vectorization, spa_vectorization

    eng_texts, spa_texts = zip(*pairs)
    eng_texts = list(eng_texts)
    spa_texts = list(spa_texts)
    dataset = tf.data.Dataset.from_tensor_slices((eng_texts, spa_texts))
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(format_dataset)
    return dataset.shuffle(2048).prefetch(16).cache()

def custom_standardization(input_string: str)-> str:
    lowercase = tf.strings.lower(input_string)
    strip_chars = string.punctuation + "¿"
    strip_chars = strip_chars.replace("[", "")
    strip_chars = strip_chars.replace("]", "")
    return tf.strings.regex_replace(lowercase, "[%s]" % re.escape(strip_chars), "")

def encode_eng_text(train_pairs: tuple,
                    path: str = None)-> TextVectorization:

    vocab_size = 15000
    sequence_length = 20

    train_eng_texts = [pair[0] for pair in train_pairs]
    train_spa_texts = [pair[1] for pair in train_pairs]

    eng_vectorization = TextVectorization(
        max_tokens=vocab_size,
        output_mode="int",
        output_sequence_length=sequence_length,
    )

    spa_vectorization = TextVectorization(
        max_tokens=vocab_size,
        output_mode="int",
        output_sequence_length=sequence_length + 1,
        standardize=custom_standardization,
    )

    
    eng_vectorization.adapt(train_eng_texts)
    spa_vectorization.adapt(train_spa_texts)

    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        # saving with pickle
        with open(os.path.join(path, "eng_vectorization.pkl"), "wb") as f:
            pickle.dump(eng_vectorization.get_config(), f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(path, "train_eng_texts.pkl"), "wb") as f:
            pickle.dump(train_eng_texts, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open(os.path.join(path, "spa_vectorization.pkl"), "wb") as f:
            pickle.dump(spa_vectorization.get_config(), f, protocol=pickle.HIGHEST_PROTOCOL)

        with open(os.path.join(path, "train_spa_texts.pkl"), "wb") as f:
            pickle.dump(train_spa_texts, f, protocol=pickle.HIGHEST_PROTOCOL)

    



    return eng_vectorization, spa_vectorization





if __name__ == "__main__":
    text_file = get_file()
    text_pairs = parsing(text_file)
    for _ in range(5):
        print(random.choice(text_pairs))
    
    train_pairs, val_pairs, test_pairs = split_data(text_pairs)
    
    print(f"{len(text_pairs)} total pairs")
    print(f"{len(train_pairs)} training pairs")
    print(f"{len(val_pairs)} validation pairs")
    print(f"{len(test_pairs)} test pairs")

    eng_vectorization, spa_vectorization = encode_eng_text(train_pairs, path="vectorization")


    train_ds = make_dataset(train_pairs, eng_vectorization, spa_vectorization)
    val_ds = make_dataset(val_pairs, eng_vectorization, spa_vectorization)


    for inputs, targets in train_ds.take(1):
        print(f'inputs["encoder_inputs"].shape: {inputs["encoder_inputs"].shape}')
        print(f'inputs["decoder_inputs"].shape: {inputs["decoder_inputs"].shape}')
        print(f"targets.shape: {targets.shape}")