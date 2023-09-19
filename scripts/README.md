# Scripts

## Audio format
- .wav files
- sample rate = 48000 Hz
- sample width = 16 b (2)
- channels = mono
- time = 10 s

## Audio normalization
- `python normalize_wav_files.py <audio_files_directory_path>`

## Reference audio files
- `python clean_wav_files.py <audio_files_directory_path>`
- `python trim_wav_files.py <audio_files_directory_path>`

## Degraded audio files preparation
Degradation types list: [degradation_processes.csv](../csv/degradation_processes.csv)

Before:
- low-pass filter won't work without *import pydub.scipy_effects* in script even if it's not directly used; `pip install scipy` required

Run script (for basic only codec degradation):
- `python degrade_wav_files.py <source_files_directory> <destination_files_directory>`

For low-pass filters degradation:
- `python degrade_with_lowpass.py <source_files_directory> <destination_files_directory>`

For tandems degradation:
- `python degrade_with_tandems.py <source_files_directory> <destination_files_directory>`

Format of generated files names is `refid_degradationid.wav`; degradation list columns meaning:
- `id` - reference audio file name
- `format` - audio codec
- `bitrate` - codec bitrate
- `lowpass` - low-pass filter frequency if applied, else None

Run *clean* and *trim* scripts on degraded files.

## Generate objective scores with ViSQOL v3
### ViSQOL
Follow the installation instructions of ViSQOL from its [GitHub repository](https://github.com/google/visqol)

### Input CSV file
- `python generate_visqol_input_csv.py <dataset_directory> <reference_files_directory> <new_file_path>`

### Objective scores
- in directory *visqol/visqol-master* (e.g. via gitbash):
- `bazel-bin\\visqol.exe --batch_input_csv <input_dataset_file.csv> --results_csv <output_dataset_file.csv> --output_debug <debug_01.json>`

### Check histogram for generated scores
- `python check_histogram.py <output_dataset_file.csv>`

## Spectrograms format

``` Python

def min_max_normalise(values):
    _min, _max = np.min(values), np.max(values)
    return (values - _min) / (_max - _min)

def mos_normalise(values):
    return (values - 1) / 4

TIME = 10
SR = 48000
N_FFT = 2048
HOP_LENGTH = 256
N_MELS = 256

audio, _ = librosa.load(filename, sr=SR)
audio = audio[:TIME * SR]
# mel spectrograms
spectrogram = librosa.feature.melspectrogram(y=audio, sr=SR, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)
spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
spectrogram = np.rot90(spectrogram)
# normalisation
spectrogram = min_max_normalise(spectrogram)
mos = mos_normalise(row.moslqo)

```

Full code in [dataset.py](/scripts/dataset.py)