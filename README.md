# audio-art-plots

## About
This project targets artists and data lovers who play with creativity when generating plots, even when the underlying data is limited. The aim is to represent data and its hidden patterns in an interesting and understandable way that appeals to the viewer's feelings.

## Current state
Possibilities of shapes and colors in audio spectrograms are explored by tuning parameters such as sampling rate, FFT window size, log frequency scale, and color maps. The result of these experiments has already generated artworks like the one below.

Supports MP3 and WAV files. Output can be saved as PDF or PNG at exact print dimensions (in cm), with margin and crop mark controls for framing.

Color tools allow exploring, trimming, and blending colormaps to create custom palettes for each piece.

<p align="center">
  <img src="https://github.com/anandastreit/audio-art-plots/blob/main/etc/athena.jpg" width="350" title="athena-pic">
</p>

## Parameters
- `sample_rate` — controls time resolution vs frequency range trade-off
- `n_fft` — FFT window size, controls frequency resolution
- `factor_logscale` — how aggressively to compress the frequency axis logarithmically
- `mono` — how stereo is handled: `avg`, `left`, `right`, or `interleave` (produces unique visual artifacts)

## Output
```python
song.load(mono='avg')
song_resampled = song.resample(sample_rate=2000)
song_resampled.make_spectrogram(n_fft=2**11, factor_logscale=1.5) \
    .plot(size_cm=[18, 13], margin_cm=2, dpi=300, save=True) \
    .contours([custom_cmap, 'viridis'])
```
