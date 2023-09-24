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

# Get the available resources
resources = get_json(REST_URL + "/")

# Get the ontologies from the `ontologies` link
ontologies = get_json(resources["links"]["ontologies"])

# Get the name and ontology id from the returned list
ontology_output = []
for ontology in ontologies:
    ontology_output.append(f"{ontology['name']}\n{ontology['@id']}\n")
    
with open("list_ontologies_result.txt", "w", encoding="utf-8") as file:
    # Print the first ontology in the list
    file.write(",".join(map(str, ontologies[0])) + "\n")

    # Print the names and ids
    file.write("\n\n")
    for ont in ontology_output:
        file.write(ont)

