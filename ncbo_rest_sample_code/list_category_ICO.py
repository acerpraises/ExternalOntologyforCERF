import urllib.request, urllib.error, urllib.parse
import json
import os
import pprint

REST_URL = "http://data.bioontology.org/"
API_KEY = "87a6e825-e26c-4bd3-9ff8-508eae699720"

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

# Get the available resources
resources = get_json(REST_URL + "/")
print(resources)
'''
# Get the category from the `categories` link
categories = get_json(resources["links"]["categories"])


# Get the name and category id from the returned list
categories_output = []
   
with open("list_categories_result.txt", "w", encoding="utf-8") as file:
    for category in categories:
        ##categories_output.append(f"{category['name']}\n{category['@id']}\n")
        formatted_ontology = pprint.pformat(category)  # Get the pretty formatted string representation
        file.write(formatted_ontology + "\n\n")  # Write to file with additional newlines for separation
    

# Get the ontologies from the `/ontologies/:acronym/categories` link

Onto_categories = get_json(resources["links"]["ontologies_full"])


# Get the name and ontology id from the returned list
Onto_categories_output = []
'''

    
with open("list_onto_categories_result.txt", "w", encoding="utf-8") as file:
    for Onto_category in Onto_categories:
            formatted_ontology = pprint.pformat(Onto_category)  # Get the pretty formatted string representation
            file.write(formatted_ontology + "\n\n")  # Write to file with additional newlines for separation
   


