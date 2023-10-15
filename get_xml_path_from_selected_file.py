import os

def get_xml_path_from_selected_file(selected_file):
    """
    Compute the XML path based on the selected file path.
    """
    directory = os.path.dirname(selected_file)
    parent_directory = os.path.dirname(directory)
    xml_file_name = os.path.basename(directory) + ".cerf"
    xml_path = os.path.join(parent_directory, xml_file_name)
    return xml_path
