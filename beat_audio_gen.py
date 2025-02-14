import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
AMPLITUDE = 1
DURATION = 4

def define_wave(amplitude, frequency):
    return lambda t: amplitude * np.sin(2 * np.pi * frequency * t)

def basic_wave(freq, t):
    audio = define_wave(AMPLITUDE, freq)(t)
    return audio

def interference(freqs, t):
    return np.sum([define_wave(AMPLITUDE, freq)(t) for freq in freqs], axis=0)
    
def main():
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    
    # name = "wave240.wav"
    # audio = basic_wave(240, t)

    # name = "waves2beat.wav"
    # audio = interference([240, 242], t)
    
    # name = "waves3beat.wav"
    # audio = interference([240, 242, 244], t)

    # name = "waves5beat.wav"
    # audio = interference([240, 242, 244, 246, 248], t)

    # name = "waves20beat.wav"
    # audio = interference([240 + i for i in range(0, 40, 2)], t)

    # name = "waves50beat.wav"
    # audio = interference([240 + i for i in range(0, 100, 2)], t)
    
    name = "waves101beat.wav"
    audio = interference([240 + i for i in range(0, 202, 2)], t)

    write(name, SAMPLE_RATE, audio.astype(np.float32))

main()
