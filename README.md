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
1. run python setup.py install
1. make sure that the objects that you want to create SAF for are in a location that your user account is permitted to access
  - run
  ```bash/shell
  generate_safs -o [directory to put new SAF] [file that contains inventory of objects to put in a SAF] [extraction_config file] [crosswalk config file]
  ```
  - run
  ```bash/shell
    find_mamluk_files [root_directory_of_mamluk_objects] --yp [optional year of publication you want to restrict the inventory to]
  ```

## Quick start notes

- This objects directory should look like the following
  ```text/plain
    objects/
      file1/
        file.pdf
        file_DATA.xml
      file2/
        file2.pdf
        file2_DATA.xml
      file3/
        file3.pdf
        file3_DATA.xml
  ```
- See [etd_crosswalk.json](configs/etd_crosswalk.json) for an example of a crosswalk configuration
- See [etd_extraction_config.json](configs/etd_extraction_config.json) for an example of a crosswalk configuration


The extraction config should give the XPATH directions to find the value for each field you want to add to extract from the input metadata. The crosswalk config should define a SAF dublin_core element and qualifier attribute for each metadata field you want to include in the dublin_core metadata.

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

```text/plain
for f in `ls`
do
newdir=$(basename $f .zip)
mkdir $newdir
unzip $f -d $newdir
done
```

- at this point you can run the SAF generator on the directory using the spreadsheet given by head of disserations office to pick out the dissertations desired
