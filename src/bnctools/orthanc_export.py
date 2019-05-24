#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = bnctools.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging
import time
import os
import os.path
import sys
import re
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc

from bnctools import __version__

__author__ = "Isabel Restrepo"
__copyright__ = "CCV - Brown University"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def normalize_path(s):
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
                                
    study_path =  normalize_path(outdir + '/' + labname + '/' + study_dicom_tags["StudyDate"] + '_' + study_dicom_tags["StudyDescription"])

    print("--------------------------------------------")
    print("Study Path " + study_path)
    print("--------------------------------------------")


    if not os.path.exists(study_path):
        os.makedirs(study_path)

    for s in series:

        print("--------------------------------------------")
        print("Processing DICOM Series " + s)

        series_json = orthanc.get_one_series(s)
        series_dicom_tags = series_json["MainDicomTags"]
        instances = series_json["Instances"]


        for i in instances[0:1]:
            instance_tags = orthanc.get_instance_simplified_tags(instances[0])

            dicom_path = normalize_path(study_path + '/' + "part-" + instance_tags["PatientName"] 
                                                   + '/' + "ses-" + series_dicom_tags["SeriesDescription"])
            
            if not os.path.exists(dicom_path):
                os.makedirs(dicom_path)

            print(".", end ="")


            dicom = orthanc.get_instance_file(i)
            # Write to the file
            f = open(dicom_path  + '/' + i + '.dcm', 'wb')
            for chunk in dicom:
                f.write(chunk)
            f.close()

        print("--------------------------------------------")



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
