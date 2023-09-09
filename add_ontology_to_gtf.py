def add_ontology_to_gtf(input_gtf, output_gtf, ontology_function):
    with open(input_gtf, 'r') as infile, open(output_gtf, 'w') as outfile:
        for line in infile:
            if line.startswith("#"):  # Copy over comments without changes
                outfile.write(line)
                continue
            
            # Parse the line
            parts = line.strip().split("\t")
            attributes = parts[8]

            # Get the feature's unique identifier (e.g., gene_id or transcript_id)
            # Adjust as necessary based on your data
            identifier = [item for item in attributes.split(";") if "gene_id" in item][0].split('"')[1]
            
            # Fetch the ontology term based on the identifier
            ontology_term = ontology_function(identifier)

            # Append the ontology term to the attributes
            attributes += f' OntologyTerm "{ontology_term}";'

            # Construct the new line and write to output
            new_line = "\t".join(parts[:-1]) + "\t" + attributes + "\n"
            outfile.write(new_line)

def get_ontology(identifier):
    """Example function to return an ontology term based on identifier."""
    # Mock function; replace with real lookup logic.
    return "GO:0006915"

# Usage
add_ontology_to_gtf("input.gtf", "output.gtf", get_ontology)