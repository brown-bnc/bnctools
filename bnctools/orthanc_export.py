#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is Python console script to export DICOM files from an Orthanc instance.
The output directory structure is compatible with bidsfy

Example:
```
orthanc_export http://localhost:8042/ orthanc orthanc /dicom_export studyid
```
"""

import argparse
import sys
import logging
import time
import os
import os.path
import sys
import re
import json
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc

from bnctools import __version__

__author__ = "Isabel Restrepo"
__copyright__ = "CCV - Brown University"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def normalize_string(s):
    s = re.sub('[^a-zA-Z0-9-/-: ]', '_', s)
    s = s.replace(' ', '_')
    return s.lower()
    
def export_stable_study(orthanc, study_id, outdir):
    
    #retrieve study info
    study_json = orthanc.get_study(study_id)
    study_dicom_tags = study_json["MainDicomTags"]

    if not study_json["IsStable"]:
        print("Study NOT stable - retry later")
        return

    labname = study_dicom_tags["ReferringPhysicianName"]

    if labname == "":
        print("No Physician tag - Study is orphan")
        labname = "orphan"    

    series = study_json["Series"]
                                
    study_path =  normalize_string(outdir + '/' + labname + '/' + study_dicom_tags["StudyDate"] + '_' + study_dicom_tags["StudyDescription"])

    _logger.info("--------------------------------------------")
    _logger.info("Study Path " + study_path)
    _logger.info("--------------------------------------------")


    if not os.path.exists(study_path):
        os.makedirs(study_path)

    subject_dict = {}
    subject_id = 0

    for s in series:

        _logger.info("--------------------------------------------")
        _logger.info("Processing DICOM Series " + s)

        series_json = orthanc.get_one_series(s)
        series_dicom_tags = series_json["MainDicomTags"]
        instances = series_json["Instances"]


        for i in instances:
            instance_tags = orthanc.get_instance_simplified_tags(i)

            patient_name = normalize_string(instance_tags["PatientName"])
            
            if not (patient_name in subject_dict):
                subject_id = subject_id + 1
                subject_dict[patient_name] = format(subject_id, '03d')
            
            dicom_path = normalize_string(study_path + '/' + "sub-" + subject_dict[patient_name] )
                                                #    + '/' + "ses-" + series_dicom_tags["SeriesDescription"])
            
            if not os.path.exists(dicom_path):
                os.makedirs(dicom_path)

            filename = normalize_string(  series_dicom_tags["SeriesDescription"] + '-' 
                                        + 'series' + series_dicom_tags["SeriesNumber"] + '-'
                                        + 'instance' + instance_tags["InstanceNumber"] )
            _logger.debug("Dicom filename " + filename)

            dicom = orthanc.get_instance_file(i)
            # Write to the file
            f = open(dicom_path  + '/' + filename + '.dcm', 'wb')
            for chunk in dicom:
                f.write(chunk)
            f.close()

        _logger.info("--------------------------------------------")

    # save the subject dictionary to json
    with open(study_path + 'subject-dict.json', 'w') as fp:
        json.dump(subject_dict, fp, sort_keys=True, indent=4)



def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Export DICOMs in Orthanc Study to BIDS-ready directory structure ")
    parser.add_argument(
        '--version',
        action='version',
        version='bnctools {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="url",
        help="url of Orthanc server",
        type=str)
    parser.add_argument(
        dest="user",
        help="User for Orthanc server",
        type=str)
    parser.add_argument(
        dest="psswd",
        help="Password for Orthanc server",
        type=str)
    parser.add_argument(
        dest="outdir",
        help="Parent output directory",
        type=str)
    parser.add_argument(
        dest="study_id",
        help="Study ID",
        type=str)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    auth = HTTPBasicAuth(args.user, args.psswd)
    orthanc = Orthanc(args.url, auth=auth)
    export_stable_study(orthanc, args.study_id, args.outdir)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
