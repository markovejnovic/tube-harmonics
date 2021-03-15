#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import Audio
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import tikzplotlib

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

tube_lengths = np.array([313, 296, 275, 255, 235, 215, 195, 175, 155, 135, 115, 95, 75]) * 1e-3
tube_length_err = 0.5 * 1e-3

for tube_length in tube_lengths:
    # Load the file.
    rate, audio = wavfile.read('Data/' + str(int(tube_length * 1e3)) + '.wav')
    audio_N = audio.shape[0]
    audio_len = audio_N / rate
    audio_norm = audio / np.max(audio)

    # Make a subplot
    fig, axs = plt.subplots(1,2)

    # Calculate the Fourier Transform and plot it, up to 3.5kHz
    freqs = rfftfreq(audio_N, 1 / rate)
    audio_ft = np.abs(rfft(audio_norm))
    axs[0].plot(freqs, audio_ft, label='Fourier Magnitude', linewidth=0.7)
    axs[0].set_xlim(0, 4500)
    axs[0].set_ylabel('Magnitude')
    axs[0].set_xlabel('Frequency [Hz]')

    # Normalize the Fourier Transform
    ft_norm = audio_ft / np.max(audio_ft)

    # Find peaks
    peaksi, _ = find_peaks(ft_norm, prominence=0.02, distance=800)
    peak_freqs = freqs[peaksi]
    peak_values = ft_norm[peaksi]
    axs[1].plot(freqs, ft_norm, label='Normalized Fourier Magnitude', linewidth=0.7)
    axs[1].plot(peak_freqs, peak_values, 'x', label='Peaks')
    axs[1].set_xlim(0, 4500)
    axs[1].set_ylabel('Normalized Magnitude')
    axs[1].set_xlabel('Frequency [Hz]')

    # Label plots
    #fig.suptitle('Peak Freqs for ' + str(int(tube_length * 1e3)) + 'mm')
    axs[0].set_title('Real Fourier Transform')
    axs[1].set_title('Normalized Fourier Transform w/ Peaks')
    axs[0].legend()
    axs[1].legend()
    fig.tight_layout()

    # Print out a table
    print('Peak Freqs for ' + str(int(tube_length * 1e3)) + '.wav (Hz):' + \
          str(np.round(peak_freqs, 2)))


    plt.show()

    plt.plot(freqs, ft_norm, label='Normalized Fourier Magnitude', linewidth=0.7)
    plt.plot(peak_freqs, peak_values, 'x', label='Peaks')
    plt.xlim(0, 4500)
    plt.ylabel('Normalized Magnitude')
    plt.xlabel('Frequency [Hz]')
    plt.legend()
    plt.tight_layout(pad=0)
    tikzplotlib.clean_figure()
    tikzplotlib.save('report/graphs/fourier-peaks/' + str(int(tube_length * 1e3)) + '.tex')
    plt.close()
