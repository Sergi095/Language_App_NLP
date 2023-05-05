import numpy as np
import tensorflow as tf
from tensorflow import keras
from modules import PositionalEmbedding, TransformerEncoder, TransformerDecoder
from helpers import *
import os
import sys
import argparse

def get_model(sequence_length: int=20, 
              vocab_size: int=15000, 
              embed_dim: int=256, 
              latent_dim: int=2048, 
              num_heads: int=8) -> keras.Model:

    encoder_inputs = keras.Input(shape=(None,), dtype="int64", name="encoder_inputs")
    x = PositionalEmbedding(sequence_length, vocab_size, embed_dim)(encoder_inputs)
    encoder_outputs = TransformerEncoder(embed_dim, latent_dim, num_heads)(x)
    encoder = keras.Model(encoder_inputs, encoder_outputs)

    decoder_inputs = keras.Input(shape=(None,), dtype="int64", name="decoder_inputs")
    encoded_seq_inputs = keras.Input(shape=(None, embed_dim), name="decoder_state_inputs")
    x = PositionalEmbedding(sequence_length, vocab_size, embed_dim)(decoder_inputs)
    x = TransformerDecoder(embed_dim, latent_dim, num_heads)(x, encoded_seq_inputs)
    x = layers.Dropout(0.5)(x)
    decoder_outputs = layers.Dense(vocab_size, activation="softmax")(x)
    decoder = keras.Model([decoder_inputs, encoded_seq_inputs], decoder_outputs)

    decoder_outputs = decoder([decoder_inputs, encoder_outputs])
    transformer = keras.Model(
        [encoder_inputs, decoder_inputs], decoder_outputs, name="transformer"
    )
    return transformer

def train(model: keras.Model, 
          train_ds: tf.data.Dataset, 
          val_ds: tf.data.Dataset, 
          epochs: int=1,
          path: str = 'saved_model')-> keras.Model:
    tf.config.list_physical_devices('GPU')
    model.summary()
    model.compile(
        "rmsprop", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    model.fit(train_ds, epochs=epochs, validation_data=val_ds)



    return model


def main(model: keras.Model, 
         train_ds: tf.data.Dataset, 
         val_ds: tf.data.Dataset, 
         epochs: int=1,
         path: str = 'saved_model')-> None:


    model = train(model, train_ds, val_ds, epochs=epochs)

    if not os.path.exists(path):
        os.makedirs(path)
    
    full_path= os.path.join(path, 'model.h5')
    model.save(full_path)

    


if __name__ == "__main__":


    text_file = get_file()
    text_pairs = parsing(text_file)
    train_pairs, val_pairs, test_pairs = split_data(text_pairs)
    eng_vectorization, spa_vectorization = encode_eng_text(train_pairs)
    train_ds = make_dataset(train_pairs, eng_vectorization, spa_vectorization)
    val_ds = make_dataset(val_pairs, eng_vectorization, spa_vectorization)
    model = get_model()
    parser = argparse.ArgumentParser()
    parser.add_argument("--epoch", type=int, default=30, help="epochs")
    args = parser.parse_args()



    main(model, train_ds, val_ds, args.epoch)