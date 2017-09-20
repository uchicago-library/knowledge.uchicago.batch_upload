# README

## Introduction

This program is meant to be run on the command-line to generate a [SimpleArchiveFormat](https://wiki.duraspace.org/display/DSDOC6x/Importing+and+Exporting+Items+via+Simple+Archive+Format) directory for exporting batches of items into a DSpace repository. It will takea  directory of objects where each object is a dirctory that contains a PDF file and some metadata record describing the object and convert the requested objects into a SAF for ingest into a DSpace repository.

## Limitations

- Requires input metadata be in XML format
- Requires each object to be a contained directory with the main file and the descriptive metadata file
- Requires the main file to be a PDF

## Background information

- files are downloaded via a cron job to /data/projects/etd on hedwig.lib.uchicago.edu
- files downloaded are with the following pattern: ```etdadmin_upload_*.zip``` where the asterisk should be replaced with five numeric characters
- quarterly downloads happen in March, June, August/September and December
- downloads that happen in March contain Winter quarter dissertations; from December contain Autumn quarter dissertations; June contain Spring quarter dissertations; August/September contain Summer quarter dissertations
- files have the fllowing permissions rw-rw-r-- with owner:group etd:etd
- the directory /data/projects/etd have permissions drwxr-xr-x with owner:group etd:etd
  - this disallows repository staff from writing in that directory
- repository staff needs to copy the files into /data/repository/tr/dissertations_for_dspace/ directory on y2.lib.uchicago.edu
- before copying files create directory named for upload date. options are:
   - December [year of upload]
   - March [year of upload]
   - June [year of upload]
   - September|August [year of upload]
- must then unzip the zip files by logging into y2.lib.uchicago.edu and moving into the relevant directory to run the following script
```
for f in `ls`
do
newdir=$(basename $f .zip)
mkdir $newdir
unzip $f -d $newdir
done
```
- at this point you can run the SAF generator on the directory using the spreadsheet given by head of disserations office to pick out the dissertations desired

## Quickstart

- create virtual environment
- actvivate the new virtual environment
- git clone the repository
- cd into the new repo directory
- run ```python setup.py install```
- run saf-generation.py and follow instructions in the command-line stdout
