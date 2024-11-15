# Configuration file for the Sphinx documentation builder.

# -- Project information
project = 'Jito Docs'
copyright = '2024, Jito Labs'
author = 'mdr0id'

release = '0.1'
version = '0.1.0'

# URL settings
set_url = 'https://docs.jito.wtf'

# Output options
html_output = '_build/html'

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
    'sphinx_sitemap',  # Added for SEO
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

# SEO: Enable heading anchors for better deep linking
myst_heading_anchors = 3

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['../../_static']  # Updated path
html_css_files = [
    'css/custom.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
]
html_images_path = ['../../images']  # Updated path

# SEO: Enhanced metadata
html_title = "Jito Labs Documentation - High Performance Solana Infrastructure"
html_short_title = "Jito Docs"
html_baseurl = set_url
html_use_opensearch = set_url
sitemap_url_scheme = "{link}"

# Theme options
html_theme_options = {
    'style_nav_header_background': '#0a0a0a',
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'sticky_navigation': True,
    'collapse_navigation': False,
    'navigation_depth': 4,
    'analytics_id': '',  # Add your Google Analytics ID
    'analytics_anonymize_ip': False,
}

# Logo configuration
html_logo = '../../images/Jitolabs_Logo_White.png'  # Updated path
html_favicon = '../../images/Jitolabs_Logo_White.png'  # Updated path

# Source configuration
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}
root_doc = 'index'
master_doc = 'index'

# Additional configurations
html_show_sourcelink = False
html_show_sphinx = False
html_copy_source = False

# Clean URLs
html_link_suffix = ''
html_file_suffix = '.html'
html_permalinks = True
html_permalink_builder = True
html_extra_path = ['robots.txt']

# URL handling
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

# Syntax highlighting
pygments_style = 'monokai'

# SEO: Better search engine handling
html_context = {
    'description': 'Official documentation for Jito Labs - Solana MEV, Block Engine, and high-performance infrastructure.',
    'keywords': 'solana, jito, mev, block engine, blockchain, trading, infrastructure',
    # Add Open Graph metadata here instead of theme options
    'og_description': 'Documentation for Jito Labs - High Performance Solana Infrastructure, Block Engine, and MEV Solutions',
    'og_type': 'website',
    'og_image': '../../images/Jitolabs_Logo_White.png',  # Updated path
    'canonical_url': set_url,
}

# Language settings
language = 'en'
locale_dirs = ['locale/']
gettext_compact = False

# Build settings
html_codeblock_linenos_style = 'table'
html_scaled_image_link = False
html_show_copyright = True
html_last_updated_fmt = ''

# Make sure epub title is set
epub_title = project
