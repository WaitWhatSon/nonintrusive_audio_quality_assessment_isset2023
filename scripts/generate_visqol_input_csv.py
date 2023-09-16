import sys
import os
from os import listdir
from os.path import isfile, join
import pandas as pd


def main(args):
    
    if len(args) != 3:
        print("wrong number of arguments; required: dataset directory path, references path, name for generated csv file")
        exit()
        
    dirname = args[0]
    references_dirname = args[1]
    new_filename = args[2]
    
    if not os.path.isdir(dirname):
        print("directory {} does not exist.".format(dirname))
        exit()
    
    print("searching for files in {}.".format(dirname))
          
    onlyfiles = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
    
    source_path =  os.path.abspath(dirname)
    reference_path = os.path.abspath(references_dirname)
    
    onlyfiles = [source_path + "\\" + f for f in listdir(source_path) if isfile(join(source_path, f))]
    files = pd.DataFrame(onlyfiles, columns = ["deg"])
    files["ref"] = [reference_path + "\\" + file.split("\\")[-1].split("_")[0] + ".wav" for file in onlyfiles]
    files = files[['ref', 'deg']]
    files.to_csv(new_filename, index = False)
    
    print("DONE - file {} saved".format(new_filename))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))