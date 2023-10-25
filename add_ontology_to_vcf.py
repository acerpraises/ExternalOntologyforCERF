
from record_change import record_changes_to_csv
#from get_ontology import get_ontology
from Bio import SeqIO
import datetime
import os
import re
'''
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
'''

def choose_info_id(vcf_file, default_id="OT"):
    """
    Allow the user to choose an ID for the ontology term in the VCF's INFO column.

    :param vcf_file: Path to the VCF file.
    :param default_id: Default ID to suggest to the user.
    :return: Chosen ID.
    """
    def check_info_id_exists(vcf_file, desired_id):
        with open(vcf_file, 'r') as fin:
            for line in fin:
                if line.startswith("##INFO"):
                    info_id = None
                    # Extract ID value from the INFO line
                    for part in line.split(","):
                        if part.startswith("ID="):
                            info_id = part.split("=")[1]
                            break
                    if info_id == desired_id:
                        return True
        return False

    #chosen_id = input(f"Enter the desired ID for the ontology term (default: {default_id}): ").strip() or default_id
    chosen_id="OT"
    while check_info_id_exists(vcf_file, chosen_id):
        print(f"The ID {chosen_id} is already in use. Use another one named OL.")
        #chosen_id = input(f"Enter the desired ID for the ontology term (default: {default_id}): ").strip() or default_id
        chosen_id="OL"
    return chosen_id
    
def add_ontology_to_vcf(input_file, user_choice, overall_ontology, attribute_ontology):
    # if other INFO already used ID=OT, ask user to choose another ID for ontology
    #chosen_id = choose_info_id(input_file)#desicion not change individual level read
    chosen_id="OT"
    # Determine if user wants a unique ontology for each sequence or a single overall ontology
    #user_choice, overall_ontology, attribute_ontology = get_ontology_choice()
    
    # Create a backup filename with date-time suffix
    base_filename = input_file.rsplit('.', 1)[0]  # Remove the .vcf extension
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{base_filename}_{current_time}.vcf"
    temp_file = f"{base_filename}_{current_time}_temp.vcf"

    # create record for to save to the csv:
    record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    change_record = {
        'Input file name': input_file.split('\\')[-1],
        'Backup file name': backup_file.split('\\')[-1],
        'Modify date and time': record_time,
        'Different Ontology in reads or not': user_choice,
        #'Changes description': '{attribute_ontology}.'
        'Changes description': '{overall_ontology}.'#add overall_ontology to header
        }

         
    # Initialize the flag
    all_sequences_unmodified = True

    
    ontology_header = f'##INFO=<ID=OT,Number=.,Type=String,Description="Ontology term associated with the variant">'
    header_added = False
    
    with open(input_file, 'r') as fin, open(temp_file, 'w') as fout:
        attribute_ontology_exist=False
        fileformat_flag=False
        INFO_flag=False
        Metadata_line_end=False
        
        previous_inputs = {}  # Dictionary to remember ontology for each read_id
        
        for line in fin:
            if (re.match(r'^##[A-Z]+', line)) and Metadata_line_end==False and attribute_ontology_exist==False:
                if attribute_ontology_exist==False and user_choice == 'no':
                    #add a meta-data line for the overall ontology
                    add_line = "##ontology="+overall_ontology+"\n"
                    change_record['Changes description']+=f"over all unique change: {overall_ontology}."
                    fout.write(add_line)
                    attribute_ontology_exist==True
                Metadata_line_end=True
            # Check if the line starts with ##ontology=
            if line.startswith("##ontology="):
                # Check if the provided attribute_ontology already exists in the line
                if overall_ontology not in line:
                    fout.write(line)
                    # add a new meta-data line and provide attribute_ontology to it
                    if user_choice == 'no':
                        add_line = "##ontology" + "="+overall_ontology+"\n"
                        
                        change_record['Changes description']+=f"over all unique change: {overall_ontology}."

                        fout.write(add_line)
                ##attribute_ontology_added = True
                attribute_ontology_exist=True
                continue
            
            
            if line.startswith("##INFO"):
                # Check if our custom ontology header already exists.
                if ontology_header in line:
                    header_added = True
                    
            # Writing headers directly
            if line.startswith("##"):                
                fout.write(line)
                continue
            
            # If our custom ontology header is not in the file, add it.
            if line.startswith("#CHROM"):
                
                if not header_added:
                    fout.write(ontology_header + "\n")
                    header_added = True
                fout.write(line)
                continue

            # Write column header line directly to output
            if line.startswith("#CHROM"):
                fout.write(line)
                continue    

            fields = line.strip().split('\t')
            
            # Get read_id (in VCF, this might be an identifier in the ID column)
            read_id = fields[2]
            
            # Get ontology term for the read/variant
            ontology_term=None
            if user_choice == 'yes':
                # Here, you'd call the get_ontology() function, something like:
                # ontology_term = get_ontology(read_id)  
                # But for the sake of this example, I'm using a mock value
                #ontology_term = get_ontology(read_id,previous_inputs=previous_inputs)
                if read_id not in previous_inputs:
                    previous_inputs[read_id] = ontology_term
            
            # Check if ontology term already exists in the INFO column

            ontology_attribute_found = False

            if len(fields)>7:
                if ontology_term == "":
                    change_record['Changes description'] += f" {read_id},No Ontology input;"
                    print(f" {read_id},No Ontology input;")
                else:
                    if f"{chosen_id}=" not in fields[7]:
                        if user_choice == 'yes':
                            fields[7] += f";{chosen_id}={ontology_term}"
                            change_record['Changes description'] += f" {read_id},{ontology_term} added;"
                            print(f" {read_id},{ontology_term} added;")
                    else:
                        info_fields = fields[7].split(";")
                        for i, info in enumerate(info_fields):
                            if info.startswith(f"{chosen_id}="):
                                ontology_values = info.split("=")[1].split(",")  # Assuming ',' is a delimiter within attribute values
                                if ontology_term in ontology_values:
                                    ontology_term_found = True
                                if ontology_term not in ontology_values:
                                    # only add ontology term which is different between IDs
                                    if user_choice == 'yes':
                                        info_fields[i] += f",{ontology_term}"
                                        change_record['Changes description'] += f" {read_id}'s Ontology_term updated with {ontology_term};"
                                        print(f" {read_id}'s Ontology_term updated with {ontology_term}")
                                    break
                        if ontology_term_found:
                            change_record['Changes description'] += f" {read_id},{ontology_term} already exist;"
                            print(f" {read_id},{ontology_term} already exist;")
                            
                        # Recreate the INFO string            
                        fields[7] = ";".join(info_fields)

                    fout.write("\t".join(fields) + "\n")
            else:
                fout.write(line)
            
            # Rename the original file to its temporaty version
    os.rename(input_file, backup_file)
    
            # rename the temp file to the original file
    os.rename(temp_file, input_file)

            # Determine the directory of the input file
    input_file_dir = os.path.dirname(input_file)
    
            # Construct the complete path for the CSV
    csv_filepath = os.path.join(input_file_dir, 'ontology_changes.csv')
    
            # store changes to CSV
    record_changes_to_csv(csv_filepath, change_record)

if __name__ == "__main__":
    # Get input from the user
    input_path = input("Please enter the path and name of the input VCF file: ")
    
    # Add ontology to the input file and save backup
    add_ontology_to_vcf(input_path)
    print(f"File modified and a backup has been saved with a date-time suffix.")
