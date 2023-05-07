from preprocess import *
from get_model import *
from evaluate import evaluate_model
import argparse
import os
from keras.callbacks import ModelCheckpoint
from keras.utils.vis_utils import plot_model
from keras.models import load_model

# TODO: train model eng to spa

def train_model(raw_data_path: str = 'raw_data/spa.txt',
                      path: str = 'data') -> None:

    dataset, train, test = build_data_set(raw_data_path, path)




    # prepare english tokenizer
    eng_tokenizer = create_tokenizer(dataset[:, 0])
    eng_vocab_size = len(eng_tokenizer.word_index) + 1
    eng_length = get_max_length(dataset[:, 0])
    print('English Vocabulary Size: %d' % eng_vocab_size)
    print('English Max Length: %d' % (eng_length))
    # prepare spanish tokenizer
    spa_tokenizer = create_tokenizer(dataset[:, 1])
    spa_vocab_size = len(spa_tokenizer.word_index) + 1
    spa_length = get_max_length(dataset[:, 1])
    print('spanish Vocabulary Size: %d' % spa_vocab_size)
    print('spanish Max Length: %d' % (spa_length))

    # define model

    # summarize defined model
    if not os.path.exists('saved_model'):
        os.makedirs('saved_model')

    #print(model.summary())
    # You must install pydot (`pip install pydot`) and install graphviz (see instructions at https://graphviz.gitlab.io/download/) for plot_model to work.
    #plot_model(model, to_file=os.path.join(path, 'model.png'), show_shapes=True)
    filename = os.path.join(path, 'model.h5')
    # prepare training data
    trainX = encode_sequences(spa_tokenizer, spa_length, train[:, 1])
    trainY = encode_sequences(eng_tokenizer, eng_length, train[:, 0])
    trainY = encode_output_sequences(trainY, eng_vocab_size)
    # prepare validation data
    testX = encode_sequences(spa_tokenizer, spa_length, test[:, 1])
    testY = encode_sequences(eng_tokenizer, eng_length, test[:, 0])
    testY = encode_output_sequences(testY, eng_vocab_size)


    # define model
    # model = define_model(ger_vocab_size, eng_vocab_size, ger_length, eng_length, 256)
    model = define_model(spa_vocab_size, eng_vocab_size, spa_length, eng_length, 256*4)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    # summarize defined model
    print(model.summary())

    # fit model
    checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    model.fit(trainX, trainY, epochs=100, batch_size=64, validation_data=(testX, testY), callbacks=[checkpoint], verbose=2)
    # evaluate model
    model = load_model(filename)
    # test on training sequences
    print('train')
    evaluate_model(model, eng_tokenizer, trainX, train)
    # test on test sequences
    print('test')
    evaluate_model(model, eng_tokenizer, testX, test)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_path', type=str, default='raw_data/spa.txt')
    parser.add_argument('--path', type=str, default='data')
    args = parser.parse_args()
    train_model(args.raw_data_path, args.path)