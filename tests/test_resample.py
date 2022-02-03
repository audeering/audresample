from glob import glob
from os import path

import pytest
import audiofile as af
import numpy as np

import audresample

resampled_wavs = glob('tests/test-assets/resampled__*.wav')


@pytest.mark.parametrize(
    'signal, original_rate, target_rate, always_copy',
    [
        # empty signal
        (
            np.zeros(0, dtype=np.float32), 16000, 8000, False,
        ),
        (
            np.zeros((1, 0), dtype=np.float32), 16000, 8000, False,
        ),
        # original_rate == target_rate without copy
        (
            np.zeros((16000,), dtype=np.float32), 16000, 16000, False,
        ),
        (
            np.zeros((16000, 1), dtype=np.float32), 16000, 16000, False,
        ),
        (
            np.zeros((16000, 3), dtype=np.float32), 16000, 16000, False,
        ),
        # original_rate == target_rate with copy
        (
            np.zeros((16000,), dtype=np.float32), 16000, 16000, True,
        ),
        (
            np.zeros((16000, 1), dtype=np.float32), 16000, 16000, True,
        ),
        (
            np.zeros((16000, 3), dtype=np.float32), 16000, 16000, True,
        ),
        # original_rate != target_rate
        (
            np.zeros((16000,), dtype=np.float32), 16000, 8000, False,
        ),
        (
            np.zeros((16000, 1), dtype=np.float32), 16000, 8000, False,
        ),
        (
            np.zeros((16000, 3), dtype=np.float32), 16000, 8000, False,
        ),
        (
            audresample.am_fm_synth(16000, 2, 16000), 16000, 8000, False,
        ),
        # wrong input shape
        pytest.param(
            np.zeros((16000, 2, 3)), 16000, 16000, False,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
        # wrong input datatype
        pytest.param(
            np.zeros((16000,), dtype=np.float64), 16000, 16000, False,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
        pytest.param(
            np.zeros((16000,), dtype=int), 16000, 16000, False,
            marks=pytest.mark.xfail(raises=RuntimeError),
        ),
    ]
)
def test_resample_signal(signal, original_rate, target_rate, always_copy):
    y = audresample.resample(
        signal, original_rate, target_rate, always_copy=always_copy,
    )
    assert y.ndim == 2
    assert y.dtype == np.float32
    if original_rate == target_rate and \
            signal.dtype == np.float32 and \
            signal.ndim == 2:
        if always_copy:
            assert id(signal) != id(y)
        else:
            assert id(signal) == id(y)


@pytest.mark.parametrize(
    'resampled_wav', resampled_wavs
)
def test_resample_file(resampled_wav):

    identifiers = path.splitext(path.basename(resampled_wav))[0].split('__')

    sr_in = int(identifiers[1].split('_')[-1])
    sr_out = int(identifiers[2].split('_')[-1])
    n_ch = int(identifiers[3].split('_')[-1])
    wav_in = f'tests/test-assets/original__sr_{sr_in}__channels_{n_ch}.wav'

    x, sr = af.read(wav_in, always_2d=True)
    assert sr == sr_in

    target, sr = af.read(resampled_wav, always_2d=True)
    assert sr == sr_out

    y = audresample.resample(
        x, sr_in, sr_out, quality=audresample.define.ResampleQuality.HIGH,
    )
    assert y.shape[0] == n_ch

    np.testing.assert_allclose(y, target, rtol=0.0, atol=0.037)

    errors = np.abs(np.ravel(y) - np.ravel(target))
    mean_error = np.mean(errors)
    assert mean_error < 5.0e-5

    outliers = errors[errors > 1.0e-3]
    assert outliers.size / errors.size < 1.0e-3
