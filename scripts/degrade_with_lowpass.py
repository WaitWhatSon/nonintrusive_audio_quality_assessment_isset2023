import sys
import os
from pydub import AudioSegment 
from pydub.playback import play 
import pydub.scipy_effects #for low_pass_filter

TEMP_FILE = "temp_audio_file"

def filter_and_save_file(wav_file, freq, ref_id, filter_id, dest_dir):
    filtered = wav_file.low_pass_filter(cutoff_freq=freq, order=4)
    samples = filtered.get_array_of_samples()[0:48000*10]
    result = AudioSegment(samples.tobytes(),
                          frame_rate=filtered.frame_rate,
                          sample_width=filtered.sample_width,
                          channels=filtered.channels)
    file_name = ref_id + "_" + filter_id + ".wav"
    result.export(dest_dir + "/" + file_name, format = "wav")

def main(args):
    
    if len(args) != 2:
        print("wrong number of arguments; two arguments required: input directory path, output directory path")
        exit()
    
    else:    
        input_directory = args[0]
        output_directory = args[1]
    
        if not os.path.isdir(input_directory):
            print("input directory {} does not exist.".format(input_directory))
        if not os.path.isdir(output_directory):
            print("output directory {} does not exist.".format(input_directory))
        else:
            print("searching for audio files in {}.".format(input_directory))
          
            onlyfiles = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
            files_count = len(onlyfiles)
            
            for i in range(files_count):
                
                file_name = onlyfiles[i]
        
                try:
                    wav_file = AudioSegment.from_file(file = os.path.join(input_directory, file_name), format = "wav")
                    
                       # 42,wav,None,3500
                        # 43,wav,None,5000
                        # 44,wav,None,7500
                        # 45,wav,None,9000
                        
                    # LOW-PASS FILTER
                    for freq in [("42", 3500), ("43", 5000), ("44", 7500), ("45", 9000)]:
                        filter_and_save_file(wav_file, freq[1], file_name.split(".")[0], freq[0], output_directory)
                    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Shutdown requested...exiting")
                    sys.exit(0)
                except:
                    print("{} ERROR.".format(file_name))

                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))