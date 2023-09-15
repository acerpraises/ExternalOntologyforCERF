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