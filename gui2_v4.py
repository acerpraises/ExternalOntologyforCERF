import flet as ft
import os
import webbrowser

file_path = None
select_file_path = None
selected_ontology = None
open_bioportal = None

def main(page: ft.page):
    
    def select_file(e: ft.FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Select file...")
        return_file()
    
    def return_file(e: ft.FilePickerResultEvent):
        selected_file_path = e.files[0].path
        selected_file_name = os.path.basename(selected_file_path)
        file_path.value = selected_file_name
        file_path.update()

    #add a function to seach ontology in BioPortal
    def open_bioportal(event): #Aieman -clicking to open BioPortal is an event so we have to let the function accept the one argument
       # Perform a search on BioPortal (you can replace this with your actual search logic)
        bioportal_url = "https://bioportal.bioontology.org"
        webbrowser.open(bioportal_url)

    #select an ontology
    def add_ontoloty_to_file():
        global select_file_path
        if select_file_path:
            with open(select_file_path, "a") as file:
                file.write(selected_ontology + "\n")


    #dropdown menu > we can maybe add Ontology options
    def dropdown_button_clicked(e):
        output_text.value = f"Dropdown value is:  {color_dropdown.value}"
        page.update()

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
    page.bgcolor = "#AED6F1"
    
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
    
    page.add(selectFileText, entriesRow, ontologyBoxText, search_box, color_dropdown, submit_btn, output_text, buttonRow)

ft.app(target=main)
