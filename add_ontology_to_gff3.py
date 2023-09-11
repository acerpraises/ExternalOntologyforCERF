def add_ontology_to_gff3(input_gff3, output_gff3, ontology_function):
    with open(input_gff3, 'r') as infile, open(output_gff3, 'w') as outfile:
        for line in infile:
            if line.startswith("#"):  # Copy over comments without changes
                outfile.write(line)
                continue
            
            # Parse the line
            parts = line.strip().split("\t")
            attributes = parts[8]

            # Extract an identifier (like ID or Name) to fetch ontology
            # Adjust as needed for your dataset
            identifier = [item.split("=")[1] for item in attributes.split(";") if "ID" in item][0]

            # Fetch the ontology term based on the identifier
            ontology_term = ontology_function(identifier)

            # Append the ontology term to the attributes
            attributes += f';OntologyTerm={ontology_term}'

            # Construct the new line and write to output
            new_line = "\t".join(parts[:-1]) + "\t" + attributes + "\n"
            outfile.write(new_line)

def get_ontology(identifier):
    """Example function to return an ontology term based on identifier."""
    # This is a mock function; replace with your lookup logic.
    return "GO:0006915"

# Usage
add_ontology_to_gff3("input.gff3", "output.gff3", get_ontology)
