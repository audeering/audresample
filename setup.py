import setuptools

from audresample.core.lib import platform_name


# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib
binaries = {
    'manylinux_2_17_x86_64': 'linux/*.so',
    'win_amd64': 'windows/*.dll',
    'macosx_12_0_x86_64': 'macos-intel/*.dylib',
    'macosx_12_0_arm64': 'macos-m1/*.dylib',
}
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
