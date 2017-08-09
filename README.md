# README

## Background information 

- files are downloaded via a cron job to /data/projects/etd on hedwig.lib.uchicago.edu
- files downloaded are with the following pattern: ```etdadmin_upload_*.zip``` where the asterisk should be replaced with five numeric characters
- quarterly downloads happen in March, June, August/September and December
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
unzip $f
```
- at this point you can run the SAF generator on the directory using the spreadsheet given by head of disserations office to pick out the dissertations desired


# How To Use

1. unzip the ETD zip files that you want to convert to SAF into separate directories per dissertation

2. run the command line module pointing it at the location of all the dissertation directories

3. zip compress the directory called SimpleArchiveFormat

4. upload new zip file SimpleArchiveFormat.zip to knowledge.uchicago.edu
