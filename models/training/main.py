#!/usr/bin/env python

import numpy as np
import pandas as pd
import h5py
import tensorflow as tf
from datetime import datetime
import sys

import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras import Sequential

# from keras.applications.vgg19 import VGG19
# from keras.preprocessing import image
# from keras.applications.vgg19 import preprocess_input
# from keras.models import Model

# from tensorflow.keras.applications.inception_v3 import InceptionV3
# from tensorflow.keras.layers import Input



# dataset_path = 'train_data.hdf5'
dataset_path = 'test_test.hdf5'

def get_model(model_name, start_learning_rate = 0.001):
    
    # Neural network
    model = Sequential()
    
    if model_name == "ALBERT":

        model.add(layers.InputLayer(input_shape= (1876, 256), name="input"))
        model.add(layers.Conv1D(filters=64, kernel_size=11, name="conv_1d_1", activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2, name="max_pooling_1d_1"))
        model.add(layers.Dropout(rate=0.01, name="dropout_1"))
        model.add(layers.Conv1D(filters=128, kernel_size=7, name="conv_1d_2", activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2, name="max_pooling_1d_2"))
        model.add(layers.Dropout(rate=0.01, name="dropout_2"))
        model.add(layers.Conv1D(filters=256, kernel_size=3, name="conv_1d_3", activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2, name="max_pooling_1d_3"))
        model.add(layers.Flatten(name="flatten"))
        model.add(layers.Dense(units=256, name="dense_1"))
        model.add(layers.Dropout(rate=0.01, name="dropout_3"))
        model.add(layers.Dense(units=128, name="dense_2"))
        model.add(layers.Dense(units=1, name="dense_3"))
                
    elif model_name == "VGG19":
        
        # base_model = VGG19(weights='imagenet')
        # base_model.trainable = False
        
        base_model = tf.keras.models.load_model("./VGG19.h5")

        model.add(layers.InputLayer(input_shape= (1876, 256), name="input"))
        model.add(layers.Reshape(target_shape= (1876, 256, 1), name="reshape_1"))
        model.add(layers.Conv2D(filters=3, kernel_size=11, name="conv_1d_1", activation='relu'))
        model.add(layers.Resizing(224, 224, name="resize_1"))
        model.add(base_model)
        model.add(layers.Dense(units=256, name="dense_1"))
        model.add(layers.Dense(units=128, name="dense_2"))
        model.add(layers.Dense(units=1, name="dense_3"))
        
    elif model_name == "INCEPTIONv3":
        
        # input_tensor = Input(shape=(224, 224, 3))
        # base_model = InceptionV3(input_tensor=input_tensor, weights='imagenet', include_top=True)
        # base_model.trainable = False
        
        base_model = tf.keras.models.load_model("./InceptionV3.h5")
        
        model.add(layers.InputLayer(input_shape= (1876, 256), name="input"))
        model.add(layers.Reshape(target_shape= (1876, 256, 1), name="reshape_1"))
        model.add(layers.Conv2D(filters=3, kernel_size=11, name="conv_1d_1", activation='relu'))
        model.add(layers.Resizing(224, 224, name="resize_1"))
        model.add(base_model)
        model.add(layers.Dense(units=256, name="dense_1"))
        model.add(layers.Dense(units=128, name="dense_2"))
        model.add(layers.Dense(units=1, name="dense_3"))
        
    else:
        print(">:C")
        exit(-1)
    
    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=float(start_learning_rate)),
        loss='mean_squared_error', 
        metrics=[tf.keras.metrics.RootMeanSquaredError()])
        
    return model


def main(model_name = "ALBERT", epochs = 100, start_learning_rate=0.001, change_learning_rate_factor=0.1):
    print("Hello World!")
    
    dt = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    PATH = "./output/" + model_name + "_" + str(start_learning_rate) + "_" + str(change_learning_rate_factor) + "_" + str(dt) + "/"
    
    print("OUTPUT DIR: " + PATH)
    
    # # load data
    with h5py.File(dataset_path, 'r') as f:
        train_x = np.array(f['train_x'])
        train_y = np.array(f['train_y'])
        validation_x = np.array(f['validation_x'])
        validation_y = np.array(f['validation_y'])
        
    # load model
    model = get_model(model_name, start_learning_rate)
        
    # FIT:
    EPOCHS = int(epochs)
    BATCH_SIZE = 64
        
    # CALLBACKS
    # checkpoint
    checkpoint_filepath = PATH + "model_" + model_name + "-weights-improvement-EPOCH_{epoch:02d}-VAL_LOSS_{val_loss:.5f}.hdf5"
    
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_loss',
        mode='min',
        save_best_only=True
    )
    
    # learning rate change
    reduce_lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=float(change_learning_rate_factor),
        patience=10,
        verbose=1,
        mode='auto',
        min_delta=0.0001,
        cooldown=0,
        min_lr=0.0001
    )
    
    # early stopping
    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        min_delta=0,
        patience=30,
        verbose=1,
        mode='min',
        baseline=None,
        restore_best_weights=False,
        start_from_epoch=10
    )

    # FIT
    history = model.fit(x=train_x, 
        y=train_y, 
        validation_data = (validation_x, validation_y),
        epochs=EPOCHS, 
        batch_size=BATCH_SIZE,
        callbacks=[model_checkpoint_callback, reduce_lr_callback, early_stopping_callback])
        
    # SAVE
    dt = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        
    history_name =  PATH + "history_" + model_name + "-" + dt
    model_file_name =    PATH + "model_" + model_name + "-" + dt
        
    # convert the history.history dict to a pandas DataFrame:     
    hist_df = pd.DataFrame(history.history) 

    # save to json:  
    hist_json_file = history_name + '.json' 
    with open(hist_json_file, mode='w') as f2:
        hist_df.to_json(f2)
                
    model.save(model_file_name + ".h5")
    
    
    # HISTORY PLOT SAVE
    keys = list(history.history.keys())
    # summarize history for accuracy
    plt.subplot(211)
    plt.plot(history.history[keys[0]], label=keys[0])
    plt.plot(history.history[keys[2]], label=keys[2])
    plt.title(keys[0])
    plt.ylabel(keys[0])
    plt.xlabel('epoch')
    plt.legend()
    plt.yscale("log") 
    plt.grid()
    # summarize history for loss
    plt.subplot(212)
    plt.plot(history.history[keys[1]], label=keys[1])
    plt.plot(history.history[keys[3]], label=keys[3])
    plt.title(keys[1])
    plt.ylabel(keys[1])
    plt.xlabel('epoch')
    plt.legend()
    plt.yscale("log") 
    plt.grid()
    plt.tight_layout()
    plt.savefig(PATH + "history_plot.png")
                    
    print("Done!")
        
if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 5:
        print(">:CCCC args error")
        exit(-1)
        
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    # running:
    # python main.py ALBERT 100 0.001 0.1
    # python main.py VGG19 100 0.001 0.1
    # python main.py INCEPTIONv3 100 0.001 0.1