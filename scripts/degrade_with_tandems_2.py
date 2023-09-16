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
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "700k", "mp2", "32k", "27_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "512k", "mp2", "48k", "26_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "320k", "mp2", "64k", "25_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "256k", "mp2", "96k", "24_04")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "192k", "mp2", "128k", "23_05")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "700k", "mp3", "32k", "27_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "512k", "mp3", "48k", "26_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "320k", "mp3", "64k", "25_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "256k", "mp3", "96k", "24_12")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "192k", "mp3", "128k", "23_13")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "512k", "ogg", "48k", "26_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "320k", "ogg", "64k", "25_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "256k", "ogg", "96k", "24_30")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "192k", "ogg", "128k", "23_31")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "700k", "opus", "32k", "27_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "512k", "opus", "48k", "26_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "320k", "opus", "64k", "25_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "256k", "opus", "96k", "24_37")
                    bicodec_degradation(wav_file, file_name, output_directory, "adts", "192k", "opus", "128k", "23_38")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "mp3", "32k", "08_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "256k", "mp3", "48k", "07_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "192k", "mp3", "64k", "06_11")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "adts", "32k", "08_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "256k", "adts", "48k", "07_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "192k", "adts", "64k", "06_20")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "ogg", "48k", "08_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "256k", "ogg", "64k", "07_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "192k", "ogg", "96k", "06_30")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "320k", "opus", "32k", "08_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "256k", "opus", "48k", "07_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp2", "192k", "opus", "64k", "06_36")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "mp2", "32k", "32_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "mp2", "48k", "31_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "mp2", "64k", "32_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "mp2", "96k", "31_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "mp3", "32k", "32_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "mp3", "48k", "31_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "mp3", "64k", "32_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "mp3", "96k", "31_12")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "adts", "32k", "32_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "adts", "48k", "31_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "adts", "64k", "32_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "adts", "96k", "31_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "opus", "32k", "32_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "opus", "48k", "31_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "192k", "opus", "64k", "32_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "ogg", "128k", "opus", "96k", "31_37")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "ogg", "48k", "38_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "192k", "ogg", "64k", "39_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "160k", "ogg", "48k", "40_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "128k", "ogg", "64k", "41_29")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "adts", "32k", "38_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "192k", "adts", "48k", "39_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "160k", "adts", "64k", "40_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "128k", "adts", "96k", "41_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "mp3", "32k", "38_09")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "192k", "mp3", "48k", "39_10")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "160k", "mp3", "64k", "40_11")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "128k", "mp3", "96k", "41_12")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "256k", "mp2", "32k", "38_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "192k", "mp2", "48k", "39_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "160k", "mp2", "64k", "40_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "opus", "128k", "mp2", "96k", "41_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "mp2", "32k", "16_01")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "256k", "mp2", "48k", "15_02")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "192k", "mp2", "64k", "14_03")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "128k", "mp2", "96k", "13_04")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "adts", "32k", "16_18")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "256k", "adts", "48k", "15_19")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "192k", "adts", "64k", "14_20")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "128k", "adts", "96k", "13_21")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "ogg", "48k", "16_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "256k", "ogg", "64k", "15_29")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "192k", "ogg", "48k", "14_28")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "128k", "ogg", "96k", "13_30")
                    
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "320k", "opus", "32k", "16_34")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "256k", "opus", "48k", "15_35")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "192k", "opus", "64k", "14_36")
                    bicodec_degradation(wav_file, file_name, output_directory, "mp3", "128k", "opus", "96k", "13_37")
                    
                    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Shutdown requested...exiting")
                    sys.exit(0)
                except:
                    print("{} ERROR.".format(file_name))

                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))