import tensorflow as tf
import os
import typer
import spacy
from spacy.util import get_words_and_spaces
from spacy.tokens import Doc, DocBin
import tensorflow_datasets as tfds

# physic_devices=tf.config.list_physical_devices("GPU")
# tf.config.experimental.set_memory_growth(physic_devices[0], True)

(ds_train, ds_test), ds_info=tfds.load(
    "conll2002", split=["train", "test"],
    as_supervised=True, with_info=True
)

print(ds_train)