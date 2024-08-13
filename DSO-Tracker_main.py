#Module Imports
import math as m
import numpy as np
import json
from astropy.coordinates import EarthLocation, AltAz, ICRS, SkyCoord
from astropy.time import Time
import astropy.units as u
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os

#Script Imports
import dso_visability

#Global Declarations
root_path = os.getcwd()

#Section to configure Telscope/Camera Parameters
def create_config_gui():

    strings = ["Telescope Focal Lenght (mm)", "Telscope Mirror Diameter (mm)", "Camera pixel size X (um)", "Camera pixel size y (um)", "Pixel Count X", "Pixel Count Y"]

    global configGUI, labels, text_fields

    def cancel():
        #Close the GUI without saving
        configGUI.destroy()

    def save_date():
        #Collect data from the labels and text fields
        data = {}
        for label, entry in zip(labels, text_fields):
            data[label.cget("text")] = entry.get()

        config_filepath = os.path.join(root_path, "Configs\\equipmentConfigs.json")

        with open(config_filepath, "w") as json_file:
            json.dump(data,json_file, indent = 4)

        configGUI.destroy()

    #Define GUI Object
    configGUI = tk.Tk()
    configGUI.title("Telescope and Camera Configuration")

    #Create frame to hold text fields
    frame = tk.Frame(configGUI)
    frame.pack(padx = 10, pady = 10)

    labels = []
    text_fields = []

    flag_fill_fields = 0

    if os.path.exists(os.path.join(root_path, "Configs\\equipmentConfigs.json")):
        flag_fill_fields = 1
        config_json = os.path.join(root_path, "Configs\\equipmentConfigs.json")

        with open(config_json) as configData:
            equip_config_Data = json.load(configData)

    i = 0

    for string in strings:
        # Create a label with the text
        label = tk.Label(frame, text=string)
        label.pack(anchor='w')  # 'w' for left alignment
        labels.append(label)
        
        # Create a text field
        text_field = tk.Entry(frame, width=40)
        text_field.pack(pady=5)
        text_fields.append(text_field)

        if flag_fill_fields:
            text_field.insert(0,(list(equip_config_Data.values())[i]))
            i += 1

    button_frame = tk.Frame(configGUI)
    button_frame.pack(pady = 10)

    cancel_button = tk.Button(button_frame, text = "Cancel", command = cancel)
    cancel_button.pack(side = tk.LEFT, padx = 5)

    enter_button = tk.Button(button_frame, text = "Enter", command = save_date)
    enter_button.pack(side = tk.LEFT, padx = 5)

    #Start Tkinter event loop
    configGUI.mainloop()

def create_selection_gui():

    def select_dsos():

        root.destroy()

        if not os.path.exists(os.path.join(root_path, "Configs\\equipmentConfigs.json")):
            create_config_gui()

        open_dso_selector()
        pass

    def update_equipment():
        create_config_gui()

    def quit_gui():
        root.destroy()

    root = tk.Tk()
    root.title("DSO Selector Main Menu")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}")

    image = Image.open(os.path.join(root_path, "Support Files\\hubbleDeepField_background.jpg"))
    image = image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(root, width = screen_width, height = screen_height)
    canvas.pack(fill = "both", expand = True)

    canvas.create_image(0, 0, image = bg_image, anchor = "nw")

    title = tk.Label(root, text = "DSO Selection Tool", font = ("Helvetica", 24), bg = "grey", fg = "white")
    title_window = canvas.create_window(screen_width / 2, 50, window = title, anchor = "center")

    button1 = tk.Button(root, text = "Select Tonight's DSO's", font=("Helvetica", 16), command=select_dsos) 
    button2 = tk.Button(root, text="Update Equipment Data", font=("Helvetica", 16), command=update_equipment)
    button3 = tk.Button(root, text="Quit", font=("Helvetica", 16), command=quit_gui)

    # Place the buttons on the canvas
    button1_window = canvas.create_window(screen_width/2, screen_height/2 - 50, window=button1)
    button2_window = canvas.create_window(screen_width/2, screen_height/2, window=button2)
    button3_window = canvas.create_window(screen_width/2, screen_height/2 + 50, window=button3)

    root.mainloop()

def open_dso_selector():
    
    def load_data(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data
    
    def populate_treeview(tree, data, sort_key = None):
        #Clear existing data in the treeview
        for row in tree.get_children():
            tree.delete(row)

        if sort_key:
            dat = sorted(data, key = lambda x: x[sort_key])

        #Populate treeview with sorted data
        for index, item in enumerate(data):
            values = [item[key] for key in item.keys()]
            tree.insert("", "end", text = index, value = values)

        #Adjust column width to fit the content
        for col in tree["columns"]:
            max_width = tkfont.Font().measure(col)
            for item in tree.get_children():
                cell_value = tree.set(item, col)
                col_width = tkfont.Font().measure(cell_value)
                if max_width < col_width:
                    max_width = col_width
            tree.column(col, width = max_width)

    def on_sort_column(tree, col, reverse):
        #Sort the data and update the treeview
        sorted_data = sorted(tree_data, key = lambda x: x[col], reverse = reverse)
        populate_treeview(tree, sorted_data)
        tree.heading(col, command = lambda _col = col: on_sort_column(tree, _col, not reverse))

    def create_gui():
        global tree_data

        dso_json_file = os.path.join(root_path, "Support Files\\deep-sky-objects.json")

        #Load data from JSON File
        tree_data  = load_data(dso_json_file)
        tree_data = tree_data

        #Initialize the main window
        root = tk.Tk()
        root.title("DSO Selector")

        # Create a frame to hold the Treeview
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)

        #Create a y scrollbar
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side = "right", fill = "y")

        #Create a x scrollbar
        scrollbar_x = tk.Scrollbar(frame)
        scrollbar_x.pack(side = "bottom", fill = "y") 

        # Create the Treeview widget
        columns = list(tree_data[0].keys())
        tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set)
        tree.pack(fill="both", expand=True)

        # Add in scrollbar
        scrollbar_y.config(command = tree.yview)
        scrollbar_x.config(command = tree.xview)


        # Define headings and add sorting functionality
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: on_sort_column(tree, _col, False))

        # Populate the treeview with data
        populate_treeview(tree, tree_data)

        # Start the Tkinter event loop
        root.mainloop()

    create_gui()

create_selection_gui()































###TEMP AREA FOR CODE UNTIL I KNOW WHERE IT'LL GO

#Path to reference files
dso_Catalog_Path = "Support Files\\deep-sky-objects.json"

#Import DSO Catalog 
with open(dso_Catalog_Path) as jsonData:
    dso_All_Data = json.load(jsonData)


def getIcrsVector(lat,long, height, time):
    location = EarthLocation(lat = lat * u.deg, lon = long * u.deg, height = height * u.m)
    
    alt = 90 * u.deg
    az = 0 * u.deg

    altaz_frame = AltAz(obstime = time, location = location)

    zenith = SkyCoord(alt = alt, az = az, frame = altaz_frame)

    icrs = zenith.transform_to(ICRS)

    ra = icrs.ra.deg
    dec = icrs.dec.deg

    return ra, dec

lat, long, height = 35.053906, -106.604774, 1625

for i in range(1):
    ra, dec = getIcrsVector(lat = lat, long = long, height = height, time = Time.now())
