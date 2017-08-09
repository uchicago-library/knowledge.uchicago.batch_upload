from setuptools import setup

def _readme():
    with open("README.md", "r") as read_file:
        return read_file.read()

setup(
    name="safgeneration",
    description="A command-line script to generate Simple Archive Format directory for ingesting Proquest disseratations to a DSpace repository",
    long_description=_readme(),
    scripts = ['bin/saf-generation'],
)
