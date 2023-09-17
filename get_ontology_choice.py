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
    
    attribute_ontology = input("Please provide the URL or other info for the ontology_term added to the attribute (leave empty if none): ")

    return user_choice, overall_ontology, attribute_ontology