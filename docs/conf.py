import configparser
from datetime import date
import os
import subprocess


# Project -----------------------------------------------------------------

config = configparser.ConfigParser()
config.read(os.path.join('..', 'setup.cfg'))

# Project -----------------------------------------------------------------
author = config['metadata']['author']
copyright = f'2020-{date.today().year} audEERING GmbH'
project = config['metadata']['name']

# The x.y.z version read from tags
try:
    version = subprocess.check_output(['git', 'describe', '--tags',
                                       '--always'])
    version = version.decode().strip()
except Exception:
    version = '<unknown>'
title = '{} Documentation'.format(project)


# General -----------------------------------------------------------------

master_doc = 'index'
extensions = []
source_suffix = '.rst'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
pygments_style = None
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # support for Google-style docstrings
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'jupyter_sphinx',
]

napoleon_use_ivar = True  # List of class attributes
autodoc_inherit_docstrings = False  # disable docstring inheritance
autodoc_default_options = {
    'members': True,
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
}
# Disable Gitlab as we need to sign in
linkcheck_ignore = ['https://gitlab.audeering.com']

# Ignore package dependencies during building the docs
autodoc_mock_imports = [
    'numpy',
]

# HTML --------------------------------------------------------------------

html_theme = 'sphinx_audeering_theme'
html_theme_options = {
    'display_version': True,
    'logo_only': False,
    'footer_links': False,
}
html_context = {
    'display_github': True,
}
html_title = title
html_css_files = [
    'css/custom.css',
]
