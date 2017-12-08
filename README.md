# README

## Introduction

This program is meant to be run on the command-line to generate a [SimpleArchiveFormat](https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format) (SAF) directory for exporting batches of items into a DSpace repository. It will takea  directory of objects where each object is a directory that contains a PDF file and some metadata record describing the object and convert the requested objects into a SAF for ingest into a DSpace repository.

## Constraints

- Requires input metadata be in XML format
- Requires each object to be a contained directory with the main file and the descriptive metadata file
- Requires the main file to be a PDF

## Quick start instructions

1. clone this repository
1. create a virtualenv on your system
1. activate the new virtualenv
1. cd into the cloned repo directory
1. run pip install -r requirements.txt
1. run python setup.py install
1. make sure that the objects that you want to create SAF for are in a location that your user account is permitted to access

## Available command-line scripts

1. ```find_mamluk_files``` will find the Mamluk Journal data fitting the defined filter value
1. ```find_dissertations``` will find the Proquest exported dissertation data for the dissertations in the spreadsheet inputted
1. ```index_dissertations``` will find ProQuest exported dissertations that are no in the index file pointed to
1. ```generate_safs``` which will generate a SimpleArchiveFormat directory where each item has some binary document file plus metadata required to be displayed in Knowledge@UChicago
1. ```modify_doi_locations``` will take a list of DOIs and modify the URL that those DOIs direct to
1. ```create_safs_of_only_metadata```will generate a SimpleArchiveFormat directory containing items that have only dublin_core.xml files


## Additional information

See the wiki for additional instructions for how to use advanced features of the tools.