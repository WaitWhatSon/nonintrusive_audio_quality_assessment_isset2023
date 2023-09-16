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
                    
                    # iterate through bitrates for filters
                    
                        # 01,mp2,32k,None
                        # 02,mp2,48k,None
                        # 03,mp2,64k,None
                        # 04,mp2,96k,None
                        # 05,mp2,128k,None
                        # 06,mp2,192k,None # DELETED
                        # 07,mp2,256k,None # DELETED
                        # 08,mp2,320k,None # DELETED
                        
                    # MP2
                    for bitrate in [("01", "32k"), ("02", "48k"), ("03", "64k"), ("04", "96k"),
                                    ("05", "128k"),
                                    # ("06", "192k"), ("07", "256k"), ("08", "320k")
                                    ]:
                        codec_file(wav_file, bitrate[1], "mp2")
                        file = AudioSegment.from_file(TEMP_FILE)
                        save_wav_file(file, file_name.split(".")[0], bitrate[0], output_directory)
                    
                        # 09,mp3,32k,None
                        # 10,mp3,48k,None
                        # 11,mp3,64k,None
                        # 12,mp3,96k,None
                        # 13,mp3,128k,None
                        # 14,mp3,192k,None # DELETED
                        # 15,mp3,256k,None # DELETED
                        # 16,mp3,320k,None # DELETED
                        
                    # MP3
                    for bitrate in [("09", "32k"), ("10", "48k"), ("11", "64k"), ("12", "96k"), 
                                    ("13", "128k"),
                                    # ("14", "192k"), ("15", "256k"), 
                                    # ("16", "320k")
                                    ]:
                        codec_file(wav_file, bitrate[1], "mp3")
                        file = AudioSegment.from_file(TEMP_FILE)
                        save_wav_file(file, file_name.split(".")[0], bitrate[0], output_directory)
                    
                        # 17,adts,24k,None
                        # 18,adts,32k,None
                        # 19,adts,48k,None
                        # 20,adts,64k,None
                        # 21,adts,96k,None
                        # 22,adts,128k,None
                        # 23,adts,192k,None # DELETED
                        # 24,adts,256k,None # DELETED
                        # 25,adts,320k,None # DELETED
                        # 26,adts,512k,None # DELETED
                        # 27,adts,700k,None # DELETED
                        
                    # ADTS
                    for bitrate in [("17", "24k"), ("18", "32k"), ("19", "48k"), ("20", "64k"), 
                                    ("21", "96k"), ("22", "128k"), 
                                    # ("23", "192k"), 
                                    # ("24", "256k"), ("25", "320k"), ("26", "512k"), ("27", "700k")
                                    ]:
                        codec_file(wav_file, bitrate[1], "adts")
                        file = AudioSegment.from_file(TEMP_FILE)
                        save_wav_file(file, file_name.split(".")[0], bitrate[0], output_directory)
                    
                        # 28,ogg,48k,None
                        # 29,ogg,64k,None
                        # 30,ogg,96k,None
                        # 31,ogg,128k,None
                        # 32,ogg,192k,None # DELETED

                    # OGG
                    for bitrate in [("28", "48k"), ("29", "64k"), ("30", "96k"), ("31", "128k"), 
                                    # ("32", "192k")
                                    ]:
                        ogg_file(wav_file, bitrate[1])
                        file = AudioSegment.from_file(TEMP_FILE)
                        save_wav_file(file, file_name.split(".")[0], bitrate[0], output_directory)
                    
                        # 33,opus,24k,None
                        # 34,opus,32k,None
                        # 35,opus,48k,None
                        # 36,opus,64k,None
                        # 37,opus,96k,None
                        # 38,opus,128k,None
                        # 39,opus,160k,None # DELETED
                        # 40,opus,192k,None # DELETED
                        # 41,opus,256k,None # DELETED
                    
                    # OPUS
                    for bitrate in [("33", "24k"), ("34", "32k"), ("35", "48k"), 
                                    ("36", "64k"), ("37", "96k"), ("38", "128k"), 
                                    # ("39", "160k"), ("40", "192k"), ("41", "256k")
                                    ]:
                        opus_file(wav_file, bitrate[1])
                        file = AudioSegment.from_file(TEMP_FILE)
                        save_wav_file(file, file_name.split(".")[0], bitrate[0], output_directory)
                    
                except KeyboardInterrupt:
                    print("KeyboardInterrupt: Shutdown requested...exiting")
                    sys.exit(0)
                except:
                    print("{} ERROR.".format(file_name))

                print("{}/{}".format(i+1, files_count), end='\r')
            
            print("\nDONE")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))