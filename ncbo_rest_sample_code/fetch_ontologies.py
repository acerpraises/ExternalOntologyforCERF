import urllib.request, urllib.error, urllib.parse
import json
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = "87a6e825-e26c-4bd3-9ff8-508eae699720"

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def fetch_ontologies():
    # Get the available resources
    resources = get_json(REST_URL + "/")
    """Fetch the ontologies and return a dictionary with names as keys and IDs as values."""
    ontologies = get_json(resources["links"]["ontologies"])
    ontology_dict = {}
    for ontology in ontologies:
        ontology_dict[ontology['name']] = ontology['@id']
    return ontology_dict

