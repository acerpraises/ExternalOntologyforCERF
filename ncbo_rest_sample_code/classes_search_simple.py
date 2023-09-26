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

# Get list of search terms
path = os.path.join(os.path.dirname(__file__), 'classes_search_simple_terms.txt')
terms_file = open(path, "r")
terms = []
for line in terms_file:
    terms.append(line)

# Do a search for every term only in GO ontology
search_results = []
for term in terms:
    #search_results.append(get_json(REST_URL + "/search?q=" + term+"&ontology=GO&roots_only=true")["collection"])
    search_results.append(get_json(REST_URL + "/search?q=melanoma&ontology=NCIT&subtree_root_id=http%3a%2f%2fncicb.nci.nih.gov%2fxml%2fowl%2fEVS%2fThesaurus.owl%23C3224&require_exact_match=True")["collection"])
# Open the file for writing
with open("classes_search_simple_result.txt", "w", encoding="utf-8") as file:
    # Print the results
    for result in search_results:
        file.write("\n".join(map(str, result)) + "\n")
