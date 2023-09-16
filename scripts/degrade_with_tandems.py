import sys
import os
from pydub import AudioSegment 
from pydub.playback import play 
import pydub.scipy_effects #for low_pass_filter

TEMP_FILE = "temp_audio_file"

def ogg_file(wav_file, bitrate):
    wav_file.export(TEMP_FILE, format='ogg', codec='libvorbis', bitrate=bitrate)
    
def opus_file(wav_file, bitrate):
    wav_file.export(TEMP_FILE, format='opus', codec='libopus', bitrate=bitrate)

def codec_file(wav_file, bitrate, codec_name):
    if codec_name == "ogg":
        ogg_file(wav_file, bitrate)
    elif codec_name == "opus":
        opus_file(wav_file, bitrate)
    else:
        wav_file.export(TEMP_FILE, format=codec_name, bitrate=bitrate)

def save_wav_file(file, ref_id, filter_id, dest_dir):
    try:
        samples = file.get_array_of_samples()
        result = AudioSegment(samples.tobytes(),
                              frame_rate=file.frame_rate,
                              sample_width=file.sample_width,
                              channels=file.channels)
        file_name = ref_id + "_" + filter_id + ".wav"
        result.export(dest_dir + "/" + file_name, format = "wav")
        
    except:
        print("WAV EXPORT PROBLEM")
        print("problem with {}, filter id: {}.".format(ref_id, filter_id))
        
def bicodec_degradation(file, file_name, output_directory, codec1, bitrate1, codec2, bitrate2, new_id):
    codec_file(file, bitrate1, codec1)
    file = AudioSegment.from_file(TEMP_FILE)
    codec_file(file, bitrate2, codec2)
    file = AudioSegment.from_file(TEMP_FILE)
    save_wav_file(file, file_name.split(".")[0], new_id, output_directory)
                    

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
                    
                    ## 08_13
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "mp3", "128k", "08_13")
                    
                    ## 16_22
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "adts", "128k", "16_22")
                    
                    ## 27_29
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "700k", "ogg", "64k", "27_29")
                    
                    ## 32_38
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "opus", "128k", "32_38")
                    
                    ## 41_05
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "mp2", "128k", "41_05")
                    
                    
                    
                    ## 07_23
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "256k", "adts", "192k", "07_23")
                    
                    ## 15_30
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "256k", "ogg", "96k", "15_30")
                    
                    ## 24_39
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "256k", "opus", "160k", "24_39")
                    
                    ## 40_06
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "192k", "mp2", "192k", "40_06")
                    
                    ## 31_14
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "mp3", "192k", "31_14")
                    
                    
                    
                    ## 08_31
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "ogg", "128k", "08_31")
                    
                    ## 16_40
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "opus", "192k", "16_40")
                    
                    ## 27_07
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "700k", "mp2", "256k", "27_07")
                    
                    ## 32_15
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "mp3", "256k", "32_15")
                    
                    ## 41_24
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "adts", "256k", "41_24")
                    
                    
                    
                    ## 06_38
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "192k", "opus", "128k", "06_38")
                    
                    ## 14_05
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "192k", "mp2", "128k", "14_05")
                    
                    ## 23_13
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "192k", "mp3", "128k", "23_13")
                    
                    ## 30_22
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "96k", "adts", "128k", "30_22")
                    
                    ## 39_29
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "160k", "ogg", "64k", "39_29")
                    
                    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Shutdown requested...exiting")
                    sys.exit(0)
                except:
                    print("{} ERROR.".format(file_name))

                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))