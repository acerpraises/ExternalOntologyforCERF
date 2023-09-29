import csv
import datetime
def record_changes_to_csv(output_filename, change_record):
    """
    Store the changes made to the FASTA file into a CSV file.
    
    :param output_filename: Name of the output CSV file.
    :param change_record: Dictionary containing change details for the current file.
    """
    fieldnames = ['Input file name', 'Backup file name', 'Modify date and time', 'Different Ontology in reads or not', 'Changes description']
    
    # Check if file exists to determine whether to write headers
    file_exists = True
    try:
        with open(output_filename, 'r'):
            pass
    except FileNotFoundError:
        file_exists = False

    with open(output_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(change_record)
