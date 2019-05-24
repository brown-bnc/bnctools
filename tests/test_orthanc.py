#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pytest
import os
import shutil
import glob
from bnctools.orthanc_export import export_stable_study
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc


__author__ = "Isabel Restrepo"
__copyright__ = "Isabel Restrepo"
__license__ = "mit"


def test_export_stable_study():
    """Test exporting from Orthanc
    This tests assumes an instace of Orthanc running on http://localhost:8042/
    """

    study_id = "d3fc1b48-73ba3acd-30b5ff85-ea27fa65-e3550bf4"
    auth = HTTPBasicAuth("orthanc", "orthanc")
    outdir = "deleteme"
    orthanc = Orthanc("http://localhost:8042/", auth=auth)

    if os.path.exists(outdir):
        shutil.rmtree(outdir)

    export_stable_study(orthanc, study_id, outdir)

    files = glob.glob(outdir + "**/**/*.dcm", recursive=True)

    print (len(files))

    # assert

test_export_stable_study()