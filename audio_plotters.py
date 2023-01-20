import numpy as np
from matplotlib import pyplot as plt

class AudioPlot:

    def __init__(self, Audio):
        self.audio = Audio

class SpectogramPlot:

    def __init__(self, Spectogram):
        self.spectogram = Spectogram

    def contours(self, colors, plot_size=[25,12], save=False, output_path=None):

        plt.figure(figsize=plot_size)
        plt.contourf(np.transpose(self.spectogram.spectogram), cmap=colors[0])
        plt.contour(np.transpose(self.spectogram.spectogram), cmap=colors[1], alpha=0.6)

        #plt.xlim([0, self.spectogram.spectogram.shape[0]-1])
        plt.axis('off')

        if output_path:
            plt.savefig(output_path)
        elif save:
            plt.savefig("output/" + self.spectogram.name + ".pdf")
