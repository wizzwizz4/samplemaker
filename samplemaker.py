import math
import audioop
import random
import wave

import simpleaudio

sine = lambda a:math.sin(a * (2 * math.pi))
saw = lambda a:((2*a + 1) % 2) - 1
square = lambda a:1 if a%1 < 0.5 else -1
white = lambda a:random.uniform(-1, 1)

def sample(f, frequency=440, duration=1, volume=0.8,
           bytes_per_sample=2, sample_rate=44100):
    effective_frequency = frequency / sample_rate
    sample_count = duration * sample_rate
    vf = volume * 2 ** (8 * bytes_per_sample - 1)
    data = [int(vf * f(effective_frequency * i))
            for i in range(sample_count)]
    return b"".join(i.to_bytes(bytes_per_sample, "little", signed=True)
                    for i in data)

def play_from_buffer(buffer, bytes_per_sample=2, sample_rate=44100):
    simpleaudio.WaveObject(buffer,
                           num_channels=1,
                           bytes_per_sample=bytes_per_sample,
                           sample_rate=sample_rate).play()

def play(f, frequency=440, duration=1, volume=0.8,
         bytes_per_sample=2, sample_rate=44100):
    buffer = sample(f, frequency, duration, volume,
                    bytes_per_sample, sample_rate)
    play_from_buffer(buffer, bytes_per_sample, sample_rate)

def save_from_buffer(file, buffer, bytes_per_sample=2, sample_rate=44100):
    with wave.open(file, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(bytes_per_sample)
        f.setframerate(sample_rate)
        f.writeframes(buffer)

def save(file, f, frequency=440, duration=1, volume=0.8,
         bytes_per_sample=2, sample_rate=44100):
    buffer = sample(f, frequency, duration, volume,
                    bytes_per_sample, sample_rate)
    save_from_buffer(file, buffer, bytes_per_sample, sample_rate)
