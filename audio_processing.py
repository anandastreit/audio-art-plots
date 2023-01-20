import os
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
from audio_plotters import *
from signal_transform import *

class Audio:

    def __init__(self, input_path):

        self.input_path = input_path
        self.name = os.path.splitext(os.path.basename(input_path))[0]
        self.plot = AudioPlot(self)

    def load(self):

        self.sample_rate, self.samples = wav.read(self.input_path)
        print(f"Audio file loaded, sample rate: {self.sample_rate}")

    def resample(self, sample_rate): # number_of_samples=300000):

        audio_resampled = Audio(self.input_path)
        audio_resampled.sample_rate = sample_rate

        number_of_samples = round((len(self.samples) * sample_rate)/ self.sample_rate)
        audio_resampled.samples = signal.resample(self.samples, int(number_of_samples))
        print(f"Audio file resampled, old sample rate: {self.sample_rate}, new sample rate: {audio_resampled.sample_rate}")

        return audio_resampled

    def make_spectogram(self, bin_size=2**10, factor_logscale=1.0):

        spec = stft(self.samples, bin_size)
        spec, freq = logscale_spec(spec, factor=factor_logscale, sr=self.sample_rate)
        spec = 20.*np.log10(np.abs(spec)/10e-6) # amplitude to decibel

        time_bins, freq_bins = np.shape(spec)
        print("time bins: ", time_bins)
        print("freq bins: ", freq_bins)

        spectogram = Spectogram(self.name, spec, freq)
        return spectogram

class Spectogram():

    def __init__(self, name=None, spectogram=None, frequencies=None):
        self.name = name
        self.spectogram = spectogram
        self.frequencies = frequencies
        self.plot = SpectogramPlot(self)
