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
    return np.atleast_2d(np.mean(signal, axis=0))


@pytest.mark.parametrize(
    'signal, channels, mixdown, always_copy, expect',
    [
        # empty signal
        (
            np.zeros(0, dtype=np.float32), None, False, False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        (
            np.zeros((1, 0), dtype=np.float32), None, False, False,
            np.zeros((1, 0), dtype=np.float32),
        ),
        # single channel
        (
            np.zeros((16000,)), None, False, False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32), None, False, False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32), None, True, False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32), 0, False, False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        (
            np.zeros((1, 16000), np.float32), 0, True, False,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        # multiple channels
        (
            set_ones(np.zeros((4, 16000), np.float32), 2), 2, False, False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), -1), -1, False, False,
            np.ones((1, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [1, 3]),
            [1, 3], False, False,
            np.ones((2, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [0, 1, 2, 3]),
            [0, 1, 2, 3], False, False,
            np.ones((4, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((4, 16000), np.float32), [0, 1, 2]),
            range(3), False, False,
            np.ones((3, 16000), dtype=np.float32),
        ),
        (
            set_ones(np.zeros((3, 16000), np.float32), 0),
            [1, 0, 0], False, False,
            set_ones(np.zeros((3, 16000), np.float32), [1, 2]),
        ),
        # multiple channels with mixdown
        (
            audresample.am_fm_synth(16000, 2, 16000), None, True, False,
            mixdown(audresample.am_fm_synth(16000, 2, 16000)),
        ),
        (
            audresample.am_fm_synth(16000, 3, 16000), [0, 1], True, False,
            mixdown(audresample.am_fm_synth(16000, 2, 16000)),
        ),
        # always copy
        (
            np.zeros((1, 16000), dtype=np.float32), None, False, True,
            np.zeros((1, 16000), dtype=np.float32),
        ),
        # wrong channel index
        pytest.param(
            np.zeros((2, 16000)), 2, False, False, None,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
        pytest.param(
            np.zeros((2, 16000)), [0, 1, 2], False, False, None,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
        # wrong input shape
        pytest.param(
            np.zeros((16000, 2, 3)), None, False, False, None,
            marks=pytest.mark.xfail(raises=RuntimeError),
        )
    ]
)
def test_resample_signal(signal, channels, mixdown, always_copy, expect):
    result = audresample.remix(
        signal, channels, mixdown, always_copy=always_copy,
    )
    np.testing.assert_equal(result, expect)
    if signal.size > 0 and\
            channels is None and\
            not mixdown and\
            signal.dtype == np.float32:
        if always_copy:
            assert id(signal) != id(result)
        else:
            assert id(signal) == id(result)
