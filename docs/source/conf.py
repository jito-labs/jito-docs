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
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "smartquotes",
    "substitution",
    "tasklist",
    "attrs_inline",
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['../_static']
html_css_files = [
    'css/custom.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
]
html_images_path = ['../images']
html_static_path = ['../_static']

# Theme options
html_theme_options = {
    'style_nav_header_background': '#0a0a0a',
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'sticky_navigation': True,
}

# Logo configuration
html_logo = '../images/Jitolabs_Logo_White.png'
html_favicon = '../images/Jitolabs_Logo_White.png'

# Source configuration
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}
master_doc = 'index'

# Additional configurations
html_show_sourcelink = False
html_show_sphinx = False
html_copy_source = False

# Syntax highlighting
pygments_style = 'monokai'