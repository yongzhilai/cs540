import tensorflow as tf
from tensorflow import keras

def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    if training is False:
        return test_images, test_labels
    return train_images, train_labels
