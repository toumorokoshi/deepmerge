#!/usr/bin/env python
import os
import sys

is_release = False
if "--release" in sys.argv:
    sys.argv.remove("--release")
    is_release = True
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = []

tests_require = []

setup(
    name="deepmerge",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="a toolset to deeply merge python dictionaries.",
    long_description=open(README_PATH).read(),
    author="Yusuke Tsutsumi",
    author_email="yusuke@tsutsumi.io",
    url="http://deepmerge.readthedocs.io/en/latest/",
    packages=find_packages(exclude=["tests*", "*.tests*"]),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    tests_require=tests_require,
)
