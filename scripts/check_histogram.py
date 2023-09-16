import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def main(args):
    
    if len(args) != 1:
        print("wrong number of arguments; one csv file path required")
        exit()
        
    file_name = args[0]
    
    if not os.path.isfile(file_name):
        print("NOT A FILE!!! >:C")
        exit()
        
    if file_name.split(".")[-1] != "csv":
        print("NOT CSV FILE!!! >:C")
        
    try:
        df = pd.read_csv(file_name)
    except:
        print("PROBLEM WITH YOUR FILE ;__;")
        exit()
        
    df.moslqo.hist()
    plt.show()
        
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))