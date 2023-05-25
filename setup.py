import os
import platform
import setuptools


# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib

binaries = {
    'manylinux_2_17_x86_64': 'linux/*.so',
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
        system = platform.system()
        processor = platform.processor()

        if system == 'Linux' and processor == 'x86_64':
            # That we support 2_17 can be seen
            # when inspecting the wheel with auditwheel
            plat_name = 'manylinux_2_17_x86_64'

        elif system == 'Windows':
            plat_name = 'win_amd64'

        elif system == 'Darwin' and processor == 'i386':
            plat_name = 'macosx_x86_64'

        elif system == 'Darwin' and processor == 'arm':
            plat_name = 'macosx_arm64'

        else:
            raise RuntimeError(
                f'Unsupported platform {system}-{processor}'
            )

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
