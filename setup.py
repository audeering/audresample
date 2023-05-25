import os
import platform
import setuptools

# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib

binaries = {
    'manylinux_x86_64': 'linux/*.so',
    'win_amd64': 'windows/*.dll',
    'macosx_x86_64': 'macos-intel/*.dylib',
    'macosx_arm64': 'macos-m1/*.dylib',
}


def platform_name():

    # Look for enrionment variable
    # to be able to enforce
    # different platform names
    # in CI on the same runner
    plat_name = os.environ.get('PLAT_NAME', None)

    if plat_name is None:

        # Extract platform name from system + processor
        systems = {
            'Linux': 'manylinux',
            'Windows': 'win',
            'Darwin': 'macos',
        }
        processors = {
            'i386': 'x86_64',
            'arm': 'arm64',
        }
        system = platform.system()
        if system not in systems:
            raise RuntimeError(f"Unsupported system '{system}'")
        processor = platform.processor()
        if processor not in processors:
            raise RuntimeError(f"Unsupported processor '{processor}'")
        plat_name = f'{system}_{processor}'

    return plat_name


plat_name = platform_name()

setuptools.setup(
    use_scm_version=True,
    packages=setuptools.find_packages(),
    package_data={
        'audresample.core': [f'bin/{binaries[plat_name]}']
    },
    # python -m build --wheel
    # does no longer accept the --plat-name option,
    # but we can set the desired platform as an option
    # (https://stackoverflow.com/a/75010995)
    options={
        'bdist_wheel': {'plat_name': plat_name},
    },
)
