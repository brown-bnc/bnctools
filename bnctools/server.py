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

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify
from requests.auth import HTTPBasicAuth
from orthanc_rest_client import Orthanc

from bnctools import __version__

__author__ = "Isabel Restrepo"
__copyright__ = "CCV - Brown University"
__license__ = "mit"

_logger = logging.getLogger(__name__)

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class DICOM_Export(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

# class Employees_Name(Resource):
#     def get(self, employee_id):
#         conn = db_connect.connect()
#         query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
#         result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#         return jsonify(result)
        

api.add_resource(DICOM_Export, '/dicom') # Route_1
api.add_resource(BIDS_Export, '/bids') # Route_2


if __name__ == '__main__':
    auth = HTTPBasicAuth(args.user, args.psswd)
    orthanc = Orthanc(args.url, auth=auth)
    export_stable_study(orthanc, args.study_id, args.outdir)

    app.run(port='5002')