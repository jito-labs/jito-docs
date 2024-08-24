# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Jito Docs'
copyright = '2024, Jito Labs'
author = 'mdr0id'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx_fontawesome',
#    'sphinxemoji.sphinxemoji',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

myst_enable_extensions = [
    "deflist",
    "colon_fence",
    "substitution",
]

# Optional: Configure MyST to support more Sphinx-like syntax in Markdown


# -- Options for EPUB output
epub_show_urls = 'footnote'

html_css_files = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
]
