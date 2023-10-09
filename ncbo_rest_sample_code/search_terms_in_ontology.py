import urllib.request
import json
import os
import tempfile
from urllib.parse import quote_plus

REST_URL = "http://data.bioontology.org"
API_KEY = "87a6e825-e26c-4bd3-9ff8-508eae699720"

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def search_terms_in_ontology(ontology_input, ontology_name, ontology_id):
    # Convert ontology_id to short form
    print(ontology_id)
    ontology_short = ontology_id.split("/")[-1]
    print(ontology_id)
    
    #encoding the string properly before putting it into the URL
    encoded_search_query = quote_plus(ontology_input)

    # Search in the selected ontology
    full_url = f"{REST_URL}/search?q={encoded_search_query}&ontologies={ontology_short}&require_exact_match=True"
    print(f"Accessing URL: {full_url}")
    results = get_json(full_url)["collection"]

    # Check the length of the results
    if len(results) == 50:
        print("Warning: Only the first 50 Ontology Classes are shown!")

    # Create a directory to store the results
    result_dir = os.path.join(tempfile.gettempdir(), "ontology_search_results")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    extracted_data = []

    # Write the results to separate temporary files
    for idx, result in enumerate(results):
        # Extract required data
        pref_label = result['prefLabel']
        id_ = result['@id']
        definition = result.get('definition', ['N/A'])[0]  # Some results might not have a definition; use N/A in that case.

        
        
        # Create a temporary file for the result
        temp_file_path = os.path.join(result_dir, f"result_{idx + 1}.json")
        with open(temp_file_path, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)  # Write entire JSON content
            
        extracted_data.append((pref_label, id_, definition, temp_file_path)) # Write entire JSON path to output
    print(f"Search results written to separate files in '{result_dir}'.")
    return extracted_data
#print(search_terms_in_ontology("melanoma", None, "https://data.bioontology.org/ontologies/NCIT"))
