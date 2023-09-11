def add_ontology_to_vcf(input_vcf, output_vcf, ontology_function):
    with open(input_vcf, 'r') as infile, open(output_vcf, 'w') as outfile:
        for line in infile:
            if line.startswith("##"):
                outfile.write(line)
                continue
            
            if line.startswith("#CHROM"):
                outfile.write('##INFO=<ID=GO,Number=.,Type=String,Description="Gene Ontology Term">\n')
                outfile.write(line)
                continue
            
            parts = line.strip().split("\t")
            info = parts[7]

            # Use an identifier (e.g., the variant's position) to fetch ontology
            identifier = parts[1]

            ontology_term = ontology_function(identifier)
            if ontology_term:
                info += f';GO={ontology_term}'

            parts[7] = info
            outfile.write("\t".join(parts) + "\n")

def get_ontology(identifier):
    """Example function to return an ontology term based on identifier."""
    # This is a mock function; replace with your lookup logic.
    if identifier == "12345":
        return "GO:0006915"
    elif identifier == "67890":
        return "GO:0008270,GO:0006915"
    return None

# Usage
add_ontology_to_vcf("input.vcf", "output.vcf", get_ontology)