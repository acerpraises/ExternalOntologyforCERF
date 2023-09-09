import pysam

def add_ontology_to_sam(input_sam, output_sam, ontology_function):
    with pysam.AlignmentFile(input_sam, "r") as infile, \
         pysam.AlignmentFile(output_sam, "wh", header=infile.header) as outfile:
        
        # Write reads with added ontology to the output SAM file
        for read in infile:
            ontology_term = ontology_function(read.query_name)
            read.set_tag("ZT", ontology_term)  # Set custom ontology tag
            outfile.write(read)

def get_ontology(read_name):
    """Example function to return an ontology term based on read name."""
    # Mock function; replace with real lookup logic.
    return "GO:0006915"

# Usage
add_ontology_to_sam("input.sam", "output.sam", get_ontology)