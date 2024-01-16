from setuptools import setup, find_packages
from pathlib import Path
import re

pkgname = "boring"
pubname = "boring_battery"

# Version info is set in one place; the {pkgname}/__init__.py file
__version__ = re.findall(
    r"""__version__ = [""]+([0-9\.\-dev]*)[""]+""",
    open(f"{pkgname}/__init__.py").read(),
)[0]

with open(Path(__file__).parent / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name=pubname,
    version=__version__,
    description="Battery Optimization Research. Integrated, Novel, Gradient-based",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "openmdao",
        "dymos",
        #"pyoptsparse", # install manually
        "matplotlib",
        "scipy",
        "pandas",
        "pyspice",
        "testflo",
        "openpyxl",
        "more_itertools",
    ],
    package_data={
    pkgname: [
        "XDSM/*.py",
        "XDSM/*.json",
        "XDSM/*/*.json",
    ]
    },

)
