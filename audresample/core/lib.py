import os
import ctypes


# load library

root = os.path.dirname(os.path.realpath(__file__))

bin_path = os.path.join(root, 'bin')
if os.name == 'nt':
    lib_path = os.path.join(bin_path, 'audresample.dll')  # pragma: no cover
else:
    lib_path = os.path.join(bin_path, 'libaudresample.so')  # pragma: no cover
lib = ctypes.cdll.LoadLibrary(lib_path)


# resample

class ConverterConfig(ctypes.Structure):
    _fields_ = [
        ("srIn", ctypes.c_double),
        ("srOut", ctypes.c_double),
        ("quality", ctypes.c_char),
    ]


lib.init_converter_config.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_char,
]
lib.init_converter_config.restype = ConverterConfig

lib.get_output_length.argtypes = [
    ctypes.c_size_t,
    ConverterConfig,
]
lib.get_output_length.restype = ctypes.c_size_t

lib.audresample_oneshot.argtypes = [
    ConverterConfig,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
]
lib.audresample_oneshot.restype = None

lib.do_mono_mixdown.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
    ctypes.c_uint,
]
lib.do_mono_mixdown.restype = None
