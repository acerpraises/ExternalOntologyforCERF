import requests
import pprint
# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = '87a6e825-e26c-4bd3-9ff8-508eae699720'

# Base URL for the BioPortal API
BASE_URL = 'http://data.bioontology.org/'

# Endpoint to get all ontologies
ONTOLOGIES_ENDPOINT = 'ontologies'

# Set up the headers, including your API key
headers = {
    'Authorization': f'apikey token={API_KEY}'
}

def get_category_from_link(category_link):
    """Retrieve the categories using the provided link."""
    response = requests.get(category_link, headers=headers)
    if response.status_code == 200:
        category_data = response.json()
        
        # If the response is a list of categories, join them with commas
        if isinstance(category_data, list):
            return ', '.join([cat.get('name', 'Unknown') for cat in category_data])
        else:
            return category_data.get('name', 'Unknown')
    return 'Unknown'

# Make the API request
response = requests.get(BASE_URL + ONTOLOGIES_ENDPOINT, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    ontologies = response.json()
    
    # Open a file for writing
    with open("ontologies_output.txt", "w") as file:
        for ontology in ontologies:
            '''
            formatted_ontology = pprint.pformat(ontology)  # Get the pretty formatted string representation
            file.write(formatted_ontology + "\n\n")  # Write to file with additional newlines for separation
            '''
            file.write(f"Ontology Name: {ontology['name']}\n")
            
            # Retrieve the category using the category link
            category_link = ontology.get('links', {}).get('categories')
            if category_link:
                category = get_category_from_link(category_link)
                file.write(f"Category: {category}\n")
            
            file.write('------------------------\n')
        
else:
    print(f"Error {response.status_code}: {response.text}")
