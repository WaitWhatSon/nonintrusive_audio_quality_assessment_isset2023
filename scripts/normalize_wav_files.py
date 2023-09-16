import sys
import os
from pydub import AudioSegment

import soundfile as sf
import pyloudnorm as pyln


def main(args):
    
    if len(args) == 0:
        print("wrong number of arguments; at least one directory path required")
        exit()
    
    for dirname in args:
        if not os.path.isdir(dirname):
            print("directory {} does not exist.".format(dirname))
        else:
            print("searching for audio files in {}.".format(dirname))
          
            onlyfiles = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
            files_count = len(onlyfiles)
            
            for i in range(files_count):
                
                filename = onlyfiles[i]
        
                try:
                    data, rate = sf.read(os.path.join(dirname, filename)) # load audio
                    
                    # measure the loudness first 
                    meter = pyln.Meter(rate) # create BS.1770 meter
                    loudness = meter.integrated_loudness(data)

                    # loudness normalize audio to -23 dB LUFS
                    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -23.0)

                    sf.write(os.path.join(dirname, filename), loudness_normalized_audio, rate)
                    
                except:
                    print("{} EXCEPTION\n".format(onlyfiles[i]))
                    
                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
        
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))