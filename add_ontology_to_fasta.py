from Bio import SeqIO

def add_ontology_to_fasta(input_file, output_file, ontology_function):
    """
    Modify FASTA file to add ontology annotations.
    
    :param input_file: Path to the input FASTA file.
    :param output_file: Path to the output FASTA file.
    :param ontology_function: Function to get ontology based on sequence ID.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for record in SeqIO.parse(infile, 'fasta'):
            ontology_term = ontology_function(record.id)
            record.description = f"{record.id} | {ontology_term} | {record.description}"
            SeqIO.write(record, outfile, 'fasta')

def get_ontology(sequence_id):
    """Example function to return an ontology term based on sequence ID."""
    # This is a mock function; replace it with real lookup logic.
    return "GO:0006915"

# Usage
add_ontology_to_fasta("input.fasta", "output.fasta", get_ontology)