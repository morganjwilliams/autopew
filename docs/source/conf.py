import re
import sys
from datetime import date

import autopew

# -- Project information -----------------------------------------------------

project = "autopew"
copyright = f"2019-{date.today().year}, Morgan Williams & Louise Schoneveld"
author = "Morgan Williams & Louise Schoneveld"

version = re.findall(r"^[\d]*.[\d]*.[\d]*", autopew.__version__)[0]
release = version


extensions = [
    "sphinx_book_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",  # generates sourcecode on docs site, with reverse links to docs
    "myst_parser",
]
autosummary_generate = True
autodoc_member_order = "bysource"
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

source_suffix = ".rst"

master_doc = "index"
language = "en"

exclude_patterns = []

pygments_style = "sphinx"
todo_include_todos = True

myst_enable_extensions = ["colon_fence", "html_image", "attrs_inline"]

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]

# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": "https://github.com/morganjwilliams/autopew",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_fullscreen_button": False,
    "toc_title": "Sections",
    "show_navbar_depth": 2,
}
html_static_path = ["_static"]


html_context = {
    "display_github": True,  # Integrate GitHub
    "last_updated": True,
    "github_user": "morganjwilliams",  # Username
    "github_repo": "autopew",  # Repo name
    "github_version": "develop",  # Version
    "conf_py_path": "/docs/source/",  # Path in the checkout to the docs root
}


html_title = "autopew"


root_doc = "index"
latex_documents = [
    (
        root_doc,
        "autopew.tex",
        "autopew Documentation",
        r"Morgan Williams \& Louise Schoneveld",
        "manual",
    )
]

texinfo_documents = [
    (
        master_doc,
        "autopew",
        "autopew Documentation",
        author,
        "autopew",
        "One line description of project.",
        "Science/Research",
    )
]

# -- intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}


github_doc_root = "https://github.com/morganjwilliams/autopew/tree/develop/docs/"

epub_title = project

epub_exclude_files = ["search.html"]

if sys.platform.lower().startswith("linux"):
    latex_engine = "lualatex"  # use lualatex for unicode pdf generation


def setup(app):
    import shutil
    from pathlib import Path

    if Path(app.doctreedir).exists():
        shutil.rmtree(app.doctreedir)
