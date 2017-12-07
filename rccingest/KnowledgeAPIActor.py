import json
from os.path import join
import requests

class KnowledgeAPIActor(object):
    def __init__(self):
        # this NUST be a https since EZID API only allows sending authentication via basic authentication
        # leave this URL as-is. NEVER change it to http because if you do you are violating security policy!
        self.api_host = "https://knowledge.uchicago.edu/rest/"

    def post_data(self, identifier, post_data, username, password):
        url = join(self.api_host, identifier)
        auth_handler = requests.auth.HTTPBasicAuth(username, password)
        post_data_string = self._post_data_to_change_target(post_data).encode("utf-8")
        headers = {'Content-Type': 'text/plain'}
        resp = requests.post(url, data=post_data_string,
                             auth=auth_handler, headers=headers)
        if resp.status_code == 200:
            return 'Ok'
        else:
            return 'null'

    def get_items(self):
        url = self.api_host + "collections/48/items"
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text 
        else:
            return 'null'

    def search_for_an_item_by_title(self, title_string):
        data = self.get_items()
        out = []
        if data != "null":
            for n_thing in json.loads(data):
                if n_thing["name"] == title_string:
                    out.append(n_thing)
        return out
    
    def get_item_metadata(self, an_id):
        url = self.api_host + "items/" + str(an_id) + "/metadata"
        print(url)
        data = requests.get(url)
        print(data)
        if data != "null":
            return data.text 
        else:
            return []