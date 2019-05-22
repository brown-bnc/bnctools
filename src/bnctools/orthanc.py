'''
Filename: bnctools/src/bnctools/orthanc.py
Created Date: Wednesday, May 22nd 2019, 11:07:01 am
Author: mrestrep

Copyright (c) 2019 CVV
'''

class OrthancServer:
    def __init__(self, url, username, password):
        self.url = url
        self.credentials = (username, password)

    def compute_get_uri(self, path, data):
        d = ''
        if len(data.keys()) > 0:
            d = '?' + urlencode(data)

        return self.url + '/' + uri + d


    def get(self, path, data, as_json = True):
        h = httplib2.Http()
        h.add_credentials(self.credentials[0], self.credentials[1])
        
        resp, content = h.request(compute_get_uri(path, data), 'GET')
        if not (resp.status in [ 200 ]):
            raise Exception(resp.status)
        elif as_json:
            return json.loads(s.decode())
        else:
            return content.decode()

#     def export_study(self, study_id):
        


# class OrthancStudy:
#     def __init__(self, study_id):
#         self.id = study_id

