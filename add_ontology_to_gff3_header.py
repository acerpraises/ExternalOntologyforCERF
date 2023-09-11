def add_ontology_to_gff3_header(input_gff3, output_gff3, ontology_info):
    with open(input_gff3, 'r') as infile, open(output_gff3, 'w') as outfile:
        for line in infile:
            if line.startswith("##gff-version"):
                # Write the version line
                outfile.write(line)
                
                # Add the ontology info right after the version
                outfile.write(f"##ontology {ontology_info}\n")
                continue

            # Copy over other lines
            outfile.write(line)

# Usage
ontology_data = "Gene Ontology, version: 2023-05, source: http://geneontology.org"
add_ontology_to_gff3_header("input.gff3", "output.gff3", ontology_data)