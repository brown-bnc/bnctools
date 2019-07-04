#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is Python console script to that starts a server to listen for actions 
such us dump DICOMs for an Orthanc Study convert to BIDS

Example:
```
orthanc_export http://localhost:8042/ orthanc orthanc /dicom_export studyid
```
"""

import logging
import argparse
import os
import sys
import glob
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# from json import dumps
# from flask.ext.jsonpify import jsonify
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc

from bnctools import __version__
from bnctools.orthanc_export import export_stable_study
from dotenv import load_dotenv

_logger = logging.getLogger(__name__)


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

class DICOM_Export(Resource):
    def __init__(self, orthanc_instance, dicom_outdir):
        self.orthanc_instance = orthanc_instance
        self.dicom_outdir = dicom_outdir

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('study_id', type=str)

        args = parser.parse_args()
        export_stable_study(self.orthanc_instance, args.study_id, self.dicom_outdir)

        files = glob.glob(self.dicom_outdir + "**/**/*.dcm", recursive=True)

        return {'nfiles': len(files)} 

# class BIDS_Export(Resource):
#     def __init__(self, dicom_dir):
#         self.dicom_dir = dicom_dir

#     def get(self, study_id):
#         conn = db_connect.connect()
#         query = conn.execute("select trackid, name, composer, unitprice from tracks;")
#         result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#         return jsonify(result)
        
app = Flask(__name__)
api = Api(app)

load_dotenv()
orthanc_url = os.environ['ORTHANC_URL']
user = os.environ['ORTHANC_USER']
psswd = os.environ['ORTHANC_PSSWD']
dicom_dir = os.environ['DICOM_DIR']
auth = HTTPBasicAuth(user, psswd)
orthanc = Orthanc(orthanc_url, auth=auth)
api.add_resource(DICOM_Export, '/dicom', resource_class_kwargs={'orthanc_instance': orthanc, 'dicom_outdir': dicom_dir}) 


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args = parse_args(args)
    setup_logging(args.loglevel)
  
    app.run(port='5002')


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()