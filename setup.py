from os.path import exists
from setuptools import setup, find_packages

def _readme():
    if exists("readme.md"):
        with open("README.md", "r", encoding="utf-8") as read_file:
            return read_file.read()
    else:
        return "no long description written"

setup(
    name="safGeneration",
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    version="2.0.0",
    description="A set of tools for UChicago librarians to use to add material to knowledge.uchicago.edu",
    long_description=_readme(),
    keywords="python3.5 SimpleArchiveFormat generation csv proquest",
    packages=find_packages(),
    entry_points={
         'console_scripts': [
             'find_mamluk_files = safgeneration.findingMamlukFiles.__main__:main',
             'generate_safs = safgeneration.generatingSAFS.__main__:main'
         ]
    },
    license="LGPL3.0",
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
