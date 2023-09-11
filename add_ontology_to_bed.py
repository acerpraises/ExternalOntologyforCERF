def add_ontology_to_bed(input_bed, output_bed, ontology_function):
    with open(input_bed, 'r') as infile, open(output_bed, 'w') as outfile:
        for line in infile:
            line = line.strip()
            parts = line.split("\t")

            # Use an identifier, like the name in column 4, to fetch the ontology
            identifier = parts[3]

            ontology_term = ontology_function(identifier)
            parts.append(ontology_term)

            outfile.write("\t".join(parts) + "\n")

def get_ontology(identifier):
    """Example function to return an ontology term based on identifier."""
    # This is a mock function; replace with your lookup logic.
    return "GO:0006915"

# Usage
add_ontology_to_bed("input.bed", "output.bed", get_ontology)
