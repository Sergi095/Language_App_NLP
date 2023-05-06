from typing import List, Tuple
import numpy as np
from pickle import load
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu
from get_model import predict_sequence, load_clean_sentences, create_tokenizer, get_max_length, encode_sequences, encode_output_sequences


def evaluate_model(model, tokenizer: Tokenizer, sources: np.array, raw_dataset: List[Tuple[str, str]]) -> None:
    actual, predicted = list(), list()
    for i, source in enumerate(sources):
        # translate encoded source text
        source = source.reshape((1, source.shape[0]))
        translation = predict_sequence(model, tokenizer, source)
        raw_target, raw_src = raw_dataset[i]
        if i < 10:
            print('source=[%s], target=[%s], predicted=[%s]' % (raw_src, raw_target, translation))
        actual.append([raw_target.split()])
        predicted.append(translation.split())
    # calculate BLEU score
    for i in range(1, 5):
        print(f'BLEU-{i}: {corpus_bleu(actual, predicted, weights=[round(1/i, 1) for _ in range(i)])}')

