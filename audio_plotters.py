import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

class AudioPlot:

    def __init__(self, Audio):
        self.audio = Audio

class SpectrogramPlot:

    def __init__(self, Spectrogram):
        self.spectrogram = Spectrogram
        self.size = [25, 12]
        self.dpi = 150
        self.save = False
        self.output_path = None
        self.margin = 0
        self.margin_color = 'white'
        self.crop_marks = False
        self.filename = None
        self.format = 'pdf'

    def __call__(self, size=None, size_cm=None, dpi=None, save=None, output_path=None, filename=None, format='pdf', margin_cm=0, margin_color='white', crop_marks=False):
        if size_cm is not None: self.size = [size_cm[0] / 2.54, size_cm[1] / 2.54]
        elif size is not None: self.size = [size[0] / 2.54, size[1] / 2.54]
        if dpi is not None: self.dpi = dpi
        if save is not None: self.save = save
        if output_path is not None: self.output_path = output_path
        self.filename = filename
        self.format = format
        self.margin = margin_cm / 2.54
        self.margin_color = margin_color
        self.crop_marks = crop_marks
        return self

    def contours(self, colors, alpha=0.6, linewidths=1.0):

        data = np.transpose(self.spectrogram.spectrogram)
        w, h = self.size[0], self.size[1]
        plt.rcParams['savefig.pad_inches'] = 0
        fig = plt.figure(figsize=(w, h), dpi=self.dpi)

        mx, my = self.margin / w, self.margin / h

        if self.margin > 0:
            for rect in [
                (0, 0, mx, 1),           # left
                (1 - mx, 0, mx, 1),       # right
                (0, 0, 1, my),            # bottom
                (0, 1 - my, 1, my),       # top
            ]:
                fig.add_artist(Rectangle(rect[:2], rect[2], rect[3],
                    transform=fig.transFigure, facecolor=self.margin_color,
                    edgecolor='none', zorder=2))

        ax = fig.add_axes([mx, my, 1 - 2 * mx, 1 - 2 * my])
        ax.contourf(data, cmap=colors[0])
        ax.contour(data, cmap=colors[1], alpha=alpha, linewidths=linewidths)
        ax.axis('off')

        if self.crop_marks and self.margin > 0:
            tick = 0.05
            for x in [0, 1]:
                for y in [0, 1]:
                    dx = tick * (1 if x == 0 else -1)
                    dy = tick * (1 if y == 0 else -1)
                    fig.add_artist(plt.Line2D([x, x + dx], [y, y], color='black', linewidth=0.5, transform=fig.transFigure, clip_on=False))
                    fig.add_artist(plt.Line2D([x, x], [y, y + dy], color='black', linewidth=0.5, transform=fig.transFigure, clip_on=False))

        if self.output_path:
            fig.savefig(self.output_path, dpi=self.dpi, facecolor=self.margin_color, bbox_inches=None)
        elif self.save:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            name = self.filename or self.spectrogram.name
            fig.savefig(output_dir / f"{name}.{self.format}", dpi=self.dpi, facecolor=self.margin_color, bbox_inches=None)
