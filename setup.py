import platform
import setuptools

# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib

# Linux
if platform.system() == 'Linux':
    path = 'linux/audresample.so'

# Windows
elif platform.system() == 'Windows':
    path = 'windows/audresample.dll'

# MacOS Intel
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'i386'
):
    path = 'macos-intel/libaudresample.dylib'

# MacOS M1
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'arm'
):
    path = 'macos-m1/libaudresample.dylib'

else:
    raise RuntimeError('Unsupported platform')


setuptools.setup(
    use_scm_version=True,
    packages=setuptools.find_packages(include=['audresample']),
    package_data={'audresample': [f'audresample/core/bin/{path}']},
)
