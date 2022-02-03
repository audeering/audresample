import ctypes
import typing

import numpy as np

from audresample.core import define
from audresample.core.config import config
from audresample.core.lib import lib


def _check_signal(
        signal: np.ndarray,
) -> np.ndarray:
    r"""Ensure float32 and two dimensions."""
    if signal.ndim > 2:
        raise RuntimeError(
            f"Input signal must have 1 or 2 dimension, "
            f"got {signal.ndim}."
        )
    return np.atleast_2d(signal)


def am_fm_synth(
        num_samples: int,
        num_channels: int,
        sampling_rate: int,
        *,
        dtype=np.float32,
) -> np.ndarray:
    r"""Synthesizes an AM/FM signal.

    Args:
        num_samples: number of samples
        num_channels: number of channels in the output signal
        sampling_rate: sampling rate in Hz
        dtype: data type

    Returns:
        signal with shape ``(number of channels, number of samples)``

    """
    g = 0.8  # gain
    g_am = 0.7  # amount of AM
    f_am = 2.5  # frequency of AM (Hz)
    f0 = 0.04 * sampling_rate  # carrier frequency (Hz)
    f_mod = 2  # modulator frequency (Hz)
    f_dev = f0 * 0.95  # frequency deviation (intensity of FM)
    omega_am = 2 * np.pi * f_am / sampling_rate
    omega0_car = 2 * np.pi * f0 / sampling_rate
    omega_mod = 2 * np.pi * f_mod / sampling_rate
    omega_dev = 2 * np.pi * f_dev / sampling_rate
    ph_fm = 0  # initial phase of FM oscillator
    ph_am = np.pi / 2  # initial phase of AM oscillator
    sig = np.zeros((num_channels, num_samples), dtype=dtype)
    for idx in range(num_channels):
        # No reinitialisation (to get true stereo)
        for t in range(num_samples):
            sig[idx, t] = g * np.cos(ph_fm)
            sig[idx, t] *= ((1 - g_am) + g_am * np.square(np.cos(ph_am)))
            ph_am += omega_am / 2
            ph_fm += omega0_car + omega_dev * np.cos(omega_mod * t)
    return sig


def remix(
        signal: np.ndarray,
        channels: typing.Union[int, typing.Sequence[int]] = None,
        mixdown: bool = False,
        *,
        upmix: str = None,
        always_copy: bool = False,
) -> np.ndarray:
    r"""Remix a signal.

    The ``channels`` arguments allows to select one or more
    channels and/or re-order them. Examples:

    ======== ===================================
    channels result
    ======== ===================================
    None     all channels
    0        first channel
    1        second channel
    -1       last channel
    -2       second last channel
    [0, 1]   first two channels
    [1, 0]   first two channels in swapped order
    [0, -1]  first and last channel
    [1, 1]   twice the second channel
    range(3) first three channels
    ======== ===================================

    If the input signal has not enough channels
    to fulfill the ``channels`` selection
    you can select an ``upmix`` method
    to fill in the missing channels.
    The workflow of :func:`audresample.remix` is always
    upmix -> channel selection -> downmix.

    The returned signal always of shape (``channels``, ``samples``).

    Args:
        signal: array with signal values
        channels: channel selection, see description
        mixdown: apply mono mix-down on selection
        upmix: if ``'zeros'`` it will pad missing channels with zeros,
            if ``'repeat'`` it will pad by repeating the existing channels
        always_copy: if ``True`` always returns a new object

    Returns:
        remixed signal with shape ``(number of channels, number of samples)``

    Raises:
        RuntimeError: if input signal has more than two dimensions
        ValueError: if channel selection is invalid and upmix is ``None``
        ValueError: if specified upmix method is not known

    """
    signal = _check_signal(signal)

    if channels is not None:
        if isinstance(channels, int):
            channels = [channels]
        max_channel = max(
            [
                max(channels) + 1,
                abs(min(channels)),  # we can have -1 entries
            ]
        )
        num_channels = signal.shape[0]
        if max_channel > num_channels:
            if upmix is None:
                raise ValueError(
                    f"Invalid channel selection {channels}, "
                    f"input signal has only {num_channels} channels.\n"
                    f"You can use the 'upmix' argument "
                    f"to increase available channels."
                )
            elif upmix == 'zeros':
                signal_ex = np.zeros(
                    (max_channel, signal.shape[1]),
                    dtype=signal.dtype,
                )
                signal_ex[:signal.shape[0], :] = signal
                signal = signal_ex
            elif upmix == 'repeat':
                # Upmix signal with [0, 1, 0, 1, ...]
                num_repetitions = int(np.ceil(max_channel / signal.shape[0]))
                signal_ex = np.concatenate([signal] * num_repetitions, axis=0)
                signal = signal_ex[:max_channel, :]
            else:
                raise ValueError(
                    f"Invalid upmix selection '{upmix}', "
                    f"has to be 'zeros', 'repeat', or None."
                )
        signal = np.atleast_2d(signal[channels, :])

    num_channels = signal.shape[0]
    if mixdown and num_channels > 1:
        return np.atleast_2d(np.mean(signal, axis=0))

    if always_copy:
        return signal.copy()
    else:
        return signal


def resample(
        signal: np.ndarray,
        original_rate: int,
        target_rate: int,
        *,
        quality: define.ResampleQuality = config.DEFAULT_RESAMPLE_QUALITY,
        always_copy: bool = False,
) -> np.ndarray:
    r"""Resample signal to a new sampling rate.

    Supports only signals in single precision floating point format.
    The returned signal is always of shape (``channels``, ``samples``).

    Args:
        signal: array with signal values
        original_rate: original sample rate of the input signal in Hz
        target_rate: target sampling rate in Hz
        quality: quality of the conversion algorithm
        always_copy: if ``True`` always returns a new object

    Returns:
        resampled signal with shape ``(number of channels, number of samples)``

    Raises:
        RuntimeError: if input signal has more than two dimensions
        RuntimeError: if input type is not :class:`numpy.single`

    """
    signal = _check_signal(signal)

    # We can only handle float32 signals
    if signal.dtype != np.float32:
        raise RuntimeError(
            'Input signal must be of type float32/single, '
            f'got {signal.dtype}.'
        )

    if original_rate == target_rate or signal.size == 0:
        if always_copy:
            return signal.copy()
        else:
            return signal

    converter_config = lib.init_converter_config(
        float(original_rate), float(target_rate), ord(quality),
    )

    channels = signal.shape[0]
    num_in = signal.shape[1]
    num_out = lib.get_output_length(num_in, converter_config)

    target = np.empty((channels, num_out), dtype=np.float32)
    for x, y in zip(signal, target):
        # as a side-effect of storing channel first
        # we need to flatten the channel in memory
        x = x.ravel()
        signal_in_p = x.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        signal_out_p = y.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        lib.audresample_oneshot(
            converter_config, signal_in_p, num_in, signal_out_p, num_out,
        )

    return target
