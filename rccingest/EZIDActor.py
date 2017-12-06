"""
"""
import base64
from os.path import join
import requests

class EZIDActor(object):
    def __init__(self):
        self.api_host = "https://ezid.cdlib.org/id/"

    def post_data(self, identifier, post_data, username, password):
        url = join(self.api_host, identifier)
        auth_handler = requests.auth.HTTPBasicAuth(username, password)
        post_data_string = self._post_data_to_change_target(post_data).encode("utf-8")
        resp = requests.post(url, data=post_data_string, auth=auth_handler)
        if resp.status == 200:
            return 'Ok'
        else:
            return 'null'

    def get_data(self, identifier):
        url = join(self.api_host, identifier)
        resp = requests.post(url)
        if resp.status == 200:
            return resp.text 
        else:
            return 'null'

    def _post_data_to_change_target(self, new_location):
        request_string = "_target: {}".format(new_location)
        return request_string

