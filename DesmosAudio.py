from pydub import AudioSegment
import numpy as np
import scipy.fftpack
import wave
import io


def load_audio(
        file: str
) -> wave.Wave_read:
    # Load the audio file
    audio = AudioSegment.from_file(file)

    # Set to mono (single channel audio)
    audio.set_channels(1)

    # Convert audio to wav using temporary bitstream
    file_handle = io.BytesIO()
    audio.export(file_handle, format="wav")
    file_handle.seek(0)
    wav = wave.open(file_handle, 'rb')

    return wav


def process_audio_chunk(
        wav_file: wave.Wave_read,
        chunk_size: int,
        sample_rate: int,
        min_freq_threshold: int,
        max_freq_threshold: int,
        offset_octaves: int,
        max_frequencies: int
) -> list:
    # Read a chunk from the wav file
    data = wav_file.readframes(chunk_size)

    # Convert the chunk waveform to a numpy array
    data = np.frombuffer(data, dtype=np.int16)

    # Perform the fourier transform on the chunk
    fft = np.abs(scipy.fftpack.fft(data))

    # Get the frequencies corresponding to the FFT values
    freqs = scipy.fftpack.fftfreq(len(fft), 1.0 / sample_rate)

    # Combine the frequencies and FFT values into a list of tuples
    chunk = list(zip(freqs, fft))

    # Round and map fft values to Desmos volume
    vol_multiplier = 5000000
    offset = 2 ** offset_octaves

    # Filter out frequencies/amplitudes above the thresholds
    chunk = [[offset * int(item[0]), round(2 ** (item[1] / vol_multiplier) - 1, 2)] for item in chunk
             if min_freq_threshold / offset <= item[0] < offset * max_freq_threshold / offset]

    # Sort the chunk to find the most prominent frequencies
    chunk.sort(key=lambda x: x[1], reverse=True)
    chunk = chunk[:max_frequencies]

    return chunk


def write_output_to_file(
        chunks: list,
        max_frequencies: int,
        output_file: str
):
    # Format into channels
    channels = [[[], []] for _ in range(max_frequencies)]
    for chunk in chunks:
        for i, freq in enumerate(chunk):
            channels[i][0].append(freq[0])
            channels[i][1].append(freq[1])
    # Open file
    with open(output_file, 'w') as f:
        for i, channel in enumerate(channels):
            if not channel[0]:
                break
            # Format as a Desmos expression
            exp = r"\operatorname{tone}" + f"({channel[0]}[t], {channel[1]}[t]v)"
            f.write(exp + "\n")


def audio_to_desmos(
        audio_file: str,
        output_file: str,
        start_seconds: float = 0,
        end_seconds: float = 1,
        read_all: bool = False,
        samples_per_second: float = 30,
        max_frequencies: int = 250,
        min_freq_threshold: int = 20,
        max_freq_threshold: int = 20000,
        offset_octaves: int = 1
):
    # Load the audio to a wav format
    wav_file = load_audio(audio_file)

    # Read whole file
    if read_all:
        end_seconds = wav_file.getnframes() / wav_file.getframerate()

    # Get sample rate - kinda like audio fps
    sample_rate = wav_file.getframerate()

    # Determine the size of the "chunks" to perform fourier transform on
    chunk_size = int(sample_rate // samples_per_second)
    chunks = []

    # Read file to the start setting
    wav_file.readframes(int(sample_rate * start_seconds))

    # Loop through the wav file until end setting
    while wav_file.tell() < sample_rate * end_seconds:
        chunk = process_audio_chunk(
            wav_file,
            chunk_size,
            sample_rate,
            min_freq_threshold,
            max_freq_threshold,
            offset_octaves,
            max_frequencies)
        # Append the chunk to the list of chunks
        chunks.append(chunk)

    # Write to output file
    write_output_to_file(
        chunks,
        max_frequencies,
        output_file)

    # Print Desmos user settings
    print(f"Length:\t{len(chunks) + 1}")
    print(f"FPS:\t{samples_per_second}")
