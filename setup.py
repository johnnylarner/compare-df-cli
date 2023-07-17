import os
import shutil
import subprocess
import sys
from distutils.cmd import Command
from pathlib import Path
from runpy import run_path

from setuptools import find_packages, setup

# read the program version from version.py (without loading the module)
__version__ = run_path("src/compare_df_cli/version.py")["__version__"]


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_install_requires() -> list[str]:
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / "requirements.txt"
    targets = []
    if fname.exists():
        with open(fname, "r") as f:
            targets = f.read().splitlines()
    return targets


setup(
    name="compare-df-cli",
    version=__version__,
    author="James Richardson",
    author_email="james.richardson.2556@gmail.com",
    description="Small CLI tool designed to compare polars dataframes",
    license="proprietary",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"compare_df_cli": ["res/*"]},
    long_description=read("README.md"),
    install_requires=get_install_requires(),
    tests_require=[
        "pytest",
        "pytest-cov",
        "pre-commit",
    ],
    platforms="any",
    python_requires=">=3.7",
)
