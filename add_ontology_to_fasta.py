#be sure to install necessary libraries:
#run following code in bash:
#pip install biopython
from record_change import record_changes_to_csv
from get_ontology import get_ontology
from get_ontology_choice import get_ontology_choice
from Bio import SeqIO
import datetime
import os
import re

def add_ontology_to_fasta(input_file):
    """
    Modify FASTA file to add ontology annotations.
    
    :param input_file: Path to the input FASTA file.
    :param ontology_function: Function to get ontology based on sequence ID.
    """
    # Determine if user wants a unique ontology for each sequence or a single overall ontology
    user_choice, overall_ontology , attribute_ontology= get_ontology_choice()
        
    # Create a backup filename with date-time suffix
    base_filename = input_file.rsplit('.', 1)[0]  # Remove the .fasta extension
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{base_filename}_{current_time}.fasta"
    temp_file = f"{base_filename}_{current_time}_temp.fasta"

    # create record for to save to the csv:
    record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    change_record = {
        'Input file name': input_file.split('\\')[-1],
        'Backup file name': backup_file.split('\\')[-1],
        'Modify date and time': record_time,
        'Overall ontology change or not': user_choice,
        'Changes description': 'attribute_ontology;'
        }
    if user_choice == 'no':
         change_record['Changes description']=f"over all unique change: {overall_ontology}."
         
    # Read the FASTA file, add ontology annotations and store in a list
    modified_records = []

    # Initialize the flag
    all_sequences_unmodified = True  

    with open(input_file, 'r') as infile:
        for record in SeqIO.parse(infile, 'fasta'):
            ontology_term = get_ontology(record.id, overall_ontology)

            # Check if ontology information already exists
            if re.search(r'\b' + re.escape(ontology_term) + r'\b', record.description):
                warning=f"Warning: fasta ID {record.id} already contain ontology information, so not modified."
                print(warning)
                warning=f"{record.id}, {ontology_term} already contained."
                modified_records.append(record)
                # Within the loop where records are processed:
                change_record['Changes description'] += warning              
            else:
                # We've modified at least one sequence
                all_sequences_unmodified = False
                record.description = f"{record.id} | {ontology_term} | {record.description.replace(record.id, '').strip().strip('|').strip()}"
                change_record['Changes description'] += f" {record.id},{ontology_term};"
                modified_records.append(record)

    # Rename the original file to its temporaty version
    os.rename(input_file, temp_file)
    
    # Write the modified records back to the original input filename
    with open(input_file, 'w') as outfile:
        SeqIO.write(modified_records, outfile, 'fasta')
    
    # rename the temp file to the original file
    os.rename(temp_file, backup_file)

    # After all records are processed:
    if all_sequences_unmodified:
        change_record['Changes description'] = 'All sequences NOT changed due to Ontology existing.'
        
    # Determine the directory of the input file
    input_file_dir = os.path.dirname(input_file)
    
    # Construct the complete path for the CSV
    csv_filepath = os.path.join(input_file_dir, 'ontology_changes.csv')
    
    # store changes to CSV
    record_changes_to_csv(csv_filepath, change_record)
    


if __name__ == "__main__":
    # Get input from the user
    input_path = input("Please enter the path and name of the input FASTA file: ")
    
    # Add ontology to the input file and save backup
    add_ontology_to_fasta(input_path)
    print(f"File modified and a backup has been saved with a date-time suffix.")
