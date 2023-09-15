def get_ontology_choice():
    """Prompt user for ontology choice and return the user's decision and overall ontology term if applicable."""
    
    user_choice = ""
    while user_choice not in ['yes', 'no']:
        user_choice = input("Do you want to add different ontology to each read? (Yes/No): ").strip().lower()
        if user_choice not in ['yes', 'no']:
            print("Please enter either 'Yes' or 'No'.")

    overall_ontology = None
    if user_choice == 'no':
        overall_ontology = input("Enter the overall unique ontology for all reads: ")

    return user_choice, overall_ontology