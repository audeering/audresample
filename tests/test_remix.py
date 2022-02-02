import ctypes
from glob import glob
from os import path

import pytest
import audiofile as af
import numpy as np

import audresample


def set_ones(signal, channels):
    signal[channels, :] = 1
    return signal


def mixdown(signal):
    signal = np.atleast_2d(signal)
    num_channels = signal.shape[0]
    if num_channels < 2:
        return signal
    else:
        num_samples = signal.shape[1]
        signal = signal.transpose().ravel()
        signal_mono = np.empty((1, num_samples), dtype=np.float32)
        # Mixdown like it is done in devAIce
        audresample.core.lib.lib.do_mono_mixdown(
            signal_mono.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            signal.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            int(num_samples),
            int(num_channels),
        )
        return np.atleast_2d(signal_mono)


@pytest.mark.parametrize(
    'signal, channels, mixdown, upmix, always_copy, expect',
    [
        # empty signal
        (
            np.zeros(0, dtype=np.float32),
            None,
            False,
            None,
            False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32),
            None,
            False,
            None,
            False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32),
            0,
            False,
            None,
            False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32),
            1,
            False,
            'repeat',
            False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32),
            1,
            False,
            'zeros',
            False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32),
            [0, 2],
            False,
            'zeros',
            False,
            np.zeros((2, 0), dtype=np.float32),
        ),
        # single channel
        (
            np.zeros((16000,), dtype=np.float64),
            None,
            False,
            None,
            False,
            np.zeros((1, 16000), dtype=np.float64),
        ),
        (
            np.zeros((1, 16000), np.float32),
            None,
            False,
            None,
            False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32),
            None,
            True,
            None,
            False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32),
            0,
            False,
            None,
            False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32),
            0,
            True,
            None,
            False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.ones((1, 16000), np.float32),
            0,
            True,
            'zeros',
            False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            np.ones((1, 16000), np.float32),
            1,
            True,
            'repeat',
            False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            np.ones((1, 16000), np.float32),
            1,
            True,
            'zeros',
            False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.ones((1, 16000), np.float32),
            -2,
            True,
            'zeros',
            False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            np.ones((1, 16000), np.float32),
            [0, 2],
            False,
            'zeros',
            False,
            np.concatenate(
                [
                    np.ones((1, 16000), dtype=np.float32),
                    np.zeros((1, 16000), dtype=np.float32),
                ]
            ),
        ),
        (
            np.ones((1, 16000), np.float32),
            [0, 2],
            True,
            'zeros',
            False,
            0.5 * np.ones((1, 16000), dtype=np.float32),
        ),
        # multiple channels
        (
            set_ones(np.zeros((4, 16000), np.float64), 2),
            2,
            False,
            None,
            False,
            np.ones((1, 16000), dtype=np.float64),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), -1),
            -1,
            False,
            None,
            False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [1, 3]),
            [1, 3],
            False,
            None,
            False,
            np.ones((2, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [0, 1, 2, 3]),
            [0, 1, 2, 3],
            False,
            None,
            False,
            np.ones((4, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [0, 1, 2]),
            range(3),
            False,
            None,
            False,
            np.ones((3, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((3, 16000), np.float32), 0),
            [1, 0, 0],
            False,
            None,
            False,
            set_ones(np.zeros((3, 16000), np.float32), [1, 2]),
        ),
        (
            set_ones(np.zeros((3, 16000), np.float32), 0),
            [3, 0, 0],
            False,
            'zeros',
            False,
            set_ones(np.zeros((3, 16000), np.float32), [1, 2]),
        ),
        (
            set_ones(np.zeros((3, 16000), np.float32), 0),
            [3, 0, 0],
            False,
            'repeat',
            False,
            np.ones((3, 16000), np.float32),
        ),
        (
            set_ones(np.zeros((3, 16000), np.float32), 0),
            [-6, 0, 0],
            False,
            'repeat',
            False,
            np.ones((3, 16000), np.float32),
        ),
        # multiple channels with mixdown
        (
            audresample.am_fm_synth(16000, 2, 16000),
            None,
            True,
            None,
            False,
            mixdown(audresample.am_fm_synth(16000, 2, 16000)),
        ),
        (
            np.zeros((3, 16000), dtype='float64'),
            None,
            True,
            None,
            False,
            np.zeros((1, 16000), dtype='float64'),
        ),
        (
            audresample.am_fm_synth(16000, 3, 16000),
            [0, 1],
            True,
            None,
            False,
            mixdown(audresample.am_fm_synth(16000, 2, 16000)),
        ),
        # always copy
        (
            np.zeros((1, 16000), dtype=np.float32),
            None,
            False,
            None,
            True,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), dtype=np.float64),
            None,
            False,
            None,
            True,
            np.zeros((1, 16000), dtype=np.float64),
        ),
        # wrong channel index
        pytest.param(
            np.zeros((2, 16000)),
            2,
            False,
            None,
            False,
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            np.zeros((2, 16000)),
            [0, 1, 2],
            False,
            None,
            False,
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        # wrong input shape
        pytest.param(
            np.zeros((16000, 2, 3)),
            None,
            False,
            None,
            False,
            None,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
        # wrong upmix type
        pytest.param(
            np.zeros((2, 16000)),
            2,
            False,
            'fancy',
            False,
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ]
)
def test_remix_signal(
        signal,
        channels,
        mixdown,
        upmix,
        always_copy,
        expect,
):
    result = audresample.remix(
        signal,
        channels,
        mixdown,
        upmix=upmix,
        always_copy=always_copy,
    )
    assert signal.dtype == expect.dtype
    np.testing.assert_equal(result, expect)
    if (
            signal.size > 0
            and channels is None
            and not mixdown
            and signal.ndim == 2
    ):
        if always_copy:
            assert id(signal) != id(result)
        else:
            assert id(signal) == id(result)
