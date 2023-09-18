import numpy as np
import pandas as pd
import h5py
import tensorflow as tf
from datetime import datetime
import sys

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras import Sequential

from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model

from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Input


base_model = VGG19(weights='imagenet')
base_model.trainable = False

base_model.save("VGG19.h5")

        
input_tensor = Input(shape=(224, 224, 3))
base_model = InceptionV3(input_tensor=input_tensor, weights='imagenet', include_top=True)
base_model.trainable = False

base_model.save("InceptionV3.h5")
