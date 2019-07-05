========
bnctools
========


Tools developed by the Behavioral Neuroimaging Center at Brown university to support
distrubution and pre-processing of Neuroimaging data.

##Installation

We develop and encourage the use of [poetry](https://poetry.eustace.io) for package installation and management.

To start a new project with **poetry**
```
mkdir mynewproject
cd mynewproject
poetry init
```


To install using **poetry** run

```
poetry add bnctools --git https://github.com/brown-bnc/bnctools.git
```

##DICOM Export

The BNC has set up a DICOM listener where all data from the scanner is sent to after collection.
The listener is an ORTHANC server that manages data in its own database. For convinience, upon receipt the listener dumps all data to a bnc-managed folder in `files.brown.edu`.

The export is performed by the `orthanc_export` script intalled as part of bnc_tools

An example of running the script is given below:

To activate your project's environment

```
cd mynewproject
poetry shell 
```

```
orthanc_export http://localhost:8042/ orthanc orthanc dicom_export d3fc1b48-73ba3acd-30b5ff85-ea27fa65-e3550bf4
```