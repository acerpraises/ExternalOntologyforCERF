

import datetime
import os
import re

from record_change import record_changes_to_csv
from get_ontology import get_ontology

def modify_header(header, ontology_term_to_add):
    # If ontology term not exist in header, add it
    if ontology_term_to_add not in header:
        header.append(ontology_term_to_add)
    '''
    else:
        counter = 1
        while f"{ontology_term_to_add}_{counter}" in header:
            counter += 1
        header.append(f"{ontology_term_to_add}_{counter}")
    '''
    return header

def update_description_with_ontology(description, ontology_term, change_record, record_Id, all_sequences_unmodified):
    # If ontology term already exists in the description
    if f"{ontology_term}" in description.split():
        print(f"Warning: Read {record_Id} already contains the ontology term {ontology_term}.")
        change_record['Changes description'] += f"{record_Id} already contained ontology. "
        return description, change_record, all_sequences_unmodified
    
    all_sequences_unmodified=False
    if "OT:Z:" in description:
        # Extract the OT:Z: portion and add the new ontology term
        change_record['Changes description'] += f"{record_Id},{ontology_term};"
        parts = description.split(";")
        for index, part in enumerate(parts):
            if part.startswith("OT:Z:"):
                parts[index] += f", {ontology_term}"
                return ";".join(parts), change_record, all_sequences_unmodified
    else:
        # Add a new OT:Z: tag with the ontology term
        description += f";OT:Z: {ontology_term}"
        change_record['Changes description'] += f"{record_Id},{ontology_term};"

    return description, change_record, all_sequences_unmodified
def add_ontology_to_sam(input_file, user_choice, overall_ontology, attribute_ontology):
    
    # Get user choice and overall ontology if applicable
    #user_choice, overall_ontology , attribute_ontology= get_ontology_choice()
        
    # Create a backup filename with date-time suffix
    base_filename = input_file.rsplit('.', 1)[0]  # Remove the .fasta extension
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{base_filename}_{current_time}.sam"
    temp_file = f"{base_filename}_{current_time}_temp.sam"
    
    # create record for to save to the csv:
    record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    change_record = {
        'Input file name': input_file.split('\\')[-1],
        'Backup file name': backup_file.split('\\')[-1],
        'Modify date and time': record_time,
        'Different Ontology in reads or not': user_choice,
        'Changes description': ''
        }
    if user_choice == 'no':
         change_record['Changes description']=f"over all unique change: {overall_ontology}."


    # Initialize the flag
    all_sequences_unmodified = True

    #prepare for header line modifications'
    header_lines = []
    
    with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
        #create a flag to check if there is a header line
        header_line_Notexist=True
        # Collect header lines
        for line in infile:
            if line.startswith('@'):
                # Header line
                headers = line.strip().split('\t')
                #for @HD if exist should always be the first line
                while header_line_Notexist==True:
                    if headers[0]=='@HD':
                        header_line_Notexist=False
                        
                        if user_choice == 'yes':
                        # User wants different ontology for each read
                            if "CO:Ontology different in each read" not in headers:
                                headers = modify_header(headers, "CO:Ontology different in each read")
                        else:
                        # User wants one ontology for all reads
                            if f'CO:Overall Ontology is {overall_ontology}' not in headers:
                                headers = modify_header(headers, f'CO:Overall Ontology is {overall_ontology}')
                    else:
                        header=['@HD']
                        header_line_Notexist=False
                        if user_choice == 'yes':
                        # User wants different ontology for each read
                            header = f'@HD'+'\t'+'CO:Ontology different in each read'
                        else:
                        # User wants one ontology for all reads
                            header = '@HD'+'\t'+f'CO:Overall Ontology is {overall_ontology}'
                        outfile.write(header + '\n')
                outfile.write('\t'.join(headers) + '\n') 
            else:
                if header_line_Notexist==True:
                    if user_choice == 'yes':
                        # User wants different ontology for each read
                        header = f'@HD'+'\t'+'CO:Ontology different in each read'
                    else:
                        # User wants one ontology for all reads
                        header = '@HD'+'\t'+f'CO:Overall Ontology is {overall_ontology}'
                    outfile.write(header + '\n')
                # SAM record line
                fields = line.strip().split('\t')
                read_name = fields[0]
                if user_choice=='yes':
                    ontology_term_to_add=get_ontology(read_name, overall_ontology=overall_ontology)
                else:
                    ontology_term_to_add=overall_ontology
                '''    
                if len(fields)==11:
                    outfile.write('\t'.join(fields) +'\t'+f'OT:Z:{ontology_term_to_add}' +'\n')
                    change_record['Changes description'] += f"{read_name},{ontology_term_to_add}."
                    all_sequences_unmodified=False
                else:
                    description=fields[11]
                    print(fields[11])
                    fields[11],change_record,all_sequences_unmodified = update_description_with_ontology(
                        description, ontology_term_to_add, change_record, read_name, all_sequences_unmodified)
                    outfile.write('\t'.join(fields) + '\n')
                '''
                #not change individual read
                outfile.write('\t'.join(fields) + '\n')
    # Rename the original file to its back version
    os.rename(input_file, backup_file)
    
    
    # rename the temp file to the original file
    os.rename(temp_file, input_file)

    # After all records are processed:
    if all_sequences_unmodified:
        change_record['Changes description'] = 'All sequences NOT changed due to Ontology existing.'
        
    # Determine the directory of the input file
    input_file_dir = os.path.dirname(input_file)
    
    # Construct the complete path for the CSV
    csv_filepath = os.path.join(input_file_dir, 'ontology_changes.csv')
    
    # store changes to CSV
    record_changes_to_csv(csv_filepath, change_record)
    print(f"Ontology added to exsiting file and the original file saved as {backup_file}")

    '''            
    # Rename the original file to its backup version
    os.rename(input_file, backup_file)
    
    # Rename the temp file to its original version
    os.rename(temp_file, inputfile)

    # After all records are processed:
    if all_sequences_unmodified:
        change_record['Changes description'] = 'All sequences NOT changed due to Ontology existing.'
    '''
# Example usage
if __name__ == "__main__":
    # Get input from the user
    input_path = input("Please enter the path and name of the input FASTA file: ")
    
    # Add ontology to the input file and save backup
    add_ontology_to_sam(input_path, get_ontology)
    print(f"File modified and a backup has been saved with a date-time suffix.")
