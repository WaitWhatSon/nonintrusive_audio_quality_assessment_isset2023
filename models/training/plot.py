import sys
import matplotlib.pyplot as plt
import json


def main(history):

    print(history.keys())
    keys = list(history.keys())
    
    print(keys[0])
    print(history[keys[0]].values())

    # summarize history for accuracy
    plt.subplot(211)
    plt.plot(history[keys[0]].values(), label=keys[0])
    plt.plot(history[keys[2]].values(), label=keys[2])
    plt.title(keys[0])
    plt.ylabel(keys[0])
    plt.xlabel('epoch')
    plt.legend()
    plt.yscale("log") 
    plt.grid()
    # summarize history for loss
    plt.subplot(212)
    plt.plot(history[keys[1]].values(), label=keys[1])
    plt.plot(history[keys[3]].values(), label=keys[3])
    plt.title(keys[1])
    plt.ylabel(keys[1])
    plt.xlabel('epoch')
    plt.legend()
    plt.yscale("log") 
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print(sys.argv)
    
    with open(sys.argv[1], "r") as file_stream:
        python_data = json.load(file_stream)
 
        print(f'Python data: {python_data}')
        main(python_data)
    
    # run:
    # python plot.py <plik.json>