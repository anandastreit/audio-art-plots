import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

class AudioPlot:

    def __init__(self, Audio):
        self.audio = Audio

class SpectrogramPlot:

    def __init__(self, Spectrogram):
        self.spectrogram = Spectrogram

    def contours(self, colors, plot_size=None, save=False, output_path=None):

        plt.figure(figsize=plot_size or [25, 12])
        plt.contourf(np.transpose(self.spectrogram.spectrogram), cmap=colors[0])
        plt.contour(np.transpose(self.spectrogram.spectrogram), cmap=colors[1], alpha=0.6)

        #plt.xlim([0, self.spectogram.spectogram.shape[0]-1])
        plt.axis('off')

        if output_path:
            plt.savefig(output_path)
        elif save:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            plt.savefig(output_dir / (self.spectrogram.name + ".pdf"))
