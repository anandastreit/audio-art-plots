import os
import numpy as np
import librosa
from scipy import signal
from audio_plotters import *
from signal_transform import *

class Audio:

    def __init__(self, input_path):

        self.input_path = input_path
        self.name = os.path.splitext(os.path.basename(input_path))[0]
        self.plot = AudioPlot(self)

    def load(self, mono='avg'):
        """
        mono options:
          'avg'        - average L+R channels (standard mono)
          'left'       - left channel only
          'right'      - right channel only
          'interleave' - interleave L and R samples [L0,R0,L1,R1,...] (produces unique visual artifacts)
        """
        samples, self.sample_rate = librosa.load(self.input_path, sr=None, mono=False)

        if samples.ndim == 1:
            self.samples = samples
        elif mono == 'avg':
            self.samples = samples.mean(axis=0)
        elif mono == 'left':
            self.samples = samples[0]
        elif mono == 'right':
            self.samples = samples[1]
        elif mono == 'interleave':
            self.samples = samples.T  # keep as (N, 2) — stft flattens it via np.append, replicating old scipy behavior

        print(f"Audio file loaded, sample rate: {self.sample_rate}")

    def resample(self, sample_rate): # number_of_samples=300000):

        audio_resampled = Audio(self.input_path)
        audio_resampled.sample_rate = sample_rate

        number_of_samples = round((len(self.samples) * sample_rate)/ self.sample_rate)
        audio_resampled.samples = signal.resample(self.samples, int(number_of_samples))
        print(f"Audio file resampled, old sample rate: {self.sample_rate}, new sample rate: {audio_resampled.sample_rate}")

        return audio_resampled

    def make_spectrogram(self, n_fft=2**10, factor_logscale=1.0):

        spec = stft(self.samples, n_fft)
        spec, freq = logscale_spec(spec, factor=factor_logscale, sr=self.sample_rate)
        spec = 20.*np.log10(np.abs(spec)/10e-6) # amplitude to decibel

        time_bins, freq_bins = np.shape(spec)
        print("time bins: ", time_bins)
        print("freq bins: ", freq_bins)

        spectrogram = Spectrogram(self.name, spec, freq)
        return spectrogram

class Spectrogram():

    def __init__(self, name=None, spectrogram=None, frequencies=None):
        self.name = name
        self.spectrogram = spectrogram
        self.frequencies = frequencies
        self.plot = SpectrogramPlot(self)
