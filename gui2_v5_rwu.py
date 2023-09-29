import flet as ft
import os
import webbrowser
import re
import os
import datetime

from ncbo_rest_sample_code.fetch_ontologies import fetch_ontologies
from ncbo_rest_sample_code.search_terms_in_ontology  import search_terms_in_ontology 

#First, make sure you have imported all the required functions at the beginning of your script:
from add_ontology_to_fasta import add_ontology_to_fasta
from add_ontology_to_sam import add_ontology_to_sam
from add_ontology_to_gff3 import add_ontology_to_gff3
from add_ontology_to_vcf import add_ontology_to_vcf

file_path = None
select_file_path = None
selected_ontology = None
open_bioportal = None
results_key = None
temp_ontology_file=None

def main(page: ft.page):
    def select_file(e: ft.FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Select file...")
        #return_file()
    
    def return_file(e: ft.FilePickerResultEvent):
        global select_file_path  # Declare that you're using the global variable
        select_file_path = e.files[0].path
        selected_file_name = os.path.basename(select_file_path)
        file_path.value = selected_file_name
        file_path.update()
        print(f"File selected: {select_file_path}")  # Debugging statement

    #add a function to seach ontology in BioPortal
    def open_bioportal(event):
       # Perform a search on BioPortal (you can replace this with your actual search logic)
        bioportal_url = "https://bioportal.bioontology.org"
        webbrowser.open(bioportal_url)

    #select an ontology
    def add_ontoloty_to_file(e):
        print("Button clicked!")  # Debugging print statement
        if select_file_path:
            print(f"Calling the function for file: {select_file_path}")  # Debugging print statement
            #if not color_dropdown.value:  # Assuming the dropdown value is None when not selected.
            # Extract the file extension
            selected_file_name = os.path.basename(select_file_path)
            file_extension = os.path.splitext(select_file_path)[1].lower()
            
            # Get the ontology to add: either the selected one or directly from input
            if results_key:  # if an ontology was selected from the dropdown
                ontology_to_add = results_key  # use the @ID
            else:
                ontology_to_add = ontology_input.value  # directly use the input value


        
            # Determine which function to call based on file format
            if file_extension == ".fasta":
                add_ontology_to_fasta(select_file_path, "no", ontology_to_add , None)
            elif file_extension == ".sam":
                add_ontology_to_sam(select_file_path, "no", ontology_to_add , None)
            elif file_extension == ".gff3":
                add_ontology_to_gff3(select_file_path, "no", ontology_to_add , None)
            elif file_extension == ".vcf":
                add_ontology_to_vcf(select_file_path, "no", ontology_to_add , None)
            else:
                print(f"Unsupported file format: {file_extension}")

            # If you processed with search_terms_in_ontology and have a temp file:
            if results_key:  # only if an ontology was selected
                datestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                #The root will be everything except the file extension, and ext will be the file extension.
                root, ext = os.path.splitext(temp_ontology_file )
                
                temp_file_name = "ontology." + selected_file_name + "." + datestamp+ext
                temp_file_path = os.path.join(os.path.dirname(select_file_path), temp_file_name)
                
                #original_temp_file_path = os.path.join(os.path.dirname(select_file_path), "temp_filename" + file_extension)
                os.rename(temp_ontology_file, temp_file_path)

    #dropdown menu > we can maybe add Ontology options
    def dropdown_button_clicked(e):
        output_text.value = f"Dropdown value is:  {color_dropdown.value}"
        page.update()

    #To add a box that lets you input text
    ontology_input = ft.TextField(label="Please input your ontology or search term:", width=400)

    # Store the ontologies in a dictionary
    ontology_dict = fetch_ontologies()
    
    # Convert the dictionary keys (ontology names) into a list of dropdown options
    ontology_options = [ft.dropdown.Option(name) for name in ontology_dict.keys()]

    #Dropdown button
    # have a text input where the user will type:
    ontology_search_input = ft.TextField(label="Search for Ontology:", width=400)
    #Have a dropdown, initially empty or filled with all possible options:
    ontology_dict = fetch_ontologies()
    all_options = [ft.dropdown.Option(name) for name in ontology_dict.keys()]
    print(f"Total Ontologies: {len(all_options)}")# Debugging statement
    #Firstly, print out the first few ontologies to see what they look like:
    print(all_options[:5])  # Print the first 5 ontology options
    print(vars(all_options[0])) #Inspect the Option Object: Let's print out what an Option object contains to understand how to access the text inside it:
    #Manual Search Check: Perform a manual check to see if you find any matches:
    search_text = "a"
    print([opt for opt in all_options if opt.text and search_text.lower() in opt.text.lower()])

    ontology_dropdown = ft.Dropdown(
        width=400,
        options=all_options,
    )

    # Dropdown to display search results
    results_dropdown = ft.Dropdown(
        width=400,
        options=[]
    )

    # Text control to display the description of a selected result
    description_text = ft.Text("", color='black')
    
    #Have a button that, when clicked, will update the dropdown options based on the user's input:
    def update_dropdown_options(e):  # Notice the 'e' parameter
        print("Updating dropdown...")  # Debugging statement
        search_text = ontology_search_input.value or ""
        filtered_options = [opt for opt in all_options if opt._Control__attrs['key'][0] and search_text.lower() in opt._Control__attrs['key'][0].lower()]
        print(f"Filtered options: {filtered_options}")  # Debugging statement
        ontology_dropdown.options = filtered_options
        ontology_dropdown.update()  # Force the dropdown to update its options

    # New function to handle the submit button click
    def handle_submit(e):
        ontology_input_value = ontology_input.value
        ontology_name = ontology_dropdown.value
        ontology_id = ontology_dict.get(ontology_name, None)  # This retrieves the @id corresponding to the selected name
        if ontology_id:
            results = search_terms_in_ontology(ontology_input_value, ontology_name, ontology_id)
            print(f"Number of results: {len(results)}")  # Debugging line
        else:
            print("Error: Could not find @id for selected ontology.")
            # Handle error appropriately
            
        # Show warning if needed
        if len(results) == 50:
            warning_text.value = "Warning: Only the first 50 Ontology Classes are shown!"
            warning_text.update()

        # Clear previous results
        results_dropdown.options = []
        
        # Update the dropdown with the results
        dropdown_options = []
        for label, _id, definition, temp_file_path in results:
            option_text = f"{label} (@ID:{_id})"
            dropdown_options.append(ft.dropdown.Option(option_text))
        results_dropdown.options = dropdown_options

        
        # Callback for the results_dropdown
        def on_dropdown_change(e):
            # Set the global variable results_key
            global results_key
            global temp_ontology_file
            selected_option_value = results_dropdown.value
            print(f"Selected Option: {selected_option_value}")  # Debugging line
            
            # Extract the ontology ID using a regular expression
            match = re.search(r"@ID:(http[^)]+)", selected_option_value)
            selected_option_key = match.group(1) if match else None
            print(f"Selected Key: {selected_option_key}")  # Debugging line

            # Extracting the description for the selected ontology
            for label, ontology_id, definitionm, temp_file_path  in results:
                print(f"Checking against: {ontology_id}")  # Debugging line
                if ontology_id == selected_option_key:
                    description = definition or "No definition available."
                    results_key = ontology_id
                    temp_ontology_file=temp_file_path# pass the temp file path to the global variable results_key
                    break
            else:
                description = "Error: Could not find the selected ontology in the results."

            description_text.value = description
            description_text.update()
            #With this adjustment, the function will correctly extract the ontology ID from the selected dropdown value and then use it to find the associated description from the results. Run the app again and see if this resolves the issue.

        
        results_dropdown.on_change = on_dropdown_change
        results_dropdown.update()

    
    submit_btn = ft.ElevatedButton(text="Submit", on_click=handle_submit)
    
    # Warning text box
    warning_text = ft.Text('', color='red')
    
    # Container to display ontology results
    results_container = ft.Container()
    print(dir(results_container))
    
    update_button = ft.ElevatedButton(text="Search", on_click=update_dropdown_options)
    output_text = ft.Text(color='black')
    #submit_btn = ft.ElevatedButton(text="Submit", on_click=dropdown_button_clicked)
    color_dropdown = ft.Dropdown(
        width=400,
        options=ontology_options,
        value="Select Ontology to search OR directly add your input to file"
    )

    row_filepicker = ft.Row(vertical_alignment="center")
    global file_path
    file_path = ft.Text('Select a file...', expand=1, color='black', no_wrap=True)
    
    filepicker = ft.FilePicker(on_result=return_file)

    browserBtn = ft.ElevatedButton(text='Select file...', on_click=select_file) 
    
    row_filepicker.controls.append(browserBtn)
    row_filepicker.controls.append(file_path)
    
    page.title = 'Ontology for CERF'
    page.window_width = 500
    page.window_height = 900
    page.bgcolor = "WHITE"
    
    selectFileText = ft.Text(value= 'Select a file to add Ontology',
                             width=500,
                             height=50,
                             color='WHITE',
                             bgcolor="#1976D2", 
                             weight='w400', 
                            size=20)

    ontologyBoxText = ft.Text(value='Select Ontology', 
                              width=500,
                              height=50,
                              color="WHITE",
                              bgcolor="#1976D2", 
                              weight='w400', 
                              size=20
                              )
    
    
    openBioPortalBtn = ft.ElevatedButton(text='Open BioPortal', on_click=open_bioportal)
    addOntologyToFileBtn = ft.ElevatedButton(text='Add Ontology to file', on_click=add_ontoloty_to_file)

    #Create a bos for the search button and text
    search_box = ft.Container(width=500, height=50, bgcolor="EAEAEA")
    search_button = ft.ElevatedButton(text='Search on BioPortal', on_click=open_bioportal)
    search_box.controls = [search_button]
    

    

    entriesRow = ft.Row(controls=[row_filepicker],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    buttonRow = ft.Row(controls=[openBioPortalBtn, addOntologyToFileBtn],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    page.add(selectFileText,  entriesRow, ontologyBoxText, search_box, ontology_input, ontology_search_input, update_button, ontology_dropdown, submit_btn, warning_text, results_dropdown, description_text, results_container, output_text, buttonRow)

ft.app(target=main)
