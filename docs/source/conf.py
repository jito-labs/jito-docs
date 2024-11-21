# Configuration file for the Sphinx documentation builder.
import os
import sys

# Add source directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# -- Project information
project = 'Jito Docs'
copyright = '2024, Jito Labs'
author = 'mdr0id'
release = '0.1'
version = '0.1.0'

# URL settings
set_url = 'https://docs.jito.wtf'

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
    'sphinx_sitemap',
    'sphinx_rtd_theme',
]

# MyST extensions
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

# SEO: Enable heading anchors
myst_heading_anchors = 3

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

# Build settings
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Theme settings
html_theme = "sphinx_rtd_theme"

# Add this line
toc_object_entries = True
toc_object_entries_show_parents = "all"

html_theme_options = {
    'navigation_depth': 6,
    'collapse_navigation': False,  # Don't collapse
    'sticky_navigation': True,
    'titles_only': False,         # Show full content
    'includehidden': True,
    'logo_only': True,
    'style_nav_header_background': '#0a0a0a',
}

# Logo configuration
html_logo = '../images/Jitolabs_Logo_White.png'
html_favicon = '../images/Jitolabs_Logo_White.png'

# Source configuration
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

# Root document settings
root_doc = 'index'
master_doc = 'index'

# Display settings
html_show_sourcelink = False
html_show_sphinx = False
html_copy_source = False
html_show_copyright = True

# SEO settings
html_title = "Jito Labs Documentation - High Performance Solana Infrastructure"
html_short_title = "Jito Docs"
html_baseurl = 'https://docs.jito.wtf'
html_use_opensearch = 'https://docs.jito.wtf'
sitemap_url_scheme = "{link}"

html_context = {
    'description': 'Official documentation for Jito Labs - Solana MEV, Block Engine, and high-performance infrastructure.',
    'keywords': 'solana, jito, mev, block engine, blockchain, trading, infrastructure',
    'og_description': 'Documentation for Jito Labs - High Performance Solana Infrastructure, Block Engine, and MEV Solutions',
    'og_type': 'website',
    'og_image': html_logo,
    'canonical_url': set_url,
}

# Language settings
language = 'en'
locale_dirs = ['locale/']
gettext_compact = False

# Code block settings
pygments_style = 'monokai'
html_codeblock_linenos_style = 'table'
html_scaled_image_link = False
html_last_updated_fmt = ''

# Basic URL settings
html_link_suffix = '.html'
html_file_suffix = '.html'
html_permalinks = True
html_permalink_builder = True
html_split_index = False
html_absolute_url = True
html_use_index = True
html_domain_indices = True

# SEO: Search engine directives
html_robots = {
    'index': True,
    'follow': True,
    'Archive': False,
}

# Important - add this
html_sidebars = {
    '**': [
        'globaltoc.html',
        'searchbox.html'
    ]
}