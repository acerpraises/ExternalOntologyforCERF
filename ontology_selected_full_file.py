import os
import datetime
import shutil

def ontology_selected_full_file(selected_file_name,temp_ontology_file):
   print(temp_ontology_file) 
   # only if an ontology was selected
   datestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
   #The root will be everything except the file extension, and ext will be the file extension.
   root, ext = os.path.splitext(temp_ontology_file )
   #only get file name but not the whole root locations
   only_name = os.path.basename(selected_file_name)
   temp_file_name = "ontology." + only_name + "." + datestamp+ext
   print(temp_file_name)
   temp_file_path = os.path.join(os.path.dirname(selected_file_name), temp_file_name)
   print(temp_file_path)                
   #original_temp_file_path = os.pa th.join(os.path.dirname(select_file_path), "temp_filename" + file_extension)
   shutil.copy(temp_ontology_file, temp_file_path)
