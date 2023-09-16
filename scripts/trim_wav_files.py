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
                    samples = wav_file.get_array_of_samples()
                    
                    if len(samples) < wav_file.frame_rate*10:
                        print("{} is to short -> must have at least 10 s".format(file_name))
                        
                    if len(samples) > wav_file.frame_rate*10:
                        print("{} is too long - it will be fixed.".format(file_name))
                        samples = samples[0 : wav_file.frame_rate*10]
                        wav_file = AudioSegment(samples.tobytes(),
                                                frame_rate = wav_file.frame_rate,
                                                sample_width = wav_file.sample_width,
                                                channels = wav_file.channels)
                        wav_file.export(os.path.join(dirname, file_name), format="wav")

                except:
                    print("{} EXCEPTION\n".format(onlyfiles[i]))
                        
                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
                
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))