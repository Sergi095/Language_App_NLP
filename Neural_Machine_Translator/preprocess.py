import string
import re
import os
import numpy as np
from pickle import dump
from unicodedata import normalize
from typing import Tuple, List, Union

def read_file(file_path: str) -> str:
    with open(file_path, mode='rt', encoding='utf-8') as f:
        text = f.read()
    return text

def split_sentences(text: str) -> list:
    lines = text.strip().split('\n')
    pairs = [line.split('\t') for line in lines]
    return pairs

def clean_sentences(pairs: list) -> np.array:
    cleaned_pairs = []
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    table = str.maketrans('', '', string.punctuation)
    for pair in pairs:
        cleaned_pair = []
        for sentence in pair:
            sentence = normalize('NFD', sentence).encode('ascii', 'ignore')
            sentence = sentence.decode('UTF-8')
            sentence = sentence.split()
            sentence = [word.lower() for word in sentence]
            sentence = [word.translate(table) for word in sentence]
            sentence = [re_print.sub('', w) for w in sentence]
            sentence = [word for word in sentence if word.isalpha()]
            cleaned_pair.append(' '.join(sentence))
        cleaned_pairs.append(cleaned_pair[:-1])
    return np.array(cleaned_pairs)

def save_cleaned_data(cleaned_sentences: np.array, file_path: str) -> None:
    with open(file_path, 'wb') as f:
        dump(cleaned_sentences, f)
    print('Cleaned sentences saved to: %s' % file_path)

def build_data_set(raw_data_path: str = 'raw_data/spa.txt',
                    path: str = 'data') -> Tuple[np.array, np.array, np.array]:
    text = read_file(raw_data_path)
    pairs = split_sentences(text)
    cleaned_sentences = clean_sentences(pairs)
    if not os.path.exists(path):
        os.makedirs(path)
    
    # check if cleaned data already exists
    if not os.path.exists(os.path.join(path, 'english-spanish.pkl')):
        save_cleaned_data(cleaned_sentences, os.path.join(path, 'english-spanish.pkl'))

    n_sentences = 10000
    dataset = cleaned_sentences[:n_sentences, :]
    np.random.shuffle(dataset)
    train, test = dataset[:9000], dataset[9000:]

    if not os.path.exists(os.path.join(path, 'english-spanish-both.pkl')) and \
        not os.path.exists(os.path.join(path, 'english-spanish-train.pkl')) and \
        not os.path.exists(os.path.join(path, 'english-spanish-test.pkl')):
        save_cleaned_data(dataset, os.path.join(path, 'english-spanish-both.pkl'))
        save_cleaned_data(train, os.path.join(path, 'english-spanish-train.pkl'))
        save_cleaned_data(test, os.path.join(path, 'english-spanish-test.pkl'))

    return dataset, train, test

