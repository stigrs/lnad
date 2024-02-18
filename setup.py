# Copyright (c) 2024 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="lnad",
    version="0.1.0",
    author="Stig Rune Sellevag",
    author_email="stig-rune.sellevag@ffi.no",
    license="MIT License",
    description="Library for network analysis and dismantling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stigrs/lnad.git",
    packages=setuptools.find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
