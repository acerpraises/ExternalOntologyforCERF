import flet as ft
import os
import webbrowser
#First, make sure you have imported all the required functions at the beginning of your script:
from add_ontology_to_fasta import add_ontology_to_fasta
from add_ontology_to_sam import add_ontology_to_sam
from add_ontology_to_gff3 import add_ontology_to_gff3
from add_ontology_to_vcf import add_ontology_to_vcf

file_path = None
select_file_path = None
selected_ontology = None
open_bioportal = None

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
            file_extension = os.path.splitext(select_file_path)[1].lower()
        
            # Determine which function to call based on file format
            if file_extension == ".fasta":
                add_ontology_to_fasta(select_file_path, "no", ontology_input.value, None)
            elif file_extension == ".sam":
                add_ontology_to_sam(select_file_path, "no", ontology_input.value, None)
            elif file_extension == ".gff3":
                add_ontology_to_gff3(select_file_path, "no", ontology_input.value, None)
            elif file_extension == ".vcf":
                add_ontology_to_vcf(select_file_path, "no", ontology_input.value, None)
            else:
                print(f"Unsupported file format: {file_extension}")


    #dropdown menu > we can maybe add Ontology options
    def dropdown_button_clicked(e):
        output_text.value = f"Dropdown value is:  {color_dropdown.value}"
        page.update()

    #To add a box that lets you input text
    ontology_input = ft.TextField(label="Please input your ontology or search term:", width=400)
    
    #Dropdown button 
    output_text = ft.Text(color='black')
    submit_btn = ft.ElevatedButton(text="Submit", on_click=dropdown_button_clicked)
    color_dropdown = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
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
                             height=200,
                             color='WHITE',
                             bgcolor="#1976D2", 
                             weight='w400', 
                            size=20)

    ontologyBoxText = ft.Text(value='Select Ontology', 
                              width=500,
                              height=200,
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
    
    page.add(selectFileText, ontology_input, entriesRow, ontologyBoxText, search_box, color_dropdown, submit_btn, output_text, buttonRow)

ft.app(target=main)
