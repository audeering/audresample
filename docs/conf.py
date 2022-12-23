import configparser
from datetime import date
import os
import shutil

import audeer


config = configparser.ConfigParser()
config.read(os.path.join('..', 'setup.cfg'))


# Project -----------------------------------------------------------------
author = config['metadata']['author']
copyright = f'2020-{date.today().year} audEERING GmbH'
project = config['metadata']['name']
version = audeer.git_repo_version()
title = 'Documentation'


# General -----------------------------------------------------------------

master_doc = 'index'
extensions = []
source_suffix = '.rst'
exclude_patterns = [
    'build',
    'tests',
    'Thumbs.db',
    '.DS_Store',
    'api-src',
]
templates_path = ['_templates']
pygments_style = None
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # support for Google-style docstrings
    'sphinx.ext.autosummary',
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

# Disable auto-generation of TOC entries in the API
# https://github.com/sphinx-doc/sphinx/issues/6316
toc_object_entries = False


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


# Copy API (sub-)module RST files to docs/api/ folder ---------------------
audeer.rmdir('api')
audeer.mkdir('api')
api_src_files = audeer.list_file_names('api-src')
api_dst_files = [
    audeer.path('api', os.path.basename(src_file))
    for src_file in api_src_files
]
for src_file, dst_file in zip(api_src_files, api_dst_files):
    shutil.copyfile(src_file, dst_file)
