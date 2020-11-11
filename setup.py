"""
Setup file for setuptools
"""
import codecs
import os
import re

from setuptools import find_packages, setup


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


###################################################################

NAME = "simago"
PACKAGES = find_packages(where="simago")
META_PATH = os.path.join("simago", "__init__.py")
KEYWORDS = ["simulation", "open data"]
PROJECT_URLS = {
    "Documentation": "https://simago.readthedocs.io/en/latest",
    "Source Code": "https://github.com/alexanderharms/Simago/"
}
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering"
]
INSTALL_REQUIRES = ["wheel", "numpy", "scipy", "pandas", "pyYAML"]

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))
META_FILE = read(META_PATH)


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        project_urls=PROJECT_URLS,
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        long_description_content_type="text/x-rst",
        packages=PACKAGES,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
    )
