import sys
import os
from pydub import AudioSegment

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
                
                file_name = onlyfiles[i]
        
                try:
                    wav_file = AudioSegment.from_file(file = os.path.join(dirname, file_name), format = "wav")
                    
                    # check if sampling rate OK -> 48000 Hz
                    # check if sample width // must be 16b -> == 2
                    # check if mono
                    
                    if wav_file.sample_width != 2 or wav_file.frame_rate != 48000 or wav_file.channels != 1:
                
                        if wav_file.sample_width != 2: 
                            print("{} has wrong sample width - it will be fixed.".format(file_name))
                            wav_file = wav_file.set_sample_width(2)
                            
                        if wav_file.frame_rate != 48000:
                            print("{} has wrong sample rate - it will be fixed.".format(file_name))
                            wav_file = wav_file.set_frame_rate(48000)
                            
                        if wav_file.channels != 1:
                            print("{} is not mono - it will be fixed.".format(file_name))
                            wav_file = wav_file.set_channels(1)
                            
                        wav_file.export(os.path.join(dirname, file_name), format="wav")
                    
                except:
                    print("{} EXCEPTION\n".format(onlyfiles[i]))
                    
                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
        
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))