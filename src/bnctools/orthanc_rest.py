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

import httplib2
import json
import sys

from urllib.parse import urlencode

_credentials = None

class Orthanc
def _DecodeJson(s):
    try:
        if (sys.version_info >= (3, 0)):
            return json.loads(s.decode())
        else:
            return json.loads(s)
    except:
        return s


def SetCredentials(username, password):
    global _credentials
    _credentials = (username, password)

def _SetupCredentials(h):
    global _credentials
    if _credentials != None:
        h.add_credentials(_credentials[0], _credentials[1])

def _ComputeGetUri(uri, data):
    d = ''
    if len(data.keys()) > 0:
        d = '?' + urlencode(data)

    return uri + d
        
def DoGet(uri, data = {}, interpretAsJson = True):
    h = httplib2.Http()
    _SetupCredentials(h)
    resp, content = h.request(_ComputeGetUri(uri, data), 'GET')
    if not (resp.status in [ 200 ]):
        raise Exception(resp.status)
    elif not interpretAsJson:
        return content.decode()
    else:
        return _DecodeJson(content)


def DoRawGet(uri, data = {}):
    h = httplib2.Http()
    _SetupCredentials(h)
    resp, content = h.request(_ComputeGetUri(uri, data), 'GET')
    if not (resp.status in [ 200 ]):
        raise Exception(resp.status)
    else:
        return content


def _DoPutOrPost(uri, method, data, contentType):
    h = httplib2.Http()
    _SetupCredentials(h)

    if isinstance(data, str):
        body = data
        if len(contentType) != 0:
            headers = { 'content-type' : contentType }
        else:
            headers = { 'content-type' : 'text/plain' }
    else:
        body = json.dumps(data)
        headers = { 'content-type' : 'application/json' }
    
    resp, content = h.request(
        uri, method,
        body = body,
        headers = headers)

    if not (resp.status in [ 200, 302 ]):
        raise Exception(resp.status)
    else:
        return _DecodeJson(content)


def DoDelete(uri):
    h = httplib2.Http()
    _SetupCredentials(h)
    resp, content = h.request(uri, 'DELETE')

    if not (resp.status in [ 200 ]):
        raise Exception(resp.status)
    else:
        return _DecodeJson(content)


def DoPut(uri, data = {}, contentType = ''):
    return _DoPutOrPost(uri, 'PUT', data, contentType)


def DoPost(uri, data = {}, contentType = ''):
    return _DoPutOrPost(uri, 'POST', data, contentType)