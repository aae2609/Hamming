import pandas as pd
import tensorflow as tf

COLUMN_NAMES = ['id', 'plainword', 'codeword', 
                'id_error', 'bin_error', 'defective_codeword']

TRAIN_PATH = "/content/drive/Hamming/hamming.txt"


def hamming_distance(first: str, second: str) -> int:
    return len([1 for (x, y) in zip(first, second) if x != y])


def loss_hamming(y, y_pred):
    return sum(hamming_distance(f,s) for (f,s) in zip(y, y_pred)) / y.shape[0]


def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(buffer_size=1000).repeat(count=None).batch(batch_size)
    return dataset.make_one_shot_iterator().get_next()


if __name__ == '__main__':
    pass
