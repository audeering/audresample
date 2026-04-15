Usage
=====

.. plot::
    :context: reset
    :include-source: false

    import matplotlib.pyplot as plt
    import numpy as np


    def plot_signal(signal, sampling_rate):
        num_channels = signal.shape[0]
        num_samples = signal.shape[1]
        plt.rcParams["figure.figsize"] = [12, 2 * num_channels]
        t = np.linspace(0, num_samples / sampling_rate, num_samples)
        if num_channels > 1:
            fig, axs = plt.subplots(nrows=num_channels)
            for ax, channel in zip(axs, signal):
                ax.plot(t, channel)
                ax.set_xlabel("Time / s")
                ax.set_ylabel("Magnitude")
                ax.set_ylim([-1, 1])
        else:
            plt.plot(t, signal.squeeze())
            plt.xlabel("Time / s")
            plt.ylabel("Magnitude")
            plt.ylim([-1, 1])
        plt.tight_layout()


Remix signal
------------

Create AM/FM signal with three channels
and a sampling rate of 16kHz
using :meth:`audresample.am_fm_synth`.

.. plot::
    :context: close-figs

    >>> import audresample
    >>> sampling_rate = 16000
    >>> num_samples = 16500
    >>> num_channels = 3
    >>> signal = audresample.am_fm_synth(num_samples, num_channels, sampling_rate)
    >>> signal.shape
    (3, 16500)
    >>> plot_signal(signal, sampling_rate)

Mixdown signal to mono.

.. plot::
    :context: close-figs

    >>> mixed = audresample.remix(signal, mixdown=True)
    >>> mixed.shape
    (1, 16500)
    >>> plot_signal(mixed, sampling_rate)

Select the last channel.

.. plot::
    :context: close-figs

    >>> mixed = audresample.remix(signal, channels=-1)
    >>> mixed.shape
    (1, 16500)
    >>> plot_signal(mixed, sampling_rate)

Select the second and first channel.

.. plot::
    :context: close-figs

    >>> mixed = audresample.remix(signal, channels=[1, 0])
    >>> mixed.shape
    (2, 16500)
    >>> plot_signal(mixed, sampling_rate)

Mixdown first and second channel to mono.

.. plot::
    :context: close-figs

    >>> mixed = audresample.remix(signal, channels=[0, 1], mixdown=True)
    >>> mixed.shape
    (1, 16500)
    >>> plot_signal(mixed, sampling_rate)


Resample signal
---------------

Create AM/FM signal with two channels
and a sampling rate of 48kHz
using :meth:`audresample.am_fm_synth`.

.. plot::
    :context: close-figs

    >>> original_rate = 48000
    >>> num_original = 16000
    >>> num_channels = 2
    >>> signal = audresample.am_fm_synth(num_original, num_channels, original_rate)
    >>> signal.shape
    (2, 16000)
    >>> plot_signal(signal, original_rate)

Resample signal to 8kHz using
:meth:`audresample.resample`.

.. plot::
    :context: close-figs

    >>> target_rate = 8000
    >>> resampled = audresample.resample(signal, original_rate, target_rate)
    >>> resampled.shape
    (2, 2667)
    >>> plot_signal(resampled, target_rate)
