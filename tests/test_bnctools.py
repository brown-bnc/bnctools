import os
import shutil
import glob
from bnctools.orthanc_export import export_stable_study
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc

from bnctools import __version__


def test_version():
    assert __version__ == '0.1.0'


def test_export_stable_study():
    """Test exporting from Orthanc
    This tests assumes an instace of Orthanc running on http://localhost:8042/
    """

    study_id = "0e16a034-87328dd8-ab6277ec-5c5658bd-4734b513"
    auth = HTTPBasicAuth("orthanc", "orthanc")
    outdir = "deleteme"
    orthanc = Orthanc("http://localhost:8042/", auth=auth)

    if os.path.exists(outdir):
        shutil.rmtree(outdir)

    export_stable_study(orthanc, study_id, outdir)

    files = glob.glob(outdir + "**/**/*.dcm", recursive=True)

    assert len(files) == 183