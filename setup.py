import platform
import setuptools

# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib

# Linux
if platform.system() == 'Linux':
    path = 'linux/*.so'

# Windows
elif platform.system() == 'Windows':
    path = 'windows/*.dll'

# MacOS Intel
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'i386'
):
    path = 'macos-intel/*.dylib'

# MacOS M1
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'arm'
):
    path = 'macos-m1/*.dylib'

else:
    raise RuntimeError('Unsupported platform')


setuptools.setup(
    use_scm_version=True,
    packages=setuptools.find_packages(),
    package_data={'audresample.core': [f'bin/{path}']},
)
