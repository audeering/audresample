===========
audresample
===========

|tests| |coverage| |docs| |python-versions| |license|

**audresample** remixes or resamples your signals.

Resampling is supported
for signals in single precision floating-point format,
and based on the `soxr`_ implementation
as provided by `audresamplelib`_.

Have a look at the installation_ and usage_ instructions.

.. code-block:: python

    >>> import numpy as np
    >>> import audresample
    >>> signal = np.zeros((2, 8000), dtype='float32')
    >>> signal.shape
    (2, 8000)
    >>> audresample.remix(signal, mixdown=True).shape
    (1, 8000)
    >>> audresample.remix(signal, channels=[0, 0, 1, 1]).shape
    (4, 8000)
    >>> audresample.resample(signal, 8000, 16000).shape
    (2, 16000)

.. _soxr: https://sourceforge.net/projects/soxr/
.. _audresamplelib: https://github.com/audeering/audresamplelib
.. _installation: https://audeering.github.io/audresample/install.html
.. _usage: https://audeering.github.io/audresample/usage.html


.. badges images and links:
.. |tests| image:: https://github.com/audeering/audresample/workflows/Test/badge.svg
    :target: https://github.com/audeering/audresample/actions?query=workflow%3ATest
    :alt: Test status
.. |coverage| image:: https://codecov.io/gh/audeering/audresample/branch/main/graph/badge.svg?token=NPQDJ5T7HI
    :target: https://codecov.io/gh/audeering/audresample/
    :alt: code coverage
.. |docs| image:: https://img.shields.io/pypi/v/audresample?label=docs
    :target: https://audeering.github.io/audresample/
    :alt: audresample's documentation
.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
    :target: https://github.com/audeering/audresample/blob/main/LICENSE
    :alt: audresample's MIT license
.. |python-versions| image:: https://img.shields.io/pypi/pyversions/audresample.svg
    :target: https://pypi.org/project/audresample/
    :alt: audresamples's supported Python versions
