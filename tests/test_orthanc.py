#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from bnctools.orthanc import OrthancServer
from pathlib import Path  
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc


__author__ = "Isabel Restrepo"
__copyright__ = "Isabel Restrepo"
__license__ = "mit"

# #load .env file
# env_path = Path('../../') / '.env'
# load_dotenv(dotenv_path=env_path)
auth = HTTPBasicAuth("orthanc", "orthanc")
out_dir = "~/deleteme"
orthanc = Orthanc("http://localhost:8042/", auth=auth)
study_id = "d3fc1b48-73ba3acd-30b5ff85-ea27fa65-e3550bf4"
study_json = orthanc.get_study(study_id)
study_dicom_tags = study_json["MainDicomTags"]

if not study_json["IsStable"]
    print("Study NOT stable - retry later")
    return

labname = main_dicom_tags["ReferringPhysicianName"]

if labname == "":
    print("Study is orphan")
    labname = "orphan"    

series = study_json["Series"]
                             
study_path =  out_dir + '/' + study_dicom_tags["StudyDate"] + study_dicom_tags["StudyDescription"]

if not os.path.exists(study_path):
    os.makedirs(study_path)

for s in series:

    print("--------------------------------------------")
    print("Processing DICOM Series " + s)
    print("--------------------------------------------")

    series_tags = orthanc.get_one_series(s)
    instances = series_tags["Instances"]

    for i in instances:
        instance_tags = orthanc.get_instance_simplified_tags(instances[0])

        dicom_path = study_path + '/' + "sub-" + instance_tags["PatientName"] 
                                + '/' + "ses-" + series_tags["SeriesDescription"]
        
        if not os.path.exists(study_path):
            os.makedirs(study_path)

        # dicom = orthanc.get_instance_file(i)
        # # Write to the file
        # f = open(series_path  + '/' + '.dcm', 'wb'))
        # f.write(dicom)
        # f.close()


    

{'ID': 'd3fc1b48-73ba3acd-30b5ff85-ea27fa65-e3550bf4', 'IsStable': True, 'LastUpdate': '20190501T172956', 'MainDicomTags': {'AccessionNumber': '', 'InstitutionName': 'BROWN UNIVERSITY MRF', 'ReferringPhysicianName': '', 'StudyDate': '20190328', 'StudyDescription': 'MRF^Daily QA', 'StudyID': '1', 'StudyInstanceUID': '1.3.12.2.1107.5.2.43.67050.30000019031314111234400000184', 'StudyTime': '122934.099000'}, 'ParentPatient': '4bf75716-f1e6f4a6-a5a582d4-c5748d78-7b8f9edb', 'PatientMainDicomTags': {'PatientBirthDate': '19500101', 'PatientID': 'JACKHAMMER_QA', 'PatientName': 'JACKHAMMER_QA', 'PatientSex': 'O'}, 'Series': ['b5931257-e7295320-77429a04-841dafbc-6bf8037d', '499edd1f-7ad20a64-04512efe-3f50f204-9fdfe117', 'e4c92ea8-95adb53d-3d005dd2-13e76ffb-b0b38757', '904f6941-96dfd3f6-3ca9997b-79015997-b2a3fd86', 'f809cce9-f9647b03-8b218be7-42fe82b0-768733f6'], 'Type': 'Study'}

# def test_orthanc_connection():
#     assert fib(1) == 1
#     assert fib(2) == 1
#     assert fib(7) == 13
#     with pytest.raises(AssertionError):
#         fib(-10)
