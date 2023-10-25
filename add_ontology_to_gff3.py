
from record_change import record_changes_to_csv
#from get_ontology import get_ontology
from Bio import SeqIO
import datetime
import os
import re

def get_ontology_choice():
    # Determine if user wants a unique ontology for each sequence or a single overall ontology
    user_choice = ""
    while user_choice not in ['yes', 'no']:
        user_choice = input("Do you want to add different ontology to each record? (Yes/No): ").strip().lower()
        if user_choice not in ['yes', 'no']:
            print("Please enter either 'Yes' or 'No'.")

    overall_ontology = None
    if user_choice == 'no':
        overall_ontology = input("Enter the overall unique ontology for all records: ")
    
    attribute_ontology = input("Please provide the URL for the ontology_term added to the attribute (leave empty if none): ")

    return user_choice, overall_ontology, attribute_ontology
	
def add_ontology_to_gff3(input_file, user_choice, overall_ontology, attribute_ontology):
    # Determine if user wants a unique ontology for each sequence or a single overall ontology
    #user_choice, overall_ontology, attribute_ontology = get_ontology_choice()
    
     # Create a backup filename with date-time suffix
    base_filename = input_file.rsplit('.', 1)[0]  # Remove the .gff3 extension
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{base_filename}_{current_time}.gff3"
    temp_file = f"{base_filename}_{current_time}_temp.gff3"

    # create record for to save to the csv:
    record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    change_record = {
        'Input file name': input_file.split('\\')[-1],
        'Backup file name': backup_file.split('\\')[-1],
        'Modify date and time': record_time,
        'Different Ontology in reads or not': user_choice,
        #'Changes description': '{attribute_ontology}.'
        'Changes description': '{overall_ontology}.'
        }
    if user_choice == 'no':
         change_record['Changes description']+=f"over all unique change: {overall_ontology}."
    
    # Initialize the flag
    all_sequences_unmodified = True  
    
    with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
        attribute_ontology_exist=False
        
        previous_inputs = {}  # Dictionary to remember ontology for each read_id
         
        for line in infile:
        
            # Check if the line starts with ##attribute-ontology
            if line.startswith("##attribute-ontology"):
                # Check if the provided attribute_ontology already exists in the line
                if overall_ontology not in line:
                    # Append the provided attribute_ontology to it
                    if user_choice == 'no':
                        #line = line.strip() + "; " + attribute_ontology +";"+overall_ontology+"\n"
                        line = line.strip() + "; " +overall_ontology+"\n"
                    #else:
                    #    line = line.strip() + "; " + attribute_ontology +"\n"
                attribute_ontology_added = True
                attribute_ontology_exist=True
                
            # Writing comments or headers directly
            if line.startswith("#"):                
                outfile.write(line)
                continue
            
            # Splitting GFF3 fields
            
            #add a ##attribute-ontology line if not exist
            if attribute_ontology_exist==False:
                if user_choice == 'no':
                    #outfile.write("##attribute-ontology"+":"+overall_ontology+";"+ attribute_ontology+"\n")
                    outfile.write("##attribute-ontology"+":"+overall_ontology+"\n")
                #else:
                    #outfile.write("##attribute-ontology:"+ attribute_ontology+"\n")
                attribute_ontology_exist=True
            
            fields = line.strip().split('\t')
            if len(fields) != 9:
                # If this isn't a valid GFF3 line, we'll simply write it to the output.
                outfile.write(line)
                continue
            
            # Assuming column 9 is the attribute column
            attributes = fields[8]
            # Assuming read_ID is the comb of seqID and first element of attribute column
            attributes_fields=attributes.split(';')
            read_id=attributes_fields[0]
            
            if user_choice == 'yes':
                # Here, you'd call the get_ontology() function, something like:
                print("Add different ontology to each read is still in development") 
                # But for the sake of this example, I'm using a mock value
                # ontology_term = get_ontology(attributes_fields[0],previous_inputs)
                if read_id not in previous_inputs:
                    previous_inputs[read_id] = ontology_term

            else:
                ontology_term = overall_ontology
            
            # Check if ontology term already exists in the source, feature, or attribute columns
            ontology_term_found = False

            if ontology_term not in fields[1] and ontology_term not in fields[2] and not any(a.startswith("Ontology_term=") for a in attributes_fields):
                attributes_fields.append(f"Ontology_term={ontology_term}")
                if user_choice == 'yes':
                    change_record['Changes description'] += f" {read_id},{ontology_term} added;"
                    print(f" {read_id},{ontology_term} added;")
            elif (ontology_term in fields[1] or ontology_term in fields[2]) and not any(a.startswith("Ontology_term=") for a in attributes_fields):
                ontology_term_found=True
            else:
                '''
                for i, attributes_element in enumerate(attributes_fields):
                    if attributes_element.startswith("Ontology_term="):
                        ontology_values = attributes_element.split("=")[1].split(" ")  # Assuming ' ' is a delimiter within attribute values
                        if ontology_term in ontology_values:
                            ontology_term_found = True
                        else:
                            # Append the ontology term to the existing Ontology_term attribute
                            updated_attribute = attributes_element + f" {ontology_term}"
            
                            # Overwrite the original attributes_element in attributes_fields
                            attributes_fields[i] = updated_attribute
                            
                            # Update change_record to reflect the change to the existing attribute
                            change_record['Changes description'] += f" {read_id}'s Ontology_term updated with {ontology_term};"
                            print(f" {read_id}'s Ontology_term updated with {ontology_term};")
                            #print(attributes_element)
                            break
                #print(attributes_fields)
                '''
                '''            
                # In case the ontology term was not found after any "Ontology_term=" instance
                if not ontology_term_found:
                    attributes_fields.append(f"Ontology_term={ontology_term}")
                    change_record['Changes description'] += f" {read_id},{ontology_term} added;"
                    print(f" {read_id},{ontology_term} added;")
                '''
            if ontology_term_found:
                change_record['Changes description'] += f" {read_id},{ontology_term} already exist;"
                print(f" {read_id},{ontology_term} already exist;")
                    
            # Recreate the attributes string
            attributes = ";".join(attributes_fields)
            #print(attributes)
                
                
            # Write updated line to the output file
            outfile.write('\t'.join(fields[:8] + [attributes]) + '\n')
            
    # Rename the original file to its temporaty version
    os.rename(input_file, backup_file )
    
    # rename the temp file to the original file
    os.rename(temp_file, input_file)

    '''
    # After all records are processed:
    if all_sequences_unmodified:
        change_record['Changes description'] = 'All sequences NOT changed due to Ontology existing.'
    '''
        
    # Determine the directory of the input file
    input_file_dir = os.path.dirname(input_file)
    
    # Construct the complete path for the CSV
    csv_filepath = os.path.join(input_file_dir, 'ontology_changes.csv')
    
    # store changes to CSV
    record_changes_to_csv(csv_filepath, change_record)
        

if __name__ == "__main__":
    # Get input from the user
    input_path = input("Please enter the path and name of the input gff3 file: ")
    
    # Add ontology to the input file and save backup
    add_ontology_to_gff3(input_path)
    print(f"File modified and a backup has been saved with a date-time suffix.")
