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
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "mp2", "32k", "17_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "mp2", "48k", "17_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "mp2", "64k", "17_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "mp2", "96k", "17_04")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "mp2", "128k", "17_05")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "mp3", "32k", "18_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "mp3", "48k", "18_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "mp3", "64k", "18_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "mp3", "96k", "18_12")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "mp3", "128k", "18_13")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "ogg", "48k", "17_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "ogg", "64k", "17_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "ogg", "96k", "17_30")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "24k", "ogg", "128k", "17_31")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "opus", "32k", "18_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "opus", "48k", "18_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "opus", "64k", "18_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "opus", "96k", "18_37")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "32k", "opus", "128k", "18_38")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "mp3", "32k", "01_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "mp3", "48k", "01_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "mp3", "64k", "01_11")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "adts", "32k", "02_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "adts", "48k", "02_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "adts", "64k", "02_20")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "ogg", "48k", "01_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "ogg", "64k", "01_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "32k", "ogg", "96k", "01_30")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "opus", "32k", "02_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "opus", "48k", "02_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "48k", "opus", "64k", "02_36")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "mp2", "32k", "29_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "mp2", "48k", "29_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "mp2", "64k", "29_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "mp2", "96k", "29_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "mp3", "32k", "28_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "mp3", "48k", "28_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "mp3", "64k", "28_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "mp3", "96k", "28_12")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "adts", "32k", "29_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "adts", "48k", "29_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "adts", "64k", "29_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "64k", "adts", "96k", "29_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "opus", "32k", "28_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "opus", "48k", "28_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "opus", "64k", "28_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "48k", "opus", "96k", "28_37")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "ogg", "48k", "34_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "ogg", "64k", "34_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "ogg", "48k", "34_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "ogg", "64k", "34_29")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "adts", "32k", "33_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "adts", "48k", "33_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "adts", "64k", "33_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "adts", "96k", "33_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "mp3", "32k", "34_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "mp3", "48k", "34_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "mp3", "64k", "34_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "32k", "mp3", "96k", "34_12")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "mp2", "32k", "33_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "mp2", "48k", "33_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "mp2", "64k", "33_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "24k", "mp2", "96k", "33_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "mp2", "32k", "09_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "mp2", "48k", "09_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "mp2", "64k", "09_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "mp2", "96k", "09_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "adts", "32k", "09_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "adts", "48k", "09_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "adts", "64k", "09_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "32k", "adts", "96k", "09_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "ogg", "48k", "10_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "ogg", "64k", "10_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "ogg", "48k", "10_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "ogg", "96k", "10_30")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "opus", "32k", "10_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "opus", "48k", "10_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "opus", "64k", "10_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "48k", "opus", "96k", "10_37")
                    
                    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Shutdown requested...exiting")
                    sys.exit(0)
                except:
                    print("{} ERROR.".format(file_name))

                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))