from Bio import SeqIO
import datetime

def add_ontology_to_fasta(input_file, ontology_function):
    """
    Modify FASTA file to add ontology annotations.
    
    :param input_file: Path to the input FASTA file.
    :param ontology_function: Function to get ontology based on sequence ID.
    """
    # Determine if user wants a unique ontology for each sequence or a single overall ontology
    user_choice = ""
    while user_choice not in ['yes', 'no']:
        user_choice = input("Do you want to add different ontology to each sequence? (Yes/No): ").strip().lower()
        if user_choice not in ['yes', 'no']:
            print("Please enter either 'Yes' or 'No'.")
    overall_ontology = None
    
    if user_choice == 'no':
        overall_ontology = input("Enter the overall unique ontology for all sequences: ")
    
    # Create a backup filename with date-time suffix
    base_filename = input_file.rsplit('.', 1)[0]  # Remove the .fasta extension
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{base_filename}_{current_time}.fasta"
    temp_file = f"{base_filename}_{current_time}_temp.fasta"
    
    # Read the FASTA file, add ontology annotations and store in a list
    modified_records = []
    
    with open(input_file, 'r') as infile:
        for record in SeqIO.parse(infile, 'fasta'):
            ontology_term = get_ontology(record.id, overall_ontology)

            # Check if ontology information already exists
            if ontology_term in record.description:
                print(f"Warning: fasta ID {record.id} already contain ontology information, so not modified.")
                modified_records.append(record)
                
            else:
                if record.description.replace(record.id, '').strip().strip('|').strip()=="":
                    record.description = f"{record.id} | {ontology_term}"
                else:
                    record.description = f"{record.id} | {ontology_term} | {record.description.replace(record.id, '').strip().strip('|').strip()}"
                modified_records.append(record)

    # Rename the original file to its backup version
    import os
    os.rename(input_file, temp_file)
    
    # Write the modified records back to the original input filename
    with open(input_file, 'w') as outfile:
        SeqIO.write(modified_records, outfile, 'fasta')
    
    # rename the temp file to the original file
    os.rename(temp_file, backup_file)

def get_ontology(sequence_id, overall_ontology=None):
    """
    Get ontology term based on sequence ID. 
    
    If overall_ontology is provided, return it directly. 
    Otherwise, prompt the user for ontology information.
    
    :param sequence_id: ID of the sequence.
    :param overall_ontology: If set, this ontology will be returned without prompting the user.
    :return: Ontology term.
    """
    if overall_ontology:
        return overall_ontology
    return input(f"Enter ontology for sequence {sequence_id}: ")

if __name__ == "__main__":
    # Get input from the user
    input_path = input("Please enter the path and name of the input FASTA file: ")
    
    # Add ontology to the input file and save backup
    add_ontology_to_fasta(input_path, get_ontology)
    print(f"File modified and a backup has been saved with a date-time suffix.")
