#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-sas7bdat",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap-sas7bdat"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
        "singer-python",
        "pandas"
    ],
    entry_points="""
    [console_scripts]
    tap-sas7bdat=tap-sas7bdat:main
    """,
    packages=["tap-sas7bdat"],
    package_data = {
        "schemas": ["tap-sas7bdat/schemas/*.json"]
    },
    include_package_data=True,
)
