# DesmosAudio
 
A simple Python program to turn an audio file into a series of Desmos expressions, using the `tone` feature.

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Method](#method)
- [Usage](#usage)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Graphs](#graphs)

## Requirements

**Dependencies:**
- NumPy (>=1.25.2)
- PyDub (>=0.25.1)
- Pyperclip (>=1.8.2)

```shell
pip install -r requirements.txt
```

To load audio files that are not in uncompressed .wav format, you also need `ffmpeg` or `libav`, which PyDub uses internally.
To install these libraries, please follow these directions at the [PyDub Documentation](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up).

## Installation

Simply clone the repository to get started.

```shell
git clone --depth 1 --branch master https://github.com/alorans/DesmosAudio.git
````

## Method

**Internally, the program:**

1. Converts the audio to an uncompressed waveform.
2. Splits the waveform into "chunks", by default each lasting 1/30 of a second.
3. Performs a Fast Fourier Transform (FFT) on each chunk, extracting the pure frequency components of the chunk, and their amplitudes.
4. Selects, by default, the 250 most prominent frequencies.
5. Formats the data as a copyable Desmos expression, and outputs to a file or directly to the system clipboard.

## Usage

**Begin by importing the *audio_to_desmos* function.**

```python
from DesmosAudio import audio_to_desmos

if __name__ == "__main__":
    audio_to_desmos(
        audio_file="<your_path>.mp3",
        output_file="output.txt",
        clipboard=True,
        start_seconds=0,
        end_seconds=20,
    )
```

**An overview of its arguments:**

- `audio_file: str`
  - The input audio filepath
  - Must be .wav, unless ffmpeg is installed, in which case
  - Can be in any format supported by ffmpeg
- `output_file: str = None`
  - The path to the output text file
  - .txt recommended extension
- `clipboard: bool = False`
  - Weather or not to output the result to the system clipboard
- `start_seconds: float = 0`
  - The beginning of the audio range to convert
- `end_seconds: float = 1`
  - The end of the audio range to convert
- `read_all: bool = False`
  - If true, will read from the start_seconds value to the end of the audio file
- `samples_per_second: float = 30`
  - How many audio samples per second the output will be
  - Like audio FPS
- `max_frequencies: int = 250`
  - The number of frequencies to select for each "chunk"
- `min_freq_threshold: int = 20`
  - The minimum frequency which will be accepted
  - Can help with low-pitched noise in the result
- `max_freq_threshold: int = 20000`
  - The maximum frequency which will be accepted
  - Can help with high-pitched noise in the result
- `offset_octaves: int = 1`
  - Due to discrepancies between the pydub and inbuilt wave modules, some audio files output an octave lower than they should
  - The default here is 1 octave higher, which works most of the time
  - Occasionally this setting may have to be adjusted

**After converting the audio:**

- Create a copy of this [graph](https://www.desmos.com/calculator/qwm6rncmry).
- Copy the contents of the output file, or use the clipboard option to automatically do this.
- Paste the contents into the `Music` folder of the graph. It will be difficult to delete all the expressions if they are not in a common folder. Know that this may take a moment.
- Note the values printed by the program for `Length` and `FPS`. Enter these into the fields with the same name under `User Settings` in Desmos.
- Ensure that the graph is unmuted and click the arrow next to `Play` to hear your audio clip.
- Take note of the limitations listed below, and fine tune the setting to get the best quality output.

## Limitations

While Desmos is an extremely powerful tool, keep in mind that it is not intended for playing audio tracks. Certain limitations do arise:

- More than 25-30 seconds at 30 sample rate results in choppy audio.
- 250 frequency channels is usually more than enough, and much more can also cause choppy audio.
- A lower sample rate, such as 15, can hold much more audio, up to about 90 seconds.

- When set to a low sample rate, such as 10-15 times per second, high-pitched artifacts often appear.
- Occasionally, the program does not pick up on soft baselines and lower-pitched tones.

- The reason for the *offset_octaves* parameter being necessary could be considered a limitation. It might be something wrong with my code...

**Keep in mind**

- Desmos does not allow you to save a graph more than 5 megabytes in size. Larger audio segments can easily become greater than this.

## Contributing

Contributions would also be greatly appreciated. This program was written quickly and not robustly tested, so any and all help is welcome. Please feel free to use and expand on this program in any way you like.

**Please do not use this in the Desmos Math Art Contest, to preserve the integrity of the competition.** 

## Graphs

**Base audio player**

- [Audio](https://www.desmos.com/calculator/ylxqx8fcek)

**Example audio, with added player graphics**

- [Rick Astley - Never Gonna Give You Up](https://www.desmos.com/calculator/atkwoczcor)
- [Billy Joel - Uptown Girl](https://www.desmos.com/calculator/tccpqy7uqu)
