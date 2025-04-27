#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-line-counter",
    version="1.1.0",
    author="Mahmoud Ashraf",
    author_email="ashrafhoda03@gmail.com",
    description="A tool to count lines of code while ignoring comments and empty lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SNO7E-G/Code-Line-Counter",
    project_urls={
        "Bug Tracker": "https://github.com/SNO7E-G/Code-Line-Counter/issues",
        "Source": "https://github.com/SNO7E-G/Code-Line-Counter",
        "Documentation": "https://github.com/SNO7E-G/Code-Line-Counter/blob/main/README.md",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="code, lines, counter, comments, blank, analyzer, development, statistics",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "code-counter=code_counter:main",
        ],
    },
) 