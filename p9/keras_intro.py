# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:58:26 2020

@author: 10655
"""
import tensorflow as tf
from tensorflow import keras

def get_dataset(training=True):
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    if training is False:
        return test_images, test_labels
    return train_images, train_labels
    
def print_stats(images, labels):
    return None
def view_image(image, label):
    return None
def build_model():
    return None
def train_model(model, images, labels, T):
    return None
def evaluate_model(model, images, labels, show_loss=True):
    return None
def predict_label(model, images, index):
    return None
