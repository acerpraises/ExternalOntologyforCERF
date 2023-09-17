def get_ontology(sequence_id, previous_inputs=None, overall_ontology=None):
    """
    Get ontology term based on sequence ID. 
    
    If overall_ontology is provided, return it directly. 
    Otherwise, prompt the user for ontology information.
    
    :param sequence_id: ID of the sequence.
    :param overall_ontology: If set, this ontology will be returned without prompting the user.
    :return: Ontology term.
    """
    if previous_inputs is None:
        previous_inputs = {}
    
    if sequence_id in previous_inputs:
        return previous_inputs[sequence_id]
        
    if overall_ontology:
        return overall_ontology
    ontology = input(f"Enter ontology for read {sequence_id}: ")
    return ontology