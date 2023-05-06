import numpy as np
import pickle
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences, to_categorical
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding, RepeatVector, TimeDistributed
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras import regularizers


def get_word_for_id(integer: int, tokenizer: Tokenizer) -> str:
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


def predict_sequence(model, tokenizer: Tokenizer, source: np.array) -> str:
    prediction = model.predict(source, verbose=0)[0]
    integers = [np.argmax(vector) for vector in prediction]
    target = []
    for i in integers:
        word = get_word_for_id(i, tokenizer)
        if word is None:
            break
        target.append(word)
    return ' '.join(target)


def load_clean_sentences(filename: str) -> np.array:
    with open(filename, 'rb') as f:
        return pickle.load(f)


def create_tokenizer(lines: list) -> Tokenizer:
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return tokenizer


def get_max_length(lines: list) -> int:

    lines = [line.split() for line in lines]
    max_length = max(len(line) for line in lines)
    return max_length


def encode_sequences(tokenizer: Tokenizer, length: int, lines: list) -> np.array:
    sequences = tokenizer.texts_to_sequences(lines)
    sequences = pad_sequences(sequences, maxlen=length, padding='post')
    return sequences


def encode_output_sequences(sequences: np.array, vocab_size: int) -> np.array:
    ylist = []
    for sequence in sequences:
        encoded = to_categorical(sequence, num_classes=vocab_size)
        ylist.append(encoded)
    y = np.array(ylist)
    y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
    return y


def define_model(src_vocab: int, tar_vocab: int, src_timesteps: int, tar_timesteps: int, n_units: int) -> Sequential:
    model = Sequential()
    model.add(Embedding(src_vocab, n_units, input_length=src_timesteps, mask_zero=True))
    model.add(LSTM(n_units))
    model.add(RepeatVector(tar_timesteps))
    model.add(LSTM(n_units, return_sequences=True))
    model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
    return model

