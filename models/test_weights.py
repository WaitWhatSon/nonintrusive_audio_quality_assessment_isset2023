import numpy as np
import h5py
import sys

import tensorflow as tf
from scipy import stats
from sklearn import metrics
import matplotlib.pyplot as plt


# dataset = np.load("test_dataset_750.pkl", allow_pickle=True)

# _1  = dataset[0]
# _2  = dataset[1]
# _3  = dataset[2]

# with h5py.File('test_data_750.hdf5', 'w') as f:
#     f.create_dataset('test_x', data = _1)
#     f.create_dataset('test_y', data = _2)
#     f.create_dataset('test_refnum', data = _3)


dataset_path = 'test_data_750.hdf5'

# # load data
with h5py.File(dataset_path, 'r') as f:
    test_x = np.array(f['test_x'])
    test_y = np.array(f['test_y'])


def make_plots_for_model(model_path, weights_path):

    model = tf.keras.models.load_model(model_path)
    
    model.load_weights(weights_path)

    predictions = model.predict(test_x)

    print("Współczynnik korelacji Pearsona:")
    correlation, p_value = stats.pearsonr(predictions.flatten(), test_y)
    print(correlation)
    # print(p_value)
    print("RMSE:")
    rmse = metrics.mean_squared_error(predictions.flatten(), test_y/100, squared=False)
    print(rmse)

    plt.figure(figsize=(6,6))
    plt.grid()
    plt.scatter(test_y, predictions.flatten(), s=5)
    plt.ylabel("Oceny modelu nieinwazyjnego")
    plt.xlabel("Oceny modelu inwazyjnego")
    plt.title("Oceny próbek")
    plt.plot([0, 1], [0, 1])
    plt.show()
    

def main(model_path, weights_path):
    make_plots_for_model(model_path, weights_path)
    
    
if __name__ == "__main__":
    print(sys.argv)
if len(sys.argv) != 3:
    print(">:CCCC args error")
    exit(-1)
    
main(sys.argv[1], sys.argv[2])
