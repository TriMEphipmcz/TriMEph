# SPDX-License-Identifier: MIT
import sys
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QApplication, QScrollArea,  QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QFileDialog, QMessageBox, QGraphicsTextItem, QComboBox
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from scipy import interpolate
import os
import re 
import math
from scipy import constants as con
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow,  QWidget,  QLabel
from PyQt5.QtGui import QPixmap 
from numpy import polyfit, polyval
import numpy as np 



"""
@brief A custom QWidget subclass that sets its background color based on the provided color string.

This class inherits from QWidget and allows setting the background color through a valid color string 
or color code. The background color of the widget is set in the initialization method.

Methods:
    - __init__(self, color): Initializes the widget with the specified color.
"""
class ColorWidget(QWidget):  # Renamed the class to follow Python naming conventions.
    def __init__(self, color):
        """
        @brief Initializes the ColorWidget with the specified background color.
        
        This method sets the widget's background color using a given color string or 
        color code.

        @param color: A string representing the name of the color (e.g., 'red', 'blue'), 
                      or a valid hexadecimal color code (e.g., '#ff0000').

        Example usage:
            widget = ColorWidget('red')
            widget = ColorWidget('#ff0000')
        """
        super().__init__()  # Corrected to call QWidget's init, not the color.
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))  # Fixed argument to pass the string 'color'
        self.setPalette(palette)













"""
@brief A custom QGraphicsTextItem subclass that toggles its color and selection state when clicked.

This class extends QGraphicsTextItem and provides functionality for changing the text color 
and selection status upon mouse click. If the item is selected, the color changes to red; 
otherwise, it turns black.

Methods:
    - __init__(self, text): Initializes the text item with the provided text.
    - mousePressEvent(self, event): Handles the mouse click event to change the color 
      and selection status of the text item.
"""

class ClickableTextItem(QGraphicsTextItem):
    """
    @brief Initializes a clickable text item that responds to mouse clicks.

    This class allows for toggling the selection status of the text item and changing
    its color when clicked. The text item turns red when selected and black when not.
    """
    
    def __init__(self, text):
        """
        @brief Initializes the clickable text item with the specified text.
        
        The text is displayed using QGraphicsTextItem, and the color is initialized 
        to the default color (black).

        @param text: A string representing the text to display in the QGraphicsTextItem.

        Example usage:
            item = ClickableTextItem("Sample Text")
        """
        super(ClickableTextItem, self).__init__(text)

    def mousePressEvent(self, event):
        """
        @brief Handles the mouse press event. Toggles the item's selection status and color.
        
        When the item is clicked, this method toggles its selection. If the item is selected,
        it changes the text color to red. If it's deselected, the color is set to black.
        
        @param event: The QGraphicsSceneMouseEvent object representing the mouse click event.
        
        Example usage:
            # When the item is clicked, it will change its color and selection state.
            item.mousePressEvent(event)
        """
        # Get the current color of the text
        color = self.defaultTextColor()
        
        # Toggle selection and update color based on selection state
        if color == QColor("red"):
            self.setSelected(not self.isSelected())
        else:
            self.setSelected(True)
        
        # Update the text color to red if selected, or black if not
        color = QColor("red") if self.isSelected() else QColor("black")
        self.setDefaultTextColor(color)

        # Ensure that the scene updates the selection status for all items
        scene = self.scene()
        if scene:
            for item in scene.selectedItems():
                item.setSelected(self.isSelected())









"""
@brief A custom QMainWindow subclass that serves as the main application window.

This class is designed for complex GUI applications, providing attributes for file 
management, data handling, and graphical representation. It creates the foundation 
for building the user interface, handling user interaction, and managing various data-related tasks.

Methods:
    - __init__(self): Initializes the main window, sets up the UI, and 
      initializes various attributes for file and data management.
    - initUI(self): Placeholder method for initializing additional UI elements.
"""

class my_window(QMainWindow):
    """
    @brief Main window class for the TriMEph application.

    This class is the main application window for the TriMEph GUI. It initializes the 
    window with specific attributes, like the window title, size, tooltip, and icon. 
    It also provides placeholders for adding more UI elements and functionalities.
    """

    def __init__(self):
        """
        @brief Initializes the main application window with default settings.

        This constructor sets the geometry, window title, tooltip, and icon. It also 
        provides the base for further customization and expansion, including managing 
        files, data handling, and graphical user interface elements.

        Example usage:
            window = my_window()
            window.show()

        Attributes:
            - setGeometry: Defines the position and size of the window (1920x1080).
            - setWindowTitle: Sets the title of the main window to 'TriMEph'.
            - setToolTip: Adds a tooltip with the message 'TriMEph'.
            - setWindowIcon: Sets the window icon using a local file ('Logo.jpg').
            file_positions (dict):
            Maps file names or paths to their positions in the current list.
        loaded_files1 (list[str]), loaded_files2 (list[str]), loaded_files3 (list[str]),
        loaded_files4 (list[str]), loaded_files5 (list[str]):
            Lists of files loaded from five different input sources.
        text_item1 (list[QGraphicsTextItem]), text_item2 (list[QGraphicsTextItem]),
        text_item3 (list[QGraphicsTextItem]), text_item4 (list[QGraphicsTextItem]):
            Lists of text graphic items for various layers/views.
        files_to_delete (list[str]):
            Paths of files scheduled for deletion.
        ev_vol_list (list[float]), temp_list (list[float]), volume_list (list[float]),
        real_temp (list[float]):
            Lists of measured or calculated data: evaporation volumes, temperatures, and actual temperatures.
        outfile (list[Any]), outfile_names (list[str]):
            Output file objects and their corresponding names for further processing or saving.
        mx, my, mz, mx1, my1, mz1, mx2, my2, mz2 (list[float]):
            Sets of X, Y, Z coordinates for different computation or display phases.
        data_list (list[Any]):
            Collection of all loaded or generated data objects.
        result (list[Any]):
            Temporary computation results.
        count (list[int]):
            Counters or record indices.
        factor_list (list[float]):
            List of normalization or scaling factors.
        generated_graphs_factor (list[QPixmap]), generated_graphs_mi1 (list[QPixmap]):
            Rendered graph objects for factors and the first set of mi values.
        atom_names (list[str]), atom_numbers (list[int]), atom_masses (list[float]),
        Er_const_list (list[float]):
            Atomic property parameters and constants used in energy calculations.
        sing_temperature (list[float]), sing_mx (list[float]), sing_my (list[float]),
        sing_mz (list[float]):
            Lists for singular temperatures and individual coordinates during analysis.
        x_axis (list[float]), y_axis (list[float]), xAxis (list[float]), yAxis (list[float]):
            X and Y axes data for plotting; duplicate names retained for backward compatibility.
        factor_stored_kwargs_f (dict):
            Dictionary holding stored keyword arguments for factor graph generation.
        mx1_stored_kwargs, my1_stored_kwargs, mz1_stored_kwargs (dict):
            Dictionaries holding stored keyword arguments for mx1, my1, and mz1 computations.
        i (int):
            Index or flag used in iterations or processing steps.
        """
        super(my_window, self).__init__()
        self.setGeometry(0 ,0 ,1920 ,1080 )
        self.setWindowTitle("TriMEph")
        self.setToolTip("TriMEph")
        self.setWindowIcon(QIcon("Logo.jpg"))

        # Initialize UI components
        self.initUI()
        # Initialize file handling attributes
        self.file_positions = {}  # A dictionary to store file positions

        # Initialize lists for different sets of loaded files
        self.loaded_files1 = []  
        self.loaded_files2 = []  
        self.loaded_files3 = []  
        self.loaded_files4 = []  
        self.loaded_files5 = []  

        # Initialize text item lists
        self.text_item1 = []
        self.text_item2 = []
        self.text_item3 = []
        self.text_item4 = []

        # Initialize list for files to delete
        self.files_to_delete = []  

        # Initialize lists for volume, temperature, and real-time data
        self.ev_vol_list = []  
        self.temp_list = []  
        self.volume_list = []  
        self.real_temp = []  

        # Initialize lists for output files and their names
        self.outfile = []  
        self.outfile_names = []  

        # Initialize lists for axis data (mx, my, mz)
        self.mx = []  
        self.my = []  
        self.mz = []  

        # Initialize a list for general data
        self.data_list_x = []  
        self.data_list_y = []  
        self.data_list_z = []  

        

        self.fit_list_x_temp_ordered = []
        self.fit_list_y_temp_ordered = []
        self.fit_list_z_temp_ordered = [] # bud eto cca takto [[prvy TD prvy riadok pre T=0,natom=0],[prvy TD prvy riadok pre T=0,natom=1]...[prvy TD prvy riadok pre T=1,natom=0]...  ]

        self.coef_x = []
        self.coef_y = []
        self.coef_z = []

        # Initialize a list for single thermal displacement approximation
        self.data_sing_list = []

        # Initialize a list for computation results
        self.result = []  

        # Initialize lists for counting purposes
        self.count = []  

        
        # Additional axis data lists (mx2, my2, mz2 and mx1, my1, mz1)
        self.mx2 = []  
        self.my2 = []  
        self.mz2 = []  
        self.mx1 = []  
        self.my1 = []  
        self.mz1 = []  

        # Initialize list for factors
        self.factor_list = []  

        # Initialize lists for generated graphs data
        self.generated_graphs_factor = []  
        self.generated_graphs_mi1 = []  

        # Initialize lists for atom data (names, numbers, masses)
        self.atom_names = []  
        self.atom_numbers = []  
        self.atom_masses = []  
        self.Er_const_list = []  

        # Initialize lists for single data points (temperature, mx, my, mz)
        self.sing_temperature = []  
        self.sing_mx = []  
        self.sing_my = []  
        self.sing_mz = []  

        # Initialize axis data lists for plots
        self.y_axis = []  
        self.x_axis = []  

        # Initialize dictionaries for storing keyword arguments
        self.factor_stored_kwargs_f = {}  
        self.mx1_stored_kwargs = {}  
        self.my1_stored_kwargs = {}  
        self.mz1_stored_kwargs = {}  

        # Initialize plot axes lists
        self.xAxis = []  
        self.yAxis = []  

        # Initialize an integer for counting purposes
        self.i = 1  

        # Set the exception hook to handle uncaught exceptions
        #sys.excepthook = self.exception_hook

        
    def initUI(self):
        """
        @brief Initializes the user interface (UI) for the main application window.

        This method sets up the layout, widgets, and their functionalities. It organizes the 
        UI components within a scrollable area, allowing users to upload and process various data files, 
        interact with graphical data, and customize plot settings.

        UI Components:
            - QScrollArea: A scrollable area that contains all other widgets.
            - QWidget: The main widget within the scroll area where all UI components are placed.
            - QLabel: Used for displaying static text and images, such as background images and instructions.
            - QPushButton: Buttons that trigger various actions like uploading files, deleting files, 
            processing data, and saving results.
            - QGraphicsView: Views for displaying graphics or images related to uploaded files and processed data.
            - QComboBox: Dropdown boxes for selecting options like plot style, color, marker, and resolution.

        Widgets and Functionalities:
            - **Background Image**: Displays a background image in the main widget to enhance the visual design.
            - **Documentation Button**: Opens a help dialog or the application's documentation when clicked.
            - **Labels and Upload Buttons**: Each section contains labels that describe the required data files 
            and corresponding buttons for uploading the files.
            - **Delete Buttons**: Buttons that allow users to delete uploaded files from the interface.
            - **Graphics Views**: Placeholder areas where visual representations of the uploaded and processed 
            data are displayed.
            - **Processing and Saving Buttons**: Buttons that allow users to process the uploaded data and 
            save the results as graphs or exported files.
            - **Plotting Controls**: Combo boxes that enable users to select details for plotting graphs, 
            such as color schemes, marker styles, and resolution.
            - **Central Widget**: The entire scrollable area containing all the widgets is set as the 
            central widget of the main window, allowing users to interact with the UI components effectively.
        
        @note This method can be further extended to add custom logic and functionality to each UI element.
        """
        

       
        
            # Initialize the scrollable area and main widget
        self.scroll = QScrollArea()          
        self.widget = QWidget() 
        self.widget.resize(1920, 1080) 
        self.scroll.setWidget(self.widget)

        # Add a background image to the main widget
        pixmap = QPixmap("backround.png")  
        background_label = QLabel(self.widget)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        # Documentation button
        self.btn_documentation = QtWidgets.QPushButton(self.widget)
        self.btn_documentation.setText("?")
        self.btn_documentation.move(10,10)
        self.btn_documentation.setStyleSheet("font-size: 40px")
        self.btn_documentation.resize(160,75)
        self.btn_documentation.clicked.connect(self.open_documentation)

        # Instruction label for uploading files
        self.txt_updload_files = QtWidgets.QLabel(self.widget)
        self.txt_updload_files.setText("Please Upload Following Data:")
        self.txt_updload_files.move(180,20)
        self.txt_updload_files.setStyleSheet("font-size: 16px")

        # Section for uploading the Phonopy.yaml file
        self.txt_name = QtWidgets.QLabel(self.widget) 
        self.txt_name.setText("Phonopy.yaml file:")
        self.txt_name.move(180, 55)
        self.txt_name.setStyleSheet("font-size: 15px")
        
        self.btn_name = QtWidgets.QPushButton(self.widget)
        self.btn_name.setText("Upload")
        self.btn_name.resize(100,30)
        self.btn_name.move(370, 50)
        self.btn_name.setStyleSheet("background-color: lightgreen; border: 1px solid black; font-size: 16px;")
        self.btn_name.clicked.connect(self.openFileDialog1)

        self.graphics_load1 = QGraphicsView(self.widget)
        self.graphics_load1.move(180,90)
        self.graphics_load1.resize(400,200)

        # Button to delete the uploaded Phonopy.yaml file
        self.btn_1delete = QtWidgets.QPushButton(self.widget)
        self.btn_1delete.setText("Delete")
        self.btn_1delete.move(480, 50)
        self.btn_1delete.resize(100,30)
        self.btn_1delete.setStyleSheet("background-color: red; border: 1px solid black; font-size: 16px;")
        self.btn_1delete.clicked.connect(self.DeleteLoadedFiles1)

        # Section for uploading Thermal Displacements Files
        self.txt_2name = QtWidgets.QLabel(self.widget)
        self.txt_2name.setText("Thermal Displacements Files:")
        self.txt_2name.move(180, 305)
        self.txt_2name.setStyleSheet("font-size: 15px")  

        self.btn_2name = QtWidgets.QPushButton(self.widget)
        self.btn_2name.setText("Upload")
        self.btn_2name.move(370, 300)
        self.btn_2name.resize(100,30)
        self.btn_2name.setStyleSheet("background-color: lightgreen; border: 1px solid black; font-size: 16px;")
        self.btn_2name.clicked.connect(self.openFileDialog2)

        self.graphics_load2 = QGraphicsView(self.widget)
        self.graphics_load2.move(180,340)
        self.graphics_load2.resize(400,200)

        # Button to delete the uploaded Thermal Displacements Files
        self.btn_2delete = QtWidgets.QPushButton(self.widget)
        self.btn_2delete.setText("Delete")
        self.btn_2delete.move(480, 300)
        self.btn_2delete.resize(100,30)
        self.btn_2delete.setStyleSheet("background-color: red; border: 1px solid black; font-size: 16px;")
        self.btn_2delete.clicked.connect(self.DeleteLoadedFiles2)

        # Section for uploading Volume - Temperature File
        self.txt_3name = QtWidgets.QLabel(self.widget)
        self.txt_3name.setText("Volume - Temperature File:")
        self.txt_3name.move(180, 555)
        self.txt_3name.setStyleSheet("font-size: 15px")

        self.btn_3name = QtWidgets.QPushButton(self.widget)
        self.btn_3name.setText("Upload")
        self.btn_3name.move(370, 550)
        self.btn_3name.resize(100,30)
        self.btn_3name.setStyleSheet("background-color: lightgreen; border: 1px solid black; font-size: 16px;")
        self.btn_3name.clicked.connect(self.openFileDialog3)

        self.graphics_load3 = QGraphicsView(self.widget)
        self.graphics_load3.move(180, 590)
        self.graphics_load3.resize(400,200)

        # Button to delete the uploaded Volume - Temperature File
        self.btn_3delete = QtWidgets.QPushButton(self.widget)
        self.btn_3delete.setText("Delete")
        self.btn_3delete.move(480, 550)
        self.btn_3delete.resize(100,30)
        self.btn_3delete.setStyleSheet("background-color: red; border: 1px solid black; font-size: 16px;")
        self.btn_3delete.clicked.connect(self.DeleteLoadedFiles3)

        # Section for uploading e-V File
        self.txt_4name = QtWidgets.QLabel(self.widget)
        self.txt_4name.setText("e-V File:")
        self.txt_4name.move(180, 805)
        self.txt_4name.setStyleSheet("font-size: 15px")

        self.btn_4name = QtWidgets.QPushButton(self.widget)
        self.btn_4name.setText("Upload")
        self.btn_4name.move(370, 800)
        self.btn_4name.resize(100,30)
        self.btn_4name.setStyleSheet("background-color: lightgreen; border: 1px solid black; font-size: 16px;")
        self.btn_4name.clicked.connect(self.openFileDialog4)

        self.graphics_load4 = QGraphicsView(self.widget)
        self.graphics_load4.move(180, 840)
        self.graphics_load4.resize(400,150)

        # Button to delete the uploaded e-V File
        self.btn_4delete = QtWidgets.QPushButton(self.widget)
        self.btn_4delete.setText("Delete")
        self.btn_4delete.move(480, 800)
        self.btn_4delete.resize(100,30)
        self.btn_4delete.setStyleSheet("background-color: red; border: 1px solid black; font-size: 16px;")
        self.btn_4delete.clicked.connect(self.DeleteLoadedFiles4)
            





        self.btn_process = QtWidgets.QPushButton(self.widget)
        self.btn_process.setText("Process")
        self.btn_process.move( 1600 , 600)
        self.btn_process.resize(100,50)
        self.btn_process.clicked.connect(self.PROCESSING)

        self.btn_save = QtWidgets.QPushButton(self.widget)
        self.btn_save.setText("Save Graph")
        self.btn_save.move( 1600 , 660)
        self.btn_save.resize(100,50)
        self.btn_save.clicked.connect(self.saveDisplayedFigure)

        self.btn_savetex = QtWidgets.QPushButton(self.widget)
        self.btn_savetex.setText("Save Tex.")
        self.btn_savetex.move(1600, 720 )
        self.btn_savetex.resize( 100, 50)
        self.btn_savetex.clicked.connect(self.Save_file)

        self.btn_Ploting = QtWidgets.QPushButton(self.widget)
        self.btn_Ploting.setText("Graph")
        self.btn_Ploting.move(1000, 600)
        self.btn_Ploting.resize(100,50)
        self.btn_Ploting.clicked.connect(self.Ploting)

        self.btn_Expdata = QtWidgets.QPushButton(self.widget)
        self.btn_Expdata.setText("Input\nExperimental\nData")
        self.btn_Expdata.setStyleSheet("text-align: center;")
        self.btn_Expdata.move( 1120 , 600)
        self.btn_Expdata.resize(100,50)
        self.btn_Expdata.clicked.connect(self.openFileDialog5)
            
        self.btn_ClearExpdata = QtWidgets.QPushButton(self.widget)
        self.btn_ClearExpdata.setText("Clear\nExperimental\nData")
        self.btn_ClearExpdata.setStyleSheet("text-align: center;")
        self.btn_ClearExpdata.move( 1240 , 600)
        self.btn_ClearExpdata.resize(100,50)
        self.btn_ClearExpdata.clicked.connect(self.ClearingExpData)
            
            
        self.graphics_graph = QGraphicsView(self.widget)
        self.graphics_graph.move(1000,80)
        self.graphics_graph.resize(700,500)
        self.graphics_graph.setInteractive(True)
            
        
        
        
        
        
        
        
        
        
        
        
        self.Box = QComboBox(self.widget)
        self.Box.move(1000, 50)
        self.Box.addItem(f"Atom Probability {1}")
        self.Box.addItem(f"Atom MSD {1}")
        
 
        self.ChooseWhich = QComboBox(self.widget)
        self.ChooseWhich.move(1140, 50)
        self.ChooseWhich.addItem("Factor")
        self.ChooseWhich.addItem("x^2")
        self.ChooseWhich.addItem("y^2")
        self.ChooseWhich.addItem("z^2")

        
        self.box_colors = QComboBox(self.widget)
        self.box_colors.move(1210, 50)
        self.box_colors.addItem('Colors')
        self.box_colors.addItem('Black')
        self.box_colors.addItem('Red')
        self.box_colors.addItem('Green')
        self.box_colors.addItem('Blue')
        self.box_colors.addItem('Yellow')
        self.box_colors.addItem('Orange')
        self.box_colors.addItem('Purple')

        self.box_linestyle = QComboBox(self.widget)
        self.box_linestyle.move(1290,50)
        self.box_linestyle.addItem('Linestyle')
        self.box_linestyle.addItem('solid')
        self.box_linestyle.addItem('dashed')
        self.box_linestyle.addItem('dashdot')
        self.box_linestyle.addItem('dotted')
        
        
        
        
        self.box_linewidth = QComboBox(self.widget)
        self.box_linewidth.move(1375,50)
        self.box_linewidth.addItem('Linewidth')
        self.box_linewidth.addItem('1')
        self.box_linewidth.addItem('2')
        self.box_linewidth.addItem('3')
        self.box_linewidth.addItem('4')
        self.box_linewidth.addItem('5')
        self.box_linewidth.addItem('6')
        self.box_linewidth.addItem('7')
        self.box_linewidth.addItem('8')
        self.box_linewidth.addItem('9')
        self.box_linewidth.addItem('10')
        self.box_linewidth.addItem('11')
        self.box_linewidth.addItem('12')


        self.box_markers = QComboBox(self.widget)
        self.box_markers.move(1465, 50 )
        self.box_markers.addItem('Markers')
        self.box_markers.addItem('none')
        self.box_markers.addItem('Circle')
        self.box_markers.addItem('Square')
        self.box_markers.addItem('Triangle')

        self.box_resolution = QComboBox(self.widget)
        self.box_resolution.move(1548, 50 )
        self.box_resolution.addItem('Resolution')
        self.box_resolution.addItem('720x480')
        self.box_resolution.addItem('1280x720')
        self.box_resolution.addItem('1920x1080 ')





        
        self.scene_load1 = None
        self.scene_load2 = None
        self.scene_load3 = None
        self.scene_load4 = None

        self.graphics_graph.setScene(QGraphicsScene())

        
        self.fit_list_x= []
        self.fit_list_y = []
        self.fit_list_z = []
        
        self.setCentralWidget(self.scroll)


    

    def open_documentation(self):
        """
        @brief Opens the documentation PDF file associated with the application.

        This method opens the specified PDF file using the default PDF viewer on the user's system.
        The file path is hardcoded and should be updated as necessary. The method includes exception 
        handling to manage any errors that occur during the file opening process.

        File Path:
            - pdf_file_path (str): The file path to the documentation PDF file.
        
        Error Handling:
            - If the file cannot be opened, the method catches the exception and prints an error message.

        Example usage:
            self.open_documentation()

        Raises:
            - Catches and prints any exceptions raised during the file opening process.
        """
        pdf_file_path = "User Manual.pdf"  
        
        try:
            os.startfile(pdf_file_path)
        except Exception as e:
            print("Error:", e)
        
  
    
    
    def GenerateComboBox(self):
        """
        @brief Populates the `Box` QComboBox with options based on the number of atoms.

        This method first clears the existing items in the `Box` combo box and then adds new items dynamically. 
        For each atom in the range from 1 to `n`, where `n` is the last element of the `atom_numbers` list, 
        two items are added to the combo box: one for "Atom Probability" and one for "Atom MSD".
        
        After populating the combo box, the method connects the `currentIndexChanged` signal of the combo box 
        to the `Choosing` method, which is responsible for handling selection changes.

        Modifies:
            - self.Box (QComboBox): The combo box that gets populated with new items.

        Attributes:
            - atom_numbers (list): A list of atom numbers, where the last element determines the number of items added.
        
        Connections:
            - `self.Box.currentIndexChanged`: Connects the combo box selection change signal to the `Choosing` method.
        
        Usage:
            - Call this method when the list of `atom_numbers` is updated or when the UI needs to be refreshed 
            to reflect the current state of the atoms data.
        
        Example usage:
            self.GenerateComboBox()

        """
        self.Box.clear()
        n = self.atom_numbers[-1]
        for i in range(1, n  +1):
            self.Box.addItem(f"Atom Probability {i}")
            self.Box.addItem(f"Atom MSD {i}")
        self.Box.currentIndexChanged.connect(self.Choosing)
    


    def combo_box_selection_changed(self, index):
        """
        @brief Updates the displayed figure when the combo box selection changes.

        This method is triggered when the user selects a different item from the combo box.
        It updates the figure displayed in the UI by calling the `display_figure` method and passing
        the selected index.

        Parameters:
            - index (int): The index of the selected item in the combo box.

        Action:
            - Calls the `display_figure(index)` method to update the displayed figure based on the selected combo box item.

        Example usage:
            self.combo_box_selection_changed(index)
        """
        self.display_figure(index)
  


    def openFileDialog1(self):
        """
        @brief Opens a file dialog for selecting files to upload and displays the selected files in a graphics view.

        This method opens a file dialog to allow the user to select one or more files for uploading. It then adds the 
        selected files to `self.loaded_files1` and displays their names in `self.graphics_load1`. If a file has 
        already been uploaded, it is skipped and the user is notified. Scroll bars are adjusted based on the 
        number of loaded files.

        Functionality:
            - Opens a file dialog for the user to select files.
            - Adds new files to `self.loaded_files1` and skips duplicates.
            - Displays the names of the loaded files in the graphics view (`self.graphics_load1`).
            - Adjusts the scroll bar policies depending on the number of items displayed.

        Parameters:
            - None

        Operations:
            - Displays a file dialog for selecting files.
            - Checks for duplicate files and alerts the user if a file is already loaded.
            - Updates the `QGraphicsView` with the names of newly loaded files.
            - Adjusts scroll bars in `self.graphics_load1` based on the number of items displayed.

        UI Components:
            - `QFileDialog`: Opens a dialog for selecting files.
            - `QGraphicsView`: Displays the names of the uploaded files.
            - `QMessageBox`: Notifies the user about duplicate file selections or missing files.

        Edge Cases:
            - Alerts the user if no files are selected.
            - Manages horizontal and vertical scroll bars based on the number of files displayed.

        Example usage:
            self.openFileDialog1()
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files for Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        

        
        double_files = []
        total_width = 0
        file_pos = 0
        
        if file_names:
            for file_name in file_names:
                if file_name not in self.loaded_files1: 
                    self.loaded_files1.append(file_name)
                    self.displayFileName(file_name, self.graphics_load1, file_pos)
                    file_pos += 20
                    for item in self.scene_load1.items():
                        if isinstance(item, QGraphicsTextItem):
                            item.setPos(0, file_pos)
                            file_pos += 20
                            for index, item in enumerate(self.scene_load1.items()):   
                                if isinstance(item, QGraphicsTextItem):
                                    item.setPos(0, index*20)
                        for item in self.scene_load1.items():
                            if isinstance(item, QGraphicsTextItem):
                                total_width += item.boundingRect().width()
                
                else: 
                    double_files.append(file_name)
                          
            
            
            if len(double_files) == 1:
                    QMessageBox.information(self, "File Already Loaded", f"The file '{double_files[0]}' is already loaded.")
            elif len(double_files) > 1:
                QMessageBox.information(
                    self, "Files Already Loaded", f"The following files are already loaded:\n{', '.join(double_files)}"
                    )             
            

            visible_horizontal = (self.graphics_load1.viewport().width() - self.graphics_load1.contentsMargins().left() - self.graphics_load1.contentsMargins().right()) // total_width
            visible_vertical = (self.graphics_load1.viewport().height() - self.graphics_load1.contentsMargins().top() - self.graphics_load1.contentsMargins().bottom())//10
            
            
            if len(self.loaded_files1) <= visible_vertical:
                self.graphics_load1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load1.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files1) <= visible_horizontal:
                self.graphics_load1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load1.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load1.update()

        else:
            QMessageBox.information(self, "No Files Selected", "No files were selected.")

    def openFileDialog2(self):
        """
        @brief Opens a file dialog for selecting files to upload and displays the selected files in a graphics view.

        This method opens a file dialog to allow the user to select one or more files for uploading. It then adds the 
        selected files to `self.loaded_files2` and displays their names in `self.graphics_load2`. If a file has 
        already been uploaded, it is skipped and the user is notified. Scroll bars are adjusted based on the 
        number of loaded files.

        Functionality:
            - Opens a file dialog for the user to select files.
            - Adds new files to `self.loaded_files2` and skips duplicates.
            - Displays the names of the loaded files in the graphics view (`self.graphics_load2`).
            - Adjusts the scroll bar policies depending on the number of items displayed.

        Parameters:
            - None

        Operations:
            - Displays a file dialog for selecting files.
            - Checks for duplicate files and alerts the user if a file is already loaded.
            - Updates the `QGraphicsView` with the names of newly loaded files.
            - Adjusts scroll bars in `self.graphics_load1` based on the number of items displayed.

        UI Components:
            - `QFileDialog`: Opens a dialog for selecting files.
            - `QGraphicsView`: Displays the names of the uploaded files.
            - `QMessageBox`: Notifies the user about duplicate file selections or missing files.

        Edge Cases:
            - Alerts the user if no files are selected.
            - Manages horizontal and vertical scroll bars based on the number of files displayed.

        Example usage:
            self.openFileDialog2()
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files for Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        

        double_files = []
        total_width = 0
        file_pos = 0
        
        if file_names:
            for file_name in file_names:
                if file_name not in self.loaded_files2:  
                    self.loaded_files2.append(file_name)
                    self.displayFileName(file_name, self.graphics_load2, file_pos)
                    file_pos += 20
                    for item in self.scene_load2.items():
                        if isinstance(item, QGraphicsTextItem):
                            item.setPos(0, file_pos)
                            file_pos += 20
                            for index, item in enumerate(self.scene_load2.items()):     
                                if isinstance(item, QGraphicsTextItem):
                                    item.setPos(0, index*20)
                        for item in self.scene_load2.items():
                            if isinstance(item, QGraphicsTextItem):
                                total_width += item.boundingRect().width()
                
                else: 
                    double_files.append(file_name)
                          
            
            
            if len(double_files) == 1:
                    QMessageBox.information(self, "File Already Loaded", f"The file '{double_files[0]}' is already loaded.")
            elif len(double_files) > 1:
                QMessageBox.information(
                    self, "Files Already Loaded", f"The following files are already loaded:\n{', '.join(double_files)}"
                    )             
            

            visible_horizontal = (self.graphics_load2.viewport().width() - self.graphics_load2.contentsMargins().left() - self.graphics_load2.contentsMargins().right()) // total_width
            visible_vertical = (self.graphics_load2.viewport().height() - self.graphics_load2.contentsMargins().top() - self.graphics_load2.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files2) <= visible_vertical:
                self.graphics_load2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files2) <= visible_horizontal:
                self.graphics_load2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load2.update()

        else:
            QMessageBox.information(self, "No Files Selected", "No files were selected.")


    def openFileDialog3(self):
        """
        @brief Opens a file dialog for selecting files to upload and displays the selected files in a graphics view.

        This method opens a file dialog to allow the user to select one or more files for uploading. It then adds the 
        selected files to `self.loaded_files3` and displays their names in `self.graphics_load3`. If a file has 
        already been uploaded, it is skipped and the user is notified. Scroll bars are adjusted based on the 
        number of loaded files.

        Functionality:
            - Opens a file dialog for the user to select files.
            - Adds new files to `self.loaded_files3` and skips duplicates.
            - Displays the names of the loaded files in the graphics view (`self.graphics_load3`).
            - Adjusts the scroll bar policies depending on the number of items displayed.

        Parameters:
            - None

        Operations:
            - Displays a file dialog for selecting files.
            - Checks for duplicate files and alerts the user if a file is already loaded.
            - Updates the `QGraphicsView` with the names of newly loaded files.
            - Adjusts scroll bars in `self.graphics_load1` based on the number of items displayed.

        UI Components:
            - `QFileDialog`: Opens a dialog for selecting files.
            - `QGraphicsView`: Displays the names of the uploaded files.
            - `QMessageBox`: Notifies the user about duplicate file selections or missing files.

        Edge Cases:
            - Alerts the user if no files are selected.
            - Manages horizontal and vertical scroll bars based on the number of files displayed.

        Example usage:
            self.openFileDialog3()
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files for Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        

        
        double_files = []
        total_width = 0
        file_pos = 0
        
        if file_names:
            for file_name in file_names:
                if file_name not in self.loaded_files3:  
                    self.loaded_files3.append(file_name)
                    self.displayFileName(file_name, self.graphics_load3, file_pos)
                    file_pos += 20
                    for item in self.scene_load3.items():
                        if isinstance(item, QGraphicsTextItem):
                            item.setPos(0, file_pos)
                            file_pos += 20
                            for index, item in enumerate(self.scene_load3.items()):     
                                if isinstance(item, QGraphicsTextItem):
                                    item.setPos(0, index*20)
                        for item in self.scene_load3.items():
                            if isinstance(item, QGraphicsTextItem):
                                total_width += item.boundingRect().width()
                
                else: 
                    double_files.append(file_name)
                          
            
            
            if len(double_files) == 1:
                    QMessageBox.information(self, "File Already Loaded", f"The file '{double_files[0]}' is already loaded.")
            elif len(double_files) > 1:
                QMessageBox.information(
                    self, "Files Already Loaded", f"The following files are already loaded:\n{', '.join(double_files)}"
                    )             
            

            visible_horizontal = (self.graphics_load3.viewport().width() - self.graphics_load3.contentsMargins().left() - self.graphics_load3.contentsMargins().right()) // total_width
            visible_vertical = (self.graphics_load3.viewport().height() - self.graphics_load3.contentsMargins().top() - self.graphics_load3.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files3) <= visible_vertical:
                self.graphics_load3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load3.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files3) <= visible_horizontal:
                self.graphics_load3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load3.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load3.update()

        else:
            QMessageBox.information(self, "No Files Selected", "No files were selected.")

    def openFileDialog4(self):
        """
        @brief Opens a file dialog for selecting files to upload and displays the selected files in a graphics view.

        This method opens a file dialog to allow the user to select one or more files for uploading. It then adds the 
        selected files to `self.loaded_files4` and displays their names in `self.graphics_load4`. If a file has 
        already been uploaded, it is skipped and the user is notified. Scroll bars are adjusted based on the 
        number of loaded files.

        Functionality:
            - Opens a file dialog for the user to select files.
            - Adds new files to `self.loaded_files4` and skips duplicates.
            - Displays the names of the loaded files in the graphics view (`self.graphics_load4`).
            - Adjusts the scroll bar policies depending on the number of items displayed.

        Parameters:
            - None

        Operations:
            - Displays a file dialog for selecting files.
            - Checks for duplicate files and alerts the user if a file is already loaded.
            - Updates the `QGraphicsView` with the names of newly loaded files.
            - Adjusts scroll bars in `self.graphics_load4` based on the number of items displayed.

        UI Components:
            - `QFileDialog`: Opens a dialog for selecting files.
            - `QGraphicsView`: Displays the names of the uploaded files.
            - `QMessageBox`: Notifies the user about duplicate file selections or missing files.

        Edge Cases:
            - Alerts the user if no files are selected.
            - Manages horizontal and vertical scroll bars based on the number of files displayed.

        Example usage:
            self.openFileDialog4()
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files for Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        

        
        double_files = []
        total_width = 0
        file_pos = 0
        
        if file_names:
            for file_name in file_names:
                if file_name not in self.loaded_files4:  
                    self.loaded_files4.append(file_name)
                    self.displayFileName(file_name, self.graphics_load4, file_pos)
                    file_pos += 20
                    for item in self.scene_load4.items():
                        if isinstance(item, QGraphicsTextItem):
                            item.setPos(0, file_pos)
                            file_pos += 20
                            for index, item in enumerate(self.scene_load4.items()):    
                                if isinstance(item, QGraphicsTextItem):
                                    item.setPos(0, index*20)
                        for item in self.scene_load4.items():
                            if isinstance(item, QGraphicsTextItem):
                                total_width += item.boundingRect().width()
                
                else: 
                    double_files.append(file_name)
                          
            
            
            if len(double_files) == 1:
                    QMessageBox.information(self, "File Already Loaded", f"The file '{double_files[0]}' is already loaded.")
            elif len(double_files) > 1:
                QMessageBox.information(
                    self, "Files Already Loaded", f"The following files are already loaded:\n{', '.join(double_files)}"
                    )             
            

            visible_horizontal = (self.graphics_load4.viewport().width() - self.graphics_load4.contentsMargins().left() - self.graphics_load4.contentsMargins().right()) // total_width
            visible_vertical = (self.graphics_load4.viewport().height() - self.graphics_load4.contentsMargins().top() - self.graphics_load4.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files4) <= visible_vertical:
                self.graphics_load4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load4.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files4) <= visible_horizontal:
                self.graphics_load4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load4.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load4.update()

        else:
            QMessageBox.information(self, "No Files Selected", "No files were selected.")


    def openFileDialog5(self):
        """
        @brief Opens a file dialog for selecting files to upload and displays the selected files in a graphics view.

        This method opens a file dialog to allow the user to select one or more files for uploading. It then adds the 
        selected files to `self.loaded_files5` and displays their names in `self.graphics_load5`. If a file has 
        already been uploaded, it is skipped and the user is notified. Scroll bars are adjusted based on the 
        number of loaded files.

        Functionality:
            - Opens a file dialog for the user to select files.
            - Adds new files to `self.loaded_files5` and skips duplicates.
            - Displays the names of the loaded files in the graphics view (`self.graphics_load5`).
            - Adjusts the scroll bar policies depending on the number of items displayed.

        Parameters:
            - None

        Operations:
            - Displays a file dialog for selecting files.
            - Checks for duplicate files and alerts the user if a file is already loaded.
            - Updates the `QGraphicsView` with the names of newly loaded files.
            - Adjusts scroll bars in `self.graphics_load1` based on the number of items displayed.

        UI Components:
            - `QFileDialog`: Opens a dialog for selecting files.
            - `QGraphicsView`: Displays the names of the uploaded files.
            - `QMessageBox`: Notifies the user about duplicate file selections or missing files.

        Edge Cases:
            - Alerts the user if no files are selected.
            - Manages horizontal and vertical scroll bars based on the number of files displayed.

        Example usage:
            self.openFileDialog5()
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files for Upload", "", "All Files (*);;Text Files (*.txt)", options=options)
        double_files = []

   
        if file_names:
            for file_name in file_names:
                if len(self.loaded_files5) == 0:
                    if file_name not in self.loaded_files5:  
                        self.loaded_files5.append(file_name)
                    else:
                        double_files.append(file_name)
                elif len(self.loaded_files5) == 1:
                    QMessageBox.information(self,"File Already Loaded", f"The file '{self.loaded_files5[0]}' is loaded. Clear experimental data for further use.")
                else:
                    self.loaded_files5.clear()
        
        
        
        if len(double_files) == 1:
            QMessageBox.information(self, "File Already Loaded", f"The file '{double_files[0]}' is loaded. Can not load the same file twice.")
        elif len(double_files) > 1:
            return
        self.OpenExperimentalData()
    
    def OpenExperimentalData(self):
        """
        @brief Opens and processes experimental data files.

        This method reads the files listed in `self.loaded_files5`. Each file is expected to contain two columns 
        of numerical data, with the first column corresponding to the X-axis and the second column corresponding 
        to the Y-axis. The method reads the data from each file, appends the X-axis values to `self.xAxis`, and 
        the Y-axis values to `self.yAxis`.

        Attributes:
            - self.loaded_files5 (list of str): A list of file paths that will be processed.
            - self.xAxis (list of float): A list that stores the X-axis data extracted from the files.
            - self.yAxis (list of float): A list that stores the Y-axis data extracted from the files.

        Functionality:
            - Reads and processes data files listed in `self.loaded_files5`.
            - Appends the first column of each file to `self.xAxis` and the second column to `self.yAxis`.

        Edge Cases:
            - Handles any file reading errors, such as incorrectly formatted files, and notifies the user of any issues.
        
        Example usage:
            self.OpenExperimentalData()
        """
        for file_name in self.loaded_files5:
            with open(file_name, 'r') as data:        
                for line in data:
                    p = line.split()
                    self.xAxis.append(float(p[0]))
                    self.yAxis.append(float(p[1]))


    def ClearingExpData(self):
        """
        @brief Clears all experimental data.

        This method clears the lists that store the experimental data and associated file paths. Specifically, 
        it empties `self.loaded_files5`, which holds the file paths of the loaded experimental data files, and 
        also clears `self.xAxis` and `self.yAxis`, which store the X-axis and Y-axis data points.

        Attributes:
            - self.loaded_files5 (list of str): List containing the file paths of the loaded experimental data files.
            - self.xAxis (list of float): List storing the X-axis data points from the experimental data.
            - self.yAxis (list of float): List storing the Y-axis data points from the experimental data.

        Example usage:
            self.clear_experimental_data()

        """
        self.loaded_files5.clear()
        self.xAxis.clear()
        self.yAxis.clear()

        
    def displayMatplotlibFigure(self, figure):
        """
        @brief Displays a Matplotlib figure in a Qt graphics view.

        This method takes a Matplotlib figure, converts it into a canvas, and displays it within 
        a `QGraphicsView` widget (`self.graphics_graph`). It clears the existing content in the 
        scene, creates a new scene with the Matplotlib figure, and then sets the new scene 
        in the view for display.

        Parameters:
            - figure (matplotlib.figure.Figure): The Matplotlib figure to be displayed in the `QGraphicsView`.

        Behavior:
            - Clears the current scene in `self.graphics_graph`.
            - Converts the Matplotlib figure into a `FigureCanvas` object.
            - Creates a new `QGraphicsScene` and adds the canvas to it.
            - Sets the new scene in the `QGraphicsView` and updates the display.

        Example usage:
            self.display_matplotlib_figure(figure)
        """
    
        self.graphics_graph.scene().clear()

        
        canvas = FigureCanvas(figure)

        
        scene = QGraphicsScene()
        scene.addWidget(canvas)

        
        self.graphics_graph.setScene(scene)

        
        self.graphics_graph.show()








    def displayFileName(self, file_name, graphics_view, file_pos):
        """
        @brief Displays a file name as a clickable text item in a specified QGraphicsView.

        This method displays a file name as an interactive text item within a `QGraphicsView` widget. 
        It checks whether the appropriate scene (`graphics_load1`, `graphics_load2`, `graphics_load3`, 
        or `graphics_load4`) has been initialized, and if not, creates a new `QGraphicsScene` for the 
        specified view. The file name is added as a `ClickableTextItem` in the scene, and the text item 
        is set to be interactive, selectable, and focusable.

        Parameters:
            - file_name (str): The name of the file to be displayed as a clickable text item.
            - graphics_view (QGraphicsView): The graphics view where the file name should be displayed.
            - file_pos (int): The vertical position offset for the text item in the view.

        Behavior:
            - Checks if the scene for the specified `graphics_view` is initialized; if not, a new scene is created.
            - Adds the file name as a `ClickableTextItem` to the scene.
            - Positions the text item in the scene based on `file_pos` and the number of existing items.
            - Ensures the text item is interactive, selectable, and focusable.

        Example usage:
            self.display_file_name("example.txt", self.graphics_load1, 50)
        """
        # Initialize the scene if it's not already set for the respective graphics view
        if graphics_view == self.graphics_load1 and self.scene_load1 is None:
            self.scene_load1 = QGraphicsScene()
            self.graphics_load1.setScene(self.scene_load1)

        if graphics_view == self.graphics_load2 and self.scene_load2 is None:
            self.scene_load2 = QGraphicsScene()
            self.graphics_load2.setScene(self.scene_load2)

        if graphics_view == self.graphics_load3 and self.scene_load3 is None:
            self.scene_load3 = QGraphicsScene()
            self.graphics_load3.setScene(self.scene_load3)

        if graphics_view == self.graphics_load4 and self.scene_load4 is None:
            self.scene_load4 = QGraphicsScene()
            self.graphics_load4.setScene(self.scene_load4)

        scene = graphics_view.scene()

        graphics_view.setInteractive(True)
        graphics_view.setScene(scene)
        
        
        
        text_item = ClickableTextItem(file_name)
      
        if graphics_view == self.graphics_load1 and text_item not in self.text_item1:
            self.text_item1.append(text_item)
            scene.addItem(text_item)

            index = scene.items().index(text_item)
            text_item.setPos(0, index + file_pos)  

            text_item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            text_item.setFlag(QGraphicsTextItem.ItemIsFocusable, True)
            text_item.setAcceptHoverEvents(True)

        if graphics_view == self.graphics_load2 and text_item not in self.text_item2:
            self.text_item2.append(text_item)
            scene.addItem(text_item)

            index = scene.items().index(text_item)
            text_item.setPos(0, index + file_pos) 

            text_item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            text_item.setFlag(QGraphicsTextItem.ItemIsFocusable, True)
            text_item.setAcceptHoverEvents(True)
        
        if graphics_view == self.graphics_load3 and text_item not in self.text_item3:
            self.text_item3.append(text_item)
            scene.addItem(text_item)
            
            index = scene.items().index(text_item)
            text_item.setPos(0, index + file_pos) 

            text_item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            text_item.setFlag(QGraphicsTextItem.ItemIsFocusable, True)
            text_item.setAcceptHoverEvents(True)
        
        if graphics_view == self.graphics_load4 and text_item not in self.text_item4:
            self.text_item4.append(text_item)
            scene.addItem(text_item)

            index = scene.items().index(text_item)
            text_item.setPos(0, index + file_pos)  
            text_item.setFlag(QGraphicsTextItem.ItemIsSelectable, True)
            text_item.setFlag(QGraphicsTextItem.ItemIsFocusable, True)
            text_item.setAcceptHoverEvents(True)





        if graphics_view == self.graphics_load1:
            self.text_item1.append(text_item)



        if graphics_view == self.graphics_load2:
            self.text_item2.append(text_item)


        if graphics_view == self.graphics_load3:
            self.text_item3.append(text_item)


        if graphics_view == self.graphics_load4:
            self.text_item4.append(text_item)
        
    
    
    
    
    def DeleteLoadedFiles1(self):
        """
        @brief Deletes selected or all loaded files from the first graphics view.

        This method manages the deletion of loaded files from the `self.loaded_files1` list. If no files 
        are currently loaded, it shows an informational message to the user. If files are loaded, it prompts 
        the user with a confirmation dialog to delete the selected files. If the user confirms, the selected 
        files are removed, and the scene is updated accordingly. If no items are selected, all files are cleared 
        from the view, and the scene is reset. The scroll bars are adjusted based on the remaining items and 
        their layout.

        Behavior:
            - Displays an informational message if no files are loaded.
            - Prompts the user for confirmation to delete selected files.
            - Removes selected files from `self.loaded_files1` and updates the scene.
            - Clears all files if no items are selected and refreshes the scene.
            - Adjusts scroll bars based on the number of remaining items and their positioning.

        UI Elements:
            - `self.graphics_load1`: The QGraphicsView displaying the loaded files.
            - `self.scene_load1`: The QGraphicsScene associated with `self.graphics_load1`.
            - `self.loaded_files1` (list of str): List of file names loaded into the first graphics view.
            - `self.text_item1` (list of QGraphicsTextItem): List of text items representing the loaded files.

        Example usage:
            self.DeleteLoadedFiles1()
        """

        if not self.loaded_files1:
            QMessageBox.information(self, "No Files Loaded", "No files have been loaded yet.")
            return
        reply = QMessageBox.question(self, "Delete Files", "Are you sure you want to delete the selected files?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            selected_items = self.scene_load1.selectedItems()
            total_width = 0

            if selected_items:
                file_pos = 0
                for item in selected_items:     
                    file_name = item.toPlainText()
                    self.loaded_files1.remove(file_name)
                    self.text_item1.remove(item)

                    self.scene_load1.removeItem(item)
                    
                file_pos = 0
                for item in self.scene_load1.items(): 
                    if isinstance(item, QGraphicsTextItem):
                        item.setPos(0, file_pos)
                        file_pos += 20
                        total_width += item.boundingRect().width()
                        self.scene_load1.setSceneRect(self.scene_load1.itemsBoundingRect())
                QMessageBox.information(
                    self, "Files Deleted", "Selected files have been deleted."
                )

            else:
                self.scene_load1.clear()
                self.loaded_files1.clear()
                QMessageBox.information(
                    self, "Files Deleted", "All files have been deleted."
                )
                self.loaded_files1.sort()
                
        
        visible_horizontal = 0
        if total_width != 0:
            visible_horizontal = (self.graphics_load1.viewport().width() - self.graphics_load1.contentsMargins().left() - self.graphics_load1.contentsMargins().right()) // total_width
        else:
            visible_horizontal = (self.graphics_load1.viewport().width() - self.graphics_load1.contentsMargins().left() - self.graphics_load1.contentsMargins().right())//1
            
            
            visible_vertical = (self.graphics_load1.viewport().height() - self.graphics_load1.contentsMargins().top() - self.graphics_load1.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files1) <= visible_vertical:
                self.graphics_load1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load1.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files1) <= visible_horizontal:
                self.graphics_load1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load1.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load1.update()          
    
    
    def DeleteLoadedFiles2(self):
        """
        @brief Deletes selected or all loaded files from the first graphics view.

        This method manages the deletion of loaded files from the `self.loaded_files2` list. If no files 
        are currently loaded, it shows an informational message to the user. If files are loaded, it prompts 
        the user with a confirmation dialog to delete the selected files. If the user confirms, the selected 
        files are removed, and the scene is updated accordingly. If no items are selected, all files are cleared 
        from the view, and the scene is reset. The scroll bars are adjusted based on the remaining items and 
        their layout.

        Behavior:
            - Displays an informational message if no files are loaded.
            - Prompts the user for confirmation to delete selected files.
            - Removes selected files from `self.loaded_files2` and updates the scene.
            - Clears all files if no items are selected and refreshes the scene.
            - Adjusts scroll bars based on the number of remaining items and their positioning.

        UI Elements:
            - `self.graphics_load2`: The QGraphicsView displaying the loaded files.
            - `self.scene_load2`: The QGraphicsScene associated with `self.graphics_load2`.
            - `self.loaded_files2` (list of str): List of file names loaded into the first graphics view.
            - `self.text_item2` (list of QGraphicsTextItem): List of text items representing the loaded files.

        Example usage:
            self.DeleteLoadedFiles2()
        """

        if not self.loaded_files2:
            QMessageBox.information(self, "No Files Loaded", "No files have been loaded yet.")
            return
        reply = QMessageBox.question(self, "Delete Files", "Are you sure you want to delete the selected files?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            selected_items = self.scene_load2.selectedItems()
            total_width = 0

            if selected_items:
                file_pos = 0
                for item in selected_items:    
                    file_name = item.toPlainText()
                    self.loaded_files2.remove(file_name)
                    self.text_item2.remove(item)

                    self.scene_load2.removeItem(item)
                    
                file_pos = 0
                for item in self.scene_load2.items(): 
                    if isinstance(item, QGraphicsTextItem):
                        item.setPos(0, file_pos)
                        file_pos += 20
                        total_width += item.boundingRect().width()
                        self.scene_load2.setSceneRect(self.scene_load2.itemsBoundingRect())
                QMessageBox.information(

                    self, "Files Deleted", "Selected files have been deleted."
                )

            else:
                self.scene_load2.clear()
                self.loaded_files2.clear()
                QMessageBox.information(
                    self, "Files Deleted", "All files have been deleted."
                )
                self.loaded_files2.sort()
        
        visible_horizontal = 0
        if total_width != 0:
            visible_horizontal = (self.graphics_load2.viewport().width() - self.graphics_load2.contentsMargins().left() - self.graphics_load2.contentsMargins().right()) // total_width
        else:
            visible_horizontal = (self.graphics_load2.viewport().width() - self.graphics_load2.contentsMargins().left() - self.graphics_load2.contentsMargins().right())//1
            
            
            visible_vertical = (self.graphics_load2.viewport().height() - self.graphics_load2.contentsMargins().top() - self.graphics_load2.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files2) <= visible_vertical:
                self.graphics_load2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files2) <= visible_horizontal:
                self.graphics_load2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load2.update()         

    
    
    def DeleteLoadedFiles3(self):
        """
        @brief Deletes selected or all loaded files from the first graphics view.

        This method manages the deletion of loaded files from the `self.loaded_files1` list. If no files 
        are currently loaded, it shows an informational message to the user. If files are loaded, it prompts 
        the user with a confirmation dialog to delete the selected files. If the user confirms, the selected 
        files are removed, and the scene is updated accordingly. If no items are selected, all files are cleared 
        from the view, and the scene is reset. The scroll bars are adjusted based on the remaining items and 
        their layout.

        Behavior:
            - Displays an informational message if no files are loaded.
            - Prompts the user for confirmation to delete selected files.
            - Removes selected files from `self.loaded_files3` and updates the scene.
            - Clears all files if no items are selected and refreshes the scene.
            - Adjusts scroll bars based on the number of remaining items and their positioning.

        UI Elements:
            - `self.graphics_load3`: The QGraphicsView displaying the loaded files.
            - `self.scene_load3`: The QGraphicsScene associated with `self.graphics_load3`.
            - `self.loaded_files3` (list of str): List of file names loaded into the first graphics view.
            - `self.text_item3` (list of QGraphicsTextItem): List of text items representing the loaded files.

        Example usage:
            self.DeleteLoadedFiles3()
        """

        if not self.loaded_files3:
            QMessageBox.information(self, "No Files Loaded", "No files have been loaded yet.")
            return
        reply = QMessageBox.question(self, "Delete Files", "Are you sure you want to delete the selected files?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            selected_items = self.scene_load3.selectedItems()
            total_width = 0 
            
            if selected_items:
                file_pos = 0
                for item in selected_items:    
                    file_name = item.toPlainText()
                    self.loaded_files3.remove(file_name)
                    self.text_item3.remove(item)

                    self.scene_load3.removeItem(item)
                    
                file_pos = 0
                for item in self.scene_load3.items():
                    if isinstance(item, QGraphicsTextItem):
                        item.setPos(0, file_pos)
                        file_pos += 20
                        total_width += item.boundingRect().width()
                        self.scene_load3.setSceneRect(self.scene_load3.itemsBoundingRect())
                QMessageBox.information(
                    self, "Files Deleted", "Selected files have been deleted."
                )

            else:
                self.scene_load3.clear()
                self.loaded_files3.clear()
                QMessageBox.information(
                    self, "Files Deleted", "All files have been deleted."
                )
                self.loaded_files3.sort()
                
        visible_horizontal = 0
        if total_width != 0:
            visible_horizontal = (self.graphics_load3.viewport().width() - self.graphics_load3.contentsMargins().left() - self.graphics_load3.contentsMargins().right()) // total_width
        else:
            visible_horizontal = (self.graphics_load3.viewport().width() - self.graphics_load3.contentsMargins().left() - self.graphics_load3.contentsMargins().right())//1
            
            
            visible_vertical = (self.graphics_load3.viewport().height() - self.graphics_load3.contentsMargins().top() - self.graphics_load3.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files3) <= visible_vertical:
                self.graphics_load3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load3.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files3) <= visible_horizontal:
                self.graphics_load3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load3.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load3.update()         




    def DeleteLoadedFiles4(self):
        """
        @brief Deletes selected or all loaded files from the first graphics view.

        This method manages the deletion of loaded files from the `self.loaded_files4` list. If no files 
        are currently loaded, it shows an informational message to the user. If files are loaded, it prompts 
        the user with a confirmation dialog to delete the selected files. If the user confirms, the selected 
        files are removed, and the scene is updated accordingly. If no items are selected, all files are cleared 
        from the view, and the scene is reset. The scroll bars are adjusted based on the remaining items and 
        their layout.

        Behavior:
            - Displays an informational message if no files are loaded.
            - Prompts the user for confirmation to delete selected files.
            - Removes selected files from `self.loaded_files4` and updates the scene.
            - Clears all files if no items are selected and refreshes the scene.
            - Adjusts scroll bars based on the number of remaining items and their positioning.

        UI Elements:
            - `self.graphics_load4`: The QGraphicsView displaying the loaded files.
            - `self.scene_load4`: The QGraphicsScene associated with `self.graphics_load4`.
            - `self.loaded_files4` (list of str): List of file names loaded into the first graphics view.
            - `self.text_item4` (list of QGraphicsTextItem): List of text items representing the loaded files.

        Example usage:
            self.DeleteLoadedFiles4()
        """

        
        if not self.loaded_files4:
            QMessageBox.information(self, "No Files Loaded", "No files have been loaded yet.")
            return
        reply = QMessageBox.question(self, "Delete Files", "Are you sure you want to delete the selected files?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            selected_items = self.scene_load4.selectedItems()
            total_width = 0 
            
            
            
            if selected_items:
                file_pos = 0
                for item in selected_items:     
                    file_name = item.toPlainText()
                    self.loaded_files4.remove(file_name)
                    self.text_item4.remove(item)

                    self.scene_load4.removeItem(item)
                    
                file_pos = 0
                for item in self.scene_load4.items():
                    if isinstance(item, QGraphicsTextItem):
                        item.setPos(0, file_pos)
                        file_pos += 20    
                        total_width += item.boundingRect().width()
                        self.scene_load4.setSceneRect(self.scene_load4.itemsBoundingRect())
                QMessageBox.information(
                    self, "Files Deleted", "Selected files have been deleted."
                )
            
            else:
                self.scene_load4.clear()
                self.loaded_files4.clear()
                QMessageBox.information(
                    self, "Files Deleted", "All files have been deleted."
                )
                self.loaded_files4.sort()
               
            visible_horizontal = 0
        if total_width != 0:
            visible_horizontal = (self.graphics_load4.viewport().width() - self.graphics_load4.contentsMargins().left() - self.graphics_load4.contentsMargins().right()) // total_width
        else:
            visible_horizontal = (self.graphics_load4.viewport().width() - self.graphics_load4.contentsMargins().left() - self.graphics_load4.contentsMargins().right())//1
            
            
            visible_vertical = (self.graphics_load4.viewport().height() - self.graphics_load4.contentsMargins().top() - self.graphics_load4.contentsMargins().bottom())//20
            
            
            if len(self.loaded_files4) <= visible_vertical:
                self.graphics_load4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load4.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            if len(self.loaded_files4) <= visible_horizontal:
                self.graphics_load4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
            else:
                self.graphics_load4.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            
            self.graphics_load4.update()


    def saveDisplayedFigure(self):
        """
        Saves the currently displayed Matplotlib figure to a file.

        This method retrieves the Matplotlib figure currently displayed in the `graphics_graph` 
        QGraphicsView. It then opens a file dialog to allow the user to choose a location and 
        filename to save the figure as a PNG file. The figure is saved to the selected file path.

        Behavior:
        - Retrieves the currently displayed figure from the `graphics_graph` QGraphicsView.
        - Opens a file dialog for the user to select where to save the file.
        - Saves the figure as a PNG file to the selected location.

        UI Elements:
        - `self.graphics_graph`: The QGraphicsView containing the Matplotlib figure.
        """
            
        # Open a file dialog for saving the figure
        current_figure = self.graphics_graph.scene().items()[0].widget().figure

        # Open a file dialog for saving the figure
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_dialog.setNameFilter("PNG Files (*.png);;All Files (*)")
        if file_dialog.exec_():
            # Get the selected file path and save the figure as a PNG
            selected_file = file_dialog.selectedFiles()[0]
            current_figure.savefig(selected_file, format='png')


    def ev_volume(self):    
        """
        @brief Processes the first file in `loaded_files4` and extracts volume data.

        This method processes the first file in the `self.loaded_files4` list. If no files are loaded, 
        the method returns without performing any actions. If there is at least one file, it opens the 
        first file, reads the contents line by line, splits each line into components, and appends the 
        first component (assumed to be a volume value) as a float to `self.ev_vol_list`.

        Behavior:
            - Checks whether `self.loaded_files4` contains any files.
            - Returns immediately if no files are loaded.
            - If files are present, opens and processes the first file.
            - Extracts the first component of each line as a volume (float) and stores it in `self.ev_vol_list`.

        Attributes:
            - `self.loaded_files4` (list of str): A list of file paths to be processed.
            - `self.ev_vol_list` (list of float): A list that stores the extracted volume data from the first file.

        Example usage:
            self.ev_volume()
        """
        # Check if any files are loaded; if not, return        
        if not self.loaded_files4:
            return                         
        file_name = self.loaded_files4[0] 
        with open(file_name, 'r') as data:
            for line in data:
                p = line.split()
                self.ev_vol_list.append(float(p[0]))

        


    def temp_vol(self):
        """
        @brief Processes files in `loaded_files3` to extract temperature and volume data.

        This method processes the files loaded in `self.loaded_files3`. It checks if any files are present 
        in the list, and if no files are loaded, it returns without performing any actions. If files are present, 
        it iterates through each file, reading its contents line by line. Each line is split into components, 
        with the first component (assumed to be temperature) appended to `self.temp_list` and the second component 
        (assumed to be volume) appended to `self.volume_list`.

        Behavior:
            - Checks whether `self.loaded_files3` contains any files.
            - Returns immediately if no files are loaded.
            - If files are present, opens each file and processes its contents.
            - Extracts the first component of each line as a temperature (float) and stores it in `self.temp_list`.
            - Extracts the second component of each line as a volume (float) and stores it in `self.volume_list`.

        Attributes:
            - `self.loaded_files3` (list of str): A list of file paths that are to be processed.
            - `self.temp_list` (list of float): A list where the extracted temperature data is stored.
            - `self.volume_list` (list of float): A list where the extracted volume data is stored.

        Example usage:
            self.temp_vol()
        """
        if not self.loaded_files3:
            return
        for file_names in self.loaded_files3:
            with open(file_names, 'r') as data:
                for line in data:
                    p = line.split()
                    self.temp_list.append(float(p[0]))
                    self.volume_list.append(float(p[1]))
        




    def Cleaning(self):
            """
            @brief Cleans and processes files from `loaded_files2` by extracting specific content.

            This method processes the files in `self.loaded_files2` by extracting specific content and writing 
            it to new output files. Before processing, the method checks if any files are loaded in `self.loaded_files3` 
            or `self.loaded_files4`. If either of these lists contains files, the method returns without performing any 
            operations. If both lists are empty, it iterates over each file in `self.loaded_files2`, processes the content, 
            and creates a new output file with the cleaned content.

            Behavior:
                - Checks whether `self.loaded_files4` or `self.loaded_files3` contain any files.
                - If either list contains files, the method exits immediately.
                - If both lists are empty, it processes each file in `self.loaded_files2`.
                - For each file, creates a new output file with the name "cleaned.txt".
                - Extracts content starting from the 7th character up to the 40th character on lines that begin with "  - [".
                - Writes the extracted content to the new output file.
                - Stores the path of the output file in `self.outfile` and the file name in `self.outfile_names`.

            Attributes:
                - `self.loaded_files2` (list of str): A list of file paths to be processed.
                - `self.loaded_files3` (list of str): A list of file paths (checked but not used directly).
                - `self.loaded_files4` (list of str): A list of file paths (checked but not used directly).
                - `self.outfile` (list of str): A list to store the paths of the cleaned output files.
                - `self.outfile_names` (list of str): A list to store the names of the cleaned output files.

            Example usage:
                self.Cleaning()
            """

            if not self.loaded_files4 and not self.loaded_files3:
                for  file_name in self.loaded_files2: 
                    infile = file_name
                    outfile = "cleaned"  + ".txt"
                    paths_outfile = os.path.abspath(outfile)
                    with open(infile) as fin, open(outfile, "w+") as fout:
                        lines = fin.readlines()
                        for i in range(len(lines)):     
                            if lines[i][0:5] == "  - [":
                                fout.writelines(lines[i][7:40] + "\n")
                    
                    self.outfile.append(paths_outfile)
                    self.outfile_names.append(paths_outfile)


            else:    
                for  file_name in self.loaded_files2: 
                    infile = file_name
                    outfile = "cleaned_" + file_name.split("yaml-")[1] + ".txt"
                    paths_outfile = os.path.abspath(outfile)
                    with open(infile) as fin, open(outfile, "w+") as fout:
                        lines = fin.readlines()
                        for i in range(len(lines)):     
                            if lines[i][0:5] == "  - [":
                                fout.writelines(lines[i][7:40] + "\n")
                    
                    self.outfile.append(paths_outfile)
                    self.outfile_names.append(paths_outfile)
                self.outfile.sort(key=self.get_sort_key)


    
    def get_sort_key(self, filename):
        """
        @brief Extracts a numerical sort key from a filename.

        This method is used to extract a numerical value from a filename, specifically for sorting 
        files in Quasi-Harmonic Approximation. It searches for the pattern 'cleaned_<number>' in the filename 
        using a regular expression. If the pattern is found, the method returns the extracted number as an 
        integer. If the pattern is not found, it returns 0.

        Parameters:
            - filename (str): The filename from which the numerical sort key is extracted.

        Returns:
            - int: The extracted number as an integer, or 0 if the pattern is not found.

        Example usage:
            - For a filename 'cleaned_-123.txt', this method will return -123.

        Example:
            sort_key = self.extract_sort_key('cleaned_-123.txt')  # Returns -123
        """

        # Search for the pattern 'cleaned_<number>' in the filename
        match = re.search(r'cleaned_(-?\d+)', filename)
        if match:
            return int(match.group(1))
        return 0

    
    




        
        


    def DeletingCleanedFiles(self):
        """
        @brief Deletes all cleaned files listed in `self.files_to_delete` and clears the `outfile` list.

        This method deletes files listed in `self.files_to_delete` and clears the `outfile` list. 
        It first checks if there are any files in `self.outfile`. If `outfile` is empty, the method exits 
        without performing any actions. If `outfile` contains files, the method iterates through each file 
        in `self.files_to_delete`, deletes the corresponding file from the filesystem, and then clears 
        the `outfile` list.

        Behavior:
            - Checks whether `self.outfile` contains any files.
            - If `self.outfile` is empty, the method returns immediately.
            - Deletes each file in `self.files_to_delete`.
            - Clears the `outfile` list after all deletions are complete.

        Attributes:
            - `self.outfile` (list of str): A list containing the paths of cleaned files.
            - `self.files_to_delete` (list of str): A list of file paths that are to be deleted.

        Example usage:
            self.delete_cleaned_files()
        """

        # Check if there are any files in outfile; if not, return
        if not self.outfile:
            return

 
        # Iterate through each file in files_to_delete and remove it
        for file_names in self.files_to_delete:
            os.remove(file_names)
        
        # Clear the outfile list after deleting the files
        self.outfile.clear()
    
    def Msd(self):
        """
        @brief Processes cleaned files to extract and store the X, Y, Z components of mean square displacements of atoms.

        This method processes each file listed in `self.outfile`, which contains paths to the cleaned files. 
        For each file, the method reads the contents line by line, assuming the data to be comma-separated 
        values representing the X, Y, and Z components of mean square displacements. These components are 
        extracted and stored as floats in three separate lists: `mx`, `my`, and `mz`. After processing each 
        file, the lists are combined as a list of lists (`[mx, my, mz]`) and appended to `self.data_list`.

        Behavior:
            - Iterates through each file in `self.outfile`.
            - Reads each file line by line.
            - Extracts the X, Y, and Z components from each line and converts them to floats.
            - Appends the extracted data for each file as a list of lists (`[mx, my, mz]`) to `self.data_list`.

        Attributes:
            - `self.outfile` (list of str): A list of paths to the cleaned files.
            - `self.data_list` (list of list of lists): A list that stores the extracted X, Y, Z data for each file.

        Example:
            - After processing, `self.data_list` might contain data in the form:
            `[[[mx1, mx2, ...], [my1, my2, ...], [mz1, mz2, ...]], ...]`
            
        Example usage:
            self.Msd()
        """
        for file_names in self.outfile:
            mx = [] 
            my = []
            mz = []
            
            with open(file_names, 'r') as data:
                for line in data:
                    p = line.split(",")
                    mx.append(float(p[0]))
                    my.append(float(p[1]))
                    mz.append(float(p[2]))
                    
            self.data_list_x.append(mx) 
            self.data_list_y.append(my) 
            self.data_list_z.append(mz)
             
    def Msd_sing(self):
        """
        Processes cleaned files to extract and store X, Y, Z data components.

        This method iterates through each file in `self.outfile`, which contains paths to the cleaned files.
        For each file, it reads the contents line by line, expecting the data to be comma-separated values 
        representing X, Y, and Z components. These components are extracted and stored as floats in separate 
        lists (`mx`, `my`, `mz`). After processing each file, the lists are appended as a list of lists to 
        `self.data_list`.

        Behavior:
        - Iterates through each file in `self.outfile`.
        - For each file, reads the data line by line.
        - Extracts the X, Y, and Z components from each line, converting them to floats.
        - Appends the extracted data for each file as a list of lists (`[mx, my, mz]`) to `self.data_list`.

        Attributes:
        - `self.outfile` (list of str): A list of paths to the cleaned files.
        - `self.data_list` (list of list of lists): A list to store the extracted X, Y, Z data for each file.

        Example:
        - After processing, `self.data_list` might contain data in the form:
        `[[[mx1, mx2, ...], [my1, my2, ...], [mz1, mz2, ...]], ...]`
        """
        for file_names in self.outfile:
            mx = [] 
            my = []
            mz = []
            
            with open(file_names, 'r') as data:
                for line in data:
                    p = line.split(",")
                    mx.append(float(p[0]))
                    my.append(float(p[1]))
                    mz.append(float(p[2]))
                    
            self.data_sing_list.append([mx, my, mz]) 
    
    def Msd_interpol(self):
        """
        @brief Performs linear interpolation on the X, Y, Z components of mean-square displacements.

        This method performs linear interpolation on the X, Y, and Z components of mean-square displacements 
        for each atom, using the temperature values from `self.temp_list`. The Phonopy calculation typically 
        produces mean-square displacements at 10 K intervals, so this method interpolates the values to match 
        the real temperature data in `self.temp_list`.

        Behavior:
            - Initializes empty lists (`mx2`, `my2`, `mz2`) for each atom to store interpolated values.
            - Iterates through the temperature data in `self.temp_list`.
            - For each temperature, calculates the appropriate indices to extract X, Y, Z data from `self.data_list`.
            - Performs linear interpolation between boundary temperature values for each component (X, Y, Z).
            - Appends the interpolated X, Y, Z values to `mx2`, `my2`, and `mz2` for the current atom.
            - After processing all temperatures, appends the results for each atom to `self.mx1`, `self.my1`, and `self.mz1`.

        Attributes:
            - `self.atom_masses` (list of float): A list representing the masses of the atoms, used to determine the number of atoms.
            - `self.temp_list` (list of float): A list of real temperature values used for interpolation.
            - `self.data_list` (list of list of lists): A list containing the X, Y, Z data components for each temperature.
            - `self.mx1` (list of lists): A list to store the interpolated X components for each atom.
            - `self.my1` (list of lists): A list to store the interpolated Y components for each atom.
            - `self.mz1` (list of lists): A list to store the interpolated Z components for each atom.

        Example usage:
            self.Msd_interpol()
        """

        natom = len(self.atom_masses)
        t = [float(np_scalar) for np_scalar in self.temp_list]
        i = 1
        for i in range(1 ,int(len(self.atom_masses)+1)):
            mx2 = []
            mz2 = []
            my2 = []
            
            for n in range(0, len(self.temp_list), 1):
                t_0 = math.trunc(t[n] / 10)*natom + i - 1 
                t_1 = t_0 + natom
                
                interpolx = [self.data_list_x[n][0][t_0], self.data_list_x[n][0][t_1]]
                interpoly = [self.data_list[n][1][t_0], self.data_list[n][1][t_1]]
                interpolz = [self.data_list[n][2][t_0], self.data_list[n][2][t_1]]

                boundary_temp = [math.trunc(t[n]/10)*10, math.trunc(t[n]/10)*10 + 10]

                fx = interpolate.interp1d(boundary_temp, interpolx, kind="linear")
                x = fx(t[n])

                fy = interpolate.interp1d(boundary_temp, interpoly, kind="linear")
                y = fy(t[n])

                fz = interpolate.interp1d(boundary_temp, interpolz, kind="linear")
                z = fz(t[n])
                mx2.append(x)
                my2.append(y)
                mz2.append(z)
            
            self.mx1.append(mx2)
            self.mz1.append(mz2)
            self.my1.append(my2)
       
      
        
    def count_values_smaller_than_first(self):
        """
        @brief Counts the number of values in `ev_vol_list` that are smaller than the first value in `volume_list`.

        This method checks how many values in `self.ev_vol_list` are smaller than the first value in `self.volume_list`. 
        This is crucial since the Phonopy settings may occasionally produce unphysical results, where mean-square 
        displacements are calculated for unit cell volumes corresponding to negative absolute temperatures. The method 
        counts how many such values exist and appends the count to `self.count`.

        Behavior:
            - Retrieves the first value from `self.volume_list` to use as a reference.
            - Iterates through each value in `self.ev_vol_list`.
            - Increments a counter for each value in `ev_vol_list` that is smaller than the first value in `volume_list`.
            - Appends the final count to `self.count`.

        Attributes:
            - `self.volume_list` (list of float): A list of volume values, where the first value is used as the reference.
            - `self.ev_vol_list` (list of float): A list of volume values to be compared against the first value in `volume_list`.
            - `self.count` (list of int): A list to store the count of values smaller than the first value in `volume_list`.

        Example usage:
            self.count_invalid_volumes()
        """

        first_vol = self.volume_list[0]
        count = 0

        for value in self.ev_vol_list:
            if value < first_vol:
                count += 1
     
        self.count.append(count)   

    
    def Removing(self):
        """
        @brief Removes the initial portion of `ev_vol_list` and `outfile` based on the first value in `count`.

        This method removes the initial elements of `self.ev_vol_list` and `self.outfile` based on the first value 
        in `self.count`. The method slices both lists, starting from the index specified by `self.count[0]`, 
        and retains only the elements from that index onward.

        Behavior:
            - Retrieves the first value from `self.count`.
            - Slices `self.ev_vol_list` and `self.outfile` to remove the initial elements up to the index specified 
            by `self.count[0]`.

        Attributes:
            - `self.ev_vol_list` (list of float): A list of volume values to be sliced.
            - `self.outfile` (list of str): A list of file paths to be sliced.
            - `self.count` (list of int): A list where the first value specifies how many initial elements to remove.

        Example usage:
            self.slice_invalid_volumes()
        """

        self.ev_vol_list = self.ev_vol_list[int(self.count[0]):]   
        self.outfile = self.outfile[int(self.count[0]):]

    
    def Mfactor(self):
        """
        @brief Calculates the Mossbauer factor for each atom based on its mass, recoil energy, temperature, 
        and mean square displacements in the X, Y, and Z directions.

        This method computes the Mossbauer factor for each atom in `self.atom_masses`. It selects the temperature 
        data based on whether `self.loaded_files3` and `self.loaded_files4` are empty. The calculation involves 
        physical constants, the atom's mass, the energy constant `Er_const_list`, and an exponential function 
        using the mean square displacements (`mz1`, `mx1`, `my1`) for each atom. The results are stored in `self.factor_list`.

        Behavior:
            - If `self.loaded_files3` and `self.loaded_files4` are empty, the method uses `self.sing_temperature` 
            for the calculations.
            - If files are loaded, the method uses `self.temp_list` for the calculations.
            - For each atom, calculates the Mossbauer factor using an exponential function based on the atom's mass, 
            energy constant, and displacements in the X, Y, and Z directions.
            - Appends the calculated factor for each atom to `self.factor_list`.

        Attributes:
            - `self.atom_masses` (list of float): A list of atomic masses for each atom.
            - `self.Er_const_list` (list of float): A list of recoil energy constants for each atom.
            - `self.sing_temperature` (list of float): A list of single temperature values used when `loaded_files3` 
            and `loaded_files4` are empty.
            - `self.temp_list` (list of float): A list of real temperature values used when `loaded_files3` and 
            `loaded_files4` are not empty.
            - `self.mx1`, `self.my1`, `self.mz1` (list of lists of float): Lists containing the mean square displacements 
            of atoms in the X, Y, and Z directions.
            - `self.factor_list` (list of lists of float): A list to store the calculated Mossbauer factors for each atom.

        Constants Used:
            - `con.eV`: Electron volt in Joules.
            - `con.atomic_mass`: Atomic mass constant.
            - `con.c`: Speed of light in a vacuum.
            - `con.hbar`: Reduced Planck constant.

        Example usage:
            self.Mfactor()
        """

        if not self.loaded_files3 and not self.loaded_files4:
            
            for i in range(1,int(len(self.atom_masses)+1)):
                atomic_number = self.atom_masses[int(i-1)]
                Er = self.Er_const_list[int(i-1)] * con.eV

                m = atomic_number * con.atomic_mass
                Eg_squared = 2 * m * con.c * con.c * Er
                d1 = Eg_squared / (con.c * con.hbar * con.c * con.hbar)
                factor_list = [] 
                for u in range(0, len(self.sing_temperature)):
                    f = math.exp(-(0.5 * ( 0.5*self.mz1[int(i-1)][u] + 0.25*self.mx1[int(i-1)][u] + 0.25*self.my1[int(i-1)][u])) * d1 * 1.0e-20)
                    if f == 1:
                        factor_list.append(0)    
                    else:
                        factor_list.append(f)
                self.factor_list.append(factor_list)
        
        else:
            i = 1
            for i in range(1,int(len(self.atom_masses)+1)):
                atomic_number = self.atom_masses[int(i-1)]
                Er = self.Er_const_list[int(i-1)] * con.eV

                m = atomic_number * con.atomic_mass
                Eg_squared = 2 * m * con.c * con.c * Er
                d1 = Eg_squared / (con.c * con.hbar * con.c * con.hbar)
                factor_list = []  
                for u in range(0, len(self.temp_list)):
                    f = math.exp(-( 0.5 * (0.5*self.mz1[int(i-1)][u] + 0.25*self.mx1[int(i-1)][u] + 0.25*self.my1[int(i-1)][u] )) * d1 * 1.0e-20)
                    factor_list.append(f)
                self.factor_list.append(factor_list)  
          
    def get_atom_info(self):
        """
        @brief Extracts atomic information from files in `loaded_files1` and stores it.

        This method processes each file in `self.loaded_files1` to extract atomic information, including 
        the atom symbol, atom number, and atom mass. It identifies the section of the file between the 
        "primitive_cell:" and "reciprocal_lattice:" markers and uses a regular expression to extract 
        relevant atomic data. The extracted atom information is then stored in `self.atom_names`, 
        `self.atom_numbers`, and `self.atom_masses`.

        Behavior:
            - Iterates through each file in `self.loaded_files1`.
            - Reads the content of each file to locate the segment containing atomic information.
            - Uses a regular expression to extract the atom symbol, atom number, and atom mass from the identified segment.
            - Appends the extracted atom symbol to `self.atom_names`.
            - Clears and appends the extracted atom number to `self.atom_numbers`.
            - Appends the extracted atom mass to `self.atom_masses`.

        Attributes:
            - `self.loaded_files1` (list of str): A list of file paths to be processed for atomic information.
            - `self.atom_names` (list of str): A list that stores the symbols of the atoms extracted from the files.
            - `self.atom_numbers` (list of int): A list that stores the atomic numbers extracted from the files.
            - `self.atom_masses` (list of float): A list that stores the masses of the atoms extracted from the files.

        Example usage:
            self.get_atom_info()
        """

        for file_name in self.loaded_files1:
            with open(file_name, "r") as file:
                content = file.read()

            start_index = content.find("primitive_cell:")
            end_index = content.find("reciprocal_lattice:")
            segment = content[start_index:end_index]

            atom_info = re.findall(r"symbol: (\w+) # (\d+)\s+coordinates: .*?\n\s+mass: ([\d.]+)", segment, re.DOTALL)

        

            for symbol, atom_number, mass in atom_info:
                self.atom_names.append(symbol)
                self.atom_numbers.clear()
                self.atom_numbers.append(int(atom_number))
                self.atom_masses.append(float(mass))


    def map_names_to_numbers(self):
        """
        @brief Maps atomic symbols in `atom_names` to corresponding energy constants and stores them in `Er_const_list`.

        This method maps each atomic symbol in `self.atom_names` to its corresponding energy constant using 
        a predefined dictionary. If an atomic symbol is not found in the dictionary, a value of `0` is appended 
        to `self.Er_const_list`. The energy constants are typically used in further calculations, such as 
        determining the Mossbauer factor.

        Behavior:
            - Defines a dictionary `elements` that maps atomic symbols to their corresponding energy constants.
            - Iterates through each symbol in `self.atom_names`.
            - For each symbol, appends the corresponding energy constant from the `elements` dictionary to `self.Er_const_list`.
            - If a symbol is not found in the dictionary, appends `0` to `self.Er_const_list`.

        Attributes:
            - `self.atom_names` (list of str): A list of atomic symbols that need to be mapped to energy constants.
            - `self.Er_const_list` (list of float): A list to store the energy constants corresponding to the atomic symbols.

        Example:
            - If `self.atom_names` contains ["Fe", "I", "Unknown"], then `self.Er_const_list` will contain 
            [1.95883310e-03, 3.218e-03, 0].

        Example usage:
            self.map_names_to_numbers()
        """


        # Define the dictionary mapping atomic symbols to their energy constants
        elements = {"Fe": 1.95883310e-03,
        "I": 3.218e-03,
        "Sn": 2.57423e-3,
        "Sb": 6.122e-03,
        "Ir": 1.9094e-02}
        for name in self.atom_names:
            if name in elements:
                self.Er_const_list.append(elements[name])
            else:
                self.Er_const_list.append((0))




     
    def extract_temperatures(self):
        """
        @brief Extracts temperature values when only one thermal-displacement file is present.

        This method extracts temperature values from a thermal-displacements file when only a single file 
        is present in the data. It reads the temperature data from the file and processes it accordingly.

        Behavior:
            - Checks if only one thermal-displacement file is available.
            - Extracts and stores the temperature values from the file for further calculations.

        Attributes:
            - `self.loaded_files2` (list of str): The list of thermal-displacement files being processed.
            - `self.temp_list` (list of float): A list to store the extracted temperature values.

        Example usage:
            self.extract_temperatures()
        """

        for file_names in self.loaded_files2:
            with open(file_names, 'r') as file:
                    for line in file:
                        
                        
                        match = re.search(r'temperature:\s+([\d.]+)', line)
                        if match:
                          
                            temperature = float(match.group(1))
                            self.sing_temperature.append(temperature)
        
    
    def Sort(self):
        """
        Reorders the raw X, Y, Z data lists by atom index across all timesteps.

        This method assumes that `data_list_x`, `data_list_y`, and `data_list_z` are
        each a list of equal-length lists, where each sublist corresponds to one timestep
        and contains concatenated coordinate values for all atoms.

        It processes each coordinate axis in turn:

        1. Determine `natom` as the number of atoms from `self.atom_masses`.
        2. For each block of size `natom` in the first timestep’s data list:
           - For each atom index `p` within that block:
             - Collect the value at position `o + p` from every timestep’s list.
             - Append that series (one per atom) to `self.fit_list_{axis}_temp_ordered`.

        After running, you will have:
        - `self.fit_list_x_temp_ordered`
        - `self.fit_list_y_temp_ordered`
        - `self.fit_list_z_temp_ordered`

        each containing one sublist per atom, with that atom’s coordinate over time.

        Raises:
            IndexError: If `data_list_{axis}` sublists are of inconsistent length.
        """
        # Process X coordinates
        natom = len(self.atom_masses)
        for o in range(0, len(self.data_list_x[0]), natom):
            for p in range(natom):
                fit_temp_list_x = [
                    self.data_list_x[i][o + p]
                    for i in range(len(self.data_list_x))
                ]
                self.fit_list_x_temp_ordered.append(fit_temp_list_x)

        # Process Y coordinates
        natom = len(self.atom_masses)
        for o in range(0, len(self.data_list_y[0]), natom):
            for p in range(natom):
                fit_temp_list_y = [
                    self.data_list_y[i][o + p]
                    for i in range(len(self.data_list_y))
                ]
                self.fit_list_y_temp_ordered.append(fit_temp_list_y)

        # Process Z coordinates
        natom = len(self.atom_masses)
        for o in range(0, len(self.data_list_z[0]), natom):
            for p in range(natom):
                fit_temp_list_z = [
                    self.data_list_z[i][o + p]
                    for i in range(len(self.data_list_z))
                ]
                self.fit_list_z_temp_ordered.append(fit_temp_list_z)

        
    def Fitting(self):
        """
        Performs polynomial fitting (degree 2) of X, Y, and Z coordinate series
        against the evaporation volume data and stores the resulting coefficients.

        This method iterates over each ordered coordinate series in 
        `fit_list_x_temp_ordered`, `fit_list_y_temp_ordered`, and `fit_list_z_temp_ordered`:
        1. Uses `self.ev_vol_list` as the independent variable (x-values).
        2. Fits a quadratic polynomial to each coordinate series using `polyfit`.
        3. Wraps the resulting coefficient array in a list and appends it to:
           - `self.coef_x` for X-coordinates,
           - `self.coef_y` for Y-coordinates,
           - `self.coef_z` for Z-coordinates.

        After execution, `coef_x`, `coef_y`, and `coef_z` each contain one element
        per atom, where each element is a list containing the polynomial coefficients
        `[a, b, c]` for the fit:

            coordinate_value ≈ a*(ev_vol)^2 + b*(ev_vol) + c

        Raises:
            ValueError: If `polyfit` fails due to mismatched input lengths or 
                        invalid data (e.g., constant `ev_vol_list`).
        """
        # Fit X-coordinates
        for series in self.fit_list_x_temp_ordered:
            coef = polyfit(self.ev_vol_list, series, 2)
            self.coef_x.append([coef])

        # Fit Y-coordinates
        for series in self.fit_list_y_temp_ordered:
            coef = polyfit(self.ev_vol_list, series, 2)
            self.coef_y.append([coef])

        # Fit Z-coordinates
        for series in self.fit_list_z_temp_ordered:
            coef = polyfit(self.ev_vol_list, series, 2)
            self.coef_z.append([coef])

            
    def Imputing(self):
        """
        Computes interpolated X, Y, and Z coordinate trajectories for each atom
        based on previously fitted polynomial coefficients and the target volume list.

        This method assumes:
        - `self.coef_x`, `self.coef_y`, and `self.coef_z` each contain one list
          per atom with the three quadratic fit coefficients.
        - `self.volume_list` is a list of evaporation volumes at which to evaluate.

        For each atom index `i` (0 through natom–1):
        1. Builds a temporary list of X-values by:
           - Stepping through `self.volume_list` in blocks of size `natom`.
           - For each block, evaluating the polynomial at that volume:
             `polyval(coef_x[i], volume)`.
        2. Appends the resulting time series to `self.mx1`.

        The same procedure is then applied to Y-coefficients → `self.my1`
        and Z-coefficients → `self.mz1`.

        Raises:
            ValueError: If the coefficient arrays do not match the expected shape
                        or if `volume_list` length is not a multiple of `natom`.
        """
        natom = len(self.atom_masses)

        # Compute X trajectories
        for i in range(natom):
            temp_series = []
            for o in range(0, len(self.volume_list) * natom, natom):
                vol_index = o // natom
                coeffs = np.array(self.coef_x[o + i]).flatten()
                value = polyval(coeffs, self.volume_list[vol_index])
                temp_series.append(value)
            self.mx1.append(temp_series)

        # Compute Y trajectories
        for i in range(natom):
            temp_series = []
            for o in range(0, len(self.volume_list) * natom, natom):
                vol_index = o // natom
                coeffs = np.array(self.coef_y[o + i]).flatten()
                value = polyval(coeffs, self.volume_list[vol_index])
                temp_series.append(value)
            self.my1.append(temp_series)

        # Compute Z trajectories
        for i in range(natom):
            temp_series = []
            for o in range(0, len(self.volume_list) * natom, natom):
                vol_index = o // natom
                coeffs = np.array(self.coef_z[o + i]).flatten()
                value = polyval(coeffs, self.volume_list[vol_index])
                temp_series.append(value)
            self.mz1.append(temp_series)

   
    def sing_Msd_interpol(self):
        """
        @brief Extracts mean-square displacement (MSD) values for each atom from a thermal-displacement file.

        This function processes a thermal-displacement file and extracts the mean-square displacement (MSD) 
        values for each atom. The extracted values can be used for further analysis, such as interpolation 
        or calculations involving atomic motion.

        Behavior:
            - Reads the thermal-displacement file.
            - Extracts the MSD values for each atom from the file.
            - Stores the extracted MSD values for each atom in relevant lists or structures.

        Attributes:
            - `self.loaded_files2` (list of str): The list of thermal-displacement files being processed.
            - `self.ms_displacement_list` (list of float): A list to store the extracted MSD values.

        Example usage:
            self.sing_Msd_interpol()
        """
        
        natom = len(self.atom_masses)
        t = [float(np_scalar) for np_scalar in self.sing_temperature]
        
        for i in range(0 ,int(len(self.atom_masses))):
            mx2 = []
            mz2 = []
            my2 = []
            
            for n in range(0, len(self.sing_temperature)):
                t_0 = math.trunc(t[n] / 10)*natom + i
                mx2.append(self.data_sing_list[0][0][t_0])
                my2.append(self.data_sing_list[0][1][t_0])
                mz2.append(self.data_sing_list[0][2][t_0])
            
            self.mx1.append(mx2)
            self.mz1.append(mz2)
            self.my1.append(my2)
            
   
   
   
  
   
   
   
   
    def get_selected_resolution(self):
        """
        @brief Retrieves the selected resolution from the `box_resolution` combo box.

        This method gets the currently selected resolution from the `box_resolution` combo box 
        and returns the corresponding figure size and DPI (dots per inch) for plotting. If no 
        specific resolution is selected, it returns a default resolution.

        Returns:
            - dict: A dictionary containing 'figsize' (tuple) and 'dpi' (int) values for the selected resolution.

        Behavior:
            - Retrieves the index of the selected resolution from `box_resolution`.
            - Based on the selection, returns a dictionary with the appropriate figure size and DPI.
            - Default resolution is `(6.4, 3.8)` with `100` DPI if no specific resolution is selected.

        Resolutions:
            - 'Resolution': Default figure size `(6.4, 3.8)` with `100` DPI.
            - '720x480': Figure size `(7.2, 4.8)` with `100` DPI.
            - '1280x720': Figure size `(12.8, 7.2)` with `100` DPI.
            - '1920x1080': Figure size `(19.2, 10.8)` with `100` DPI.

        Example usage:
            resolution = self.get_selected_resolution()
        """
        selected_resolution_index = self.box_resolution.currentIndex()
        selected_resolution = self.box_resolution.itemText(selected_resolution_index)
        
        if selected_resolution == 'Resolution':
            return {'figsize': (6.4, 3.8), 'dpi': 100}
        elif selected_resolution == '720x480':
            return {'figsize': (7.2, 4.8), 'dpi': 100}
        elif selected_resolution == '1280x720':
            return {'figsize': (12.8, 7.2), 'dpi': 100}
        else:
            return {'figsize': (19.2, 10.8), 'dpi': 100}
    
    
    
    
    def get_selected_color(self):
        """
        @brief Retrieves the selected color from the `box_colors` combo box.

        This method returns the color selected from the `box_colors` combo box. If no specific color is 
        selected, it defaults to 'black'.

        Returns:
            - dict: A dictionary containing the selected 'color'. Defaults to 'black' if no color is selected.

        Example usage:
            color = self.get_selected_color()
        """
        selected_color_index = self.box_colors.currentIndex()
        selected_color = self.box_colors.itemText(selected_color_index)
        
        if selected_color != 'Colors':
            return {'color': selected_color}
        else:
            return {'color': 'black'}
    
    
    def get_linestyle(self):
        """
        @brief Retrieves the selected line style from the `box_linestyle` combo box.

        This method returns the selected line style from the `box_linestyle` combo box. If no specific 
        line style is selected, it defaults to 'solid'.

        Returns:
            - dict: A dictionary containing the selected 'linestyle'. Defaults to 'solid' if no line style is selected.

        Example usage:
            linestyle = self.get_linestyle()
        """
        selected_linestyle_index = self.box_linestyle.currentIndex()
        selected_linestyle = self.box_linestyle.itemText(selected_linestyle_index)

        if selected_linestyle != 'Linestyle':
            return {'linestyle' : selected_linestyle}
        else:     
            return {'linestyle' : 'solid'}
    
    def get_markers(self):
        """
        @brief Retrieves the selected marker style from the `box_markers` combo box.

        This method returns the selected marker style from the `box_markers` combo box. If no specific marker is selected, 
        it returns `None`.

        Returns:
            - dict: A dictionary containing the selected 'marker'. If no marker is selected, returns `None`.

        Marker options:
            - 'Circle': Returns `'o'` for circle markers.
            - 'Triangle': Returns `'^'` for triangle markers.
            - 'Square': Returns `'s'` for square markers.
            - Default: Returns `None` if no marker is selected.

        Example usage:
            markers = self.get_markers()
        """
        selected_markers_index = self.box_markers.currentIndex()
        selected_markers = self.box_markers.itemText(selected_markers_index)

        if selected_markers == 'Circle':
            return {'marker' : 'o' }
        elif selected_markers == 'Triangle':
            return {'marker' : '^' }
        elif selected_markers == 'Square':
            return {'marker' : 's' }   
        else:
            return {'marker' : None }
        
    def get_linewidth(self):
        """
        @brief Retrieves the selected line width from the `box_linewidth` combo box.

        This method returns the selected line width from the `box_linewidth` combo box. If no specific 
        line width is selected, it defaults to `1.0`.

        Returns:
            - dict: A dictionary containing the selected 'linewidth' as a float. Defaults to `1.0` if no line width is selected.

        Behavior:
            - Converts the selected line width to a float for use in plotting.

        Example usage:
            linewidth = self.get_linewidth()
        """
        selected_width_index = self.box_linewidth.currentIndex()
        selected_width = self.box_linewidth.itemText(selected_width_index)

        if selected_width != 'Linewidth':
            selected_width_converted = float(selected_width)
            return {'linewidth' : selected_width_converted}
        else:     
            return {'linewidth' : 1.0}
    
        
    
    
    
    def generate_graph(self):
        """
        @brief Generates graphs for Mossbauer factor and mean-square displacements (MSD) based on selected options.

        This method generates two types of graphs for each atom: one for the Mossbauer factor and one for the MSD 
        (mean-square displacements) based on the selected parameters (e.g., factor, x², y², z²). The method supports 
        both the case where experimental data is available and when it's not.

        Behavior:
            - Determines whether experimental data or loaded files are present and configures graphs accordingly.
            - Retrieves the selected resolution, color, line style, marker, and line width for plotting.
            - For each atom:
                - Generates a Mossbauer factor plot.
                - Generates an MSD plot with x², y², and z² components.
            - Appends the generated figures to the respective lists for Mossbauer factor and MSD.

        Graph types:
            - Mossbauer factor: Plots the factor for each atom using temperature as the x-axis.
            - MSD: Plots the MSD components (x², y², z²) for each atom using temperature as the x-axis.

        Attributes:
            - `self.loaded_files5` (list of str): Determines whether experimental data is available.
            - `self.loaded_files3`, `self.loaded_files4` (list of str): Check if relevant files are loaded.
            - `self.sing_temperature` (list of float): A list of single temperature values used when no files are loaded.
            - `self.temp_list` (list of float): A list of real temperature values used when files are loaded.
            - `self.factor_list` (list of lists): Stores the Mossbauer factors for each atom.
            - `self.mx1`, `self.my1`, `self.mz1` (list of lists): Stores MSD components for each atom.
            - `self.atom_names` (list of str): Stores the names of the atoms.
            - `self.factor_stored_kwargs_f`, `self.mx1_stored_kwargs`, `self.my1_stored_kwargs`, `self.mz1_stored_kwargs`:
                Stores selected plotting styles (color, line style, marker, line width) for the graphs.
            - `self.generated_graphs_factor`, `self.generated_graphs_mi1`: Lists to store the generated graphs.

        Example usage:
            self.generate_graph()
        """

        if not self.loaded_files5:
            if not self.loaded_files3 and not self.loaded_files4:    
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)

                resolution_settings = self.get_selected_resolution()
                if selected_ChooseWhich == 'Factor':
                    self.factor_stored_kwargs_f.clear()
                    self.factor_stored_kwargs_f.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'x^2':
                    self.mx1_stored_kwargs.clear()
                    self.mx1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'y^2':
                    self.my1_stored_kwargs.clear()
                    self.my1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'z^2':
                    self.mz1_stored_kwargs.clear()
                    self.mz1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                else:
                    return
                i= 1
                for i in range(1,len(self.atom_masses)+1):
                    fig1, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])  
                    ax.plot(self.sing_temperature, self.factor_list[int(i-1)], **self.factor_stored_kwargs_f)
                    ax.set_xlabel('T[K]')  
                    ax.set_ylabel('f') 
                    ax.set_title(f'Mossbauser factor for {self.atom_names[int(i-1)]}')  
                    ax.grid(False)  
                    ax.legend(['Factor'])
                    self.generated_graphs_factor.append(fig1)
                    
                    
                    fig2, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])
                    ax.plot(self.sing_temperature, self.mx1[int(i-1)], **self.mx1_stored_kwargs )
                    ax.plot(self.sing_temperature, self.mz1[int(i-1)], **self.mz1_stored_kwargs )
                    ax.plot(self.sing_temperature, self.my1[int(i-1)], **self.my1_stored_kwargs )
                    ax.set_xlabel('T[K]')  
                    ax.set_ylabel('MSD')  
                    ax.set_title(f'MSD for {self.atom_names[int(i-1)]}')  
                    ax.grid(False)  
                    ax.legend(['MSD of X','MSD of Z','MSD of Y'])
                    self.generated_graphs_mi1.append(fig2)
                
           
                
                
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)
            
            
            
            
            
            else:
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)

                resolution_settings = self.get_selected_resolution()
                if selected_ChooseWhich == 'Factor':
                    self.factor_stored_kwargs_f.clear()
                    self.factor_stored_kwargs_f.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'x^2':
                    self.mx1_stored_kwargs.clear()
                    self.mx1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'y^2':
                    self.my1_stored_kwargs.clear()
                    self.my1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'z^2':
                    self.mz1_stored_kwargs.clear()
                    self.mz1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                else:
                    return
                i= 1
                for i in range(1,len(self.atom_masses)+1):
                    fig1, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])  
                    ax.plot(self.temp_list, self.factor_list[int(i-1)], **self.factor_stored_kwargs_f)
                    ax.set_xlabel('T[K]') 
                    ax.set_ylabel('f') 
                    ax.set_title(f'Mossbauser factor for {self.atom_names[int(i-1)]}') 
                    ax.grid(False)
                    ax.legend(['Factor']) 
                    self.generated_graphs_factor.append(fig1)
                    
                    
                    fig2, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])
                    ax.plot(self.temp_list, self.mx1[int(i-1)], **self.mx1_stored_kwargs )
                    ax.plot(self.temp_list, self.mz1[int(i-1)], **self.mz1_stored_kwargs )
                    ax.plot(self.temp_list, self.my1[int(i-1)], **self.my1_stored_kwargs )
                    ax.set_xlabel('T[K]')  
                    ax.set_ylabel('MSD') 
                    ax.set_title(f'MSD for {self.atom_names[int(i-1)]}')  
                    ax.grid(False)  
                    ax.legend(['MSD of X','MSD of Z','MSD of Y'])
                    self.generated_graphs_mi1.append(fig2)
                
   
                
                
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)
        else:
            if not self.loaded_files3 and not self.loaded_files4:    
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)

                resolution_settings = self.get_selected_resolution()
                if selected_ChooseWhich == 'Factor':
                    self.factor_stored_kwargs_f.clear()
                    self.factor_stored_kwargs_f.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'x^2':
                    self.mx1_stored_kwargs.clear()
                    self.mx1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'y^2':
                    self.my1_stored_kwargs.clear()
                    self.my1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'z^2':
                    self.mz1_stored_kwargs.clear()
                    self.mz1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                else:
                    return
                i= 1
                for i in range(1,len(self.atom_masses)+1):
                    fig1, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])  
                    ax.plot(self.sing_temperature, self.factor_list[int(i-1)], **self.factor_stored_kwargs_f)  
                    ax.plot(self.xAxis, self.yAxis, marker='+', linestyle='None', markersize=10, color='b', label='Experimental results')
                    ax.set_xlabel('T[K]') 
                    ax.set_ylabel('f') 
                    ax.set_title(f'Mossbauser factor for {self.atom_names[int(i-1)]}')  
                    ax.grid(False)  
                    ax.legend(['Factor'])
                    self.generated_graphs_factor.append(fig1)
                    
                    
                    fig2, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])
                    ax.plot(self.sing_temperature, self.mx1[int(i-1)], **self.mx1_stored_kwargs )
                    ax.plot(self.sing_temperature, self.mz1[int(i-1)], **self.mz1_stored_kwargs )
                    ax.plot(self.sing_temperature, self.my1[int(i-1)], **self.my1_stored_kwargs )
                    ax.set_xlabel('T[K]')
                    ax.set_ylabel('MSD') 
                    ax.set_title(f'MSD for {self.atom_names[int(i-1)]}')  
                    ax.grid(False)  
                    ax.legend(['MSD of X','MSD of Z','MSD of Y'])
                    self.generated_graphs_mi1.append(fig2)
                
             
                
                
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)
            
            
            
            
            
            else:
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)

                resolution_settings = self.get_selected_resolution()
                if selected_ChooseWhich == 'Factor':
                    self.factor_stored_kwargs_f.clear()
                    self.factor_stored_kwargs_f.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'x^2':
                    self.mx1_stored_kwargs.clear()
                    self.mx1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'y^2':
                    self.my1_stored_kwargs.clear()
                    self.my1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                elif selected_ChooseWhich == 'z^2':
                    self.mz1_stored_kwargs.clear()
                    self.mz1_stored_kwargs.update(**self.get_selected_color(), **self.get_linestyle(), **self.get_markers(), **self.get_linewidth())
                else:
                    return
                i= 1
                for i in range(1,len(self.atom_masses)+1):
                    fig1, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])  
                    ax.plot(self.temp_list, self.factor_list[int(i-1)], **self.factor_stored_kwargs_f)
                    ax.plot(self.xAxis, self.yAxis, marker='+', linestyle='None', markersize=10, color='b', label='Experimental results')
                    ax.set_xlabel('T[K]') 
                    ax.set_ylabel('f') 
                    ax.set_title(f'Mossbauser factor for {self.atom_names[int(i-1)]}') 
                    ax.grid(False) 
                    ax.legend(['Factor']) 
                    self.generated_graphs_factor.append(fig1)
                    
                    
                    fig2, ax = plt.subplots(figsize=resolution_settings['figsize'], dpi=resolution_settings['dpi'])
                    ax.plot(self.temp_list, self.mx1[int(i-1)], **self.mx1_stored_kwargs )
                    ax.plot(self.temp_list, self.mz1[int(i-1)], **self.mz1_stored_kwargs )
                    ax.plot(self.temp_list, self.my1[int(i-1)], **self.my1_stored_kwargs )
                    ax.set_xlabel('T[K]') 
                    ax.set_ylabel('MSD')  
                    ax.set_title(f'MSD for {self.atom_names[int(i-1)]}')  
                    ax.grid(False) 
                    ax.legend(['MSD of X','MSD of Z','MSD of Y'])
                    self.generated_graphs_mi1.append(fig2)
                
              
                
                
                selected_ChooseWhich_index = self.ChooseWhich.currentIndex()
                selected_ChooseWhich = self.ChooseWhich.itemText(selected_ChooseWhich_index)
        

        
    
    
    
    
    
    
     
    def Choosing(self, index):
        """
        @brief Handles the selection of atom-related data (Atom Probability or Atom MSD) from the combo box.

        This method processes the selected item from `self.Box` (combo box). Based on whether the selection is 
        "Atom Probability" or "Atom MSD," it extracts the appropriate atom number from the selected text and 
        calls the corresponding handler method (`handleAtomProbability` or `handleAtomMSD`).

        Parameters:
            - index (int): The index of the selected item in the combo box.

        Behavior:
            - Checks the selected text for either "Atom Probability" or "Atom MSD."
            - Extracts the atom number from the selected text.
            - Calls `handleAtomProbability` if "Atom Probability" is selected.
            - Calls `handleAtomMSD` if "Atom MSD" is selected.

        Example usage:
            self.Choosing(index)
        """
        selected_text = self.Box.currentText()

        if "Atom Probability" in selected_text:
            atom_type = "Atom Probability"
        elif "Atom MSD" in selected_text:
            atom_type = "Atom MSD"
        else:
            atom_type = None
        
        if atom_type:
            selected_value = int(selected_text[-2:])
            self.i = selected_value
            if atom_type == "Atom Probability":
                self.handleAtomProbability(selected_value)
            elif atom_type == "Atom MSD":
                self.handleAtomMSD(selected_value)
        
    def handleAtomProbability(self, value):
        """
        @brief Displays the Mossbauer factor graph for the selected atom.

        This method displays the pre-generated Mossbauer factor graph for the selected atom 
        based on the provided `value`.

        Parameters:
            - value (int): The atom number for which the graph should be displayed.

        Behavior:
            - If the atom number is valid, displays the corresponding Mossbauer factor graph.
            - If the atom number is out of range, the method returns without action.

        Example usage:
            self.handleAtomProbability(value)
        """
        if 1 <= value <= len(self.generated_graphs_factor):
            self.displayMatplotlibFigure(self.generated_graphs_factor[int(value)-1])
        else:
            return

    def handleAtomMSD(self, value):
        """
        @brief Displays the mean-square displacement (MSD) graph for the selected atom.

        This method displays the pre-generated MSD graph for the selected atom based on the provided `value`.

        Parameters:
            - value (int): The atom number for which the graph should be displayed.

        Behavior:
            - If the atom number is valid, displays the corresponding MSD graph.
            - If the atom number is out of range, the method returns without action.

        Example usage:
            self.handleAtomMSD(value)
        """
        if 1 <= value <= len(self.generated_graphs_mi1):       

                self.displayMatplotlibFigure(self.generated_graphs_mi1[int(value)-1])
        else:
            return
    
    
    def Ploting(self):
        """
        @brief Clears and regenerates the graphs, then updates the display based on the current selection.

        This method clears the previously generated graphs, regenerates them using `generate_graph`, and 
        updates the display based on the current atom selection.

        Behavior:
            - Clears `self.generated_graphs_mi1` and `self.generated_graphs_factor`.
            - Regenerates the graphs by calling `generate_graph`.
            - Calls `Choosing(self.i)` to update the display based on the current atom selection.

        Example usage:
            self.Ploting()
        """
        self.generated_graphs_mi1.clear()
        self.generated_graphs_factor.clear()
        self.generate_graph()
        self.Choosing(self.i)

    

    

    
    def copyfiles(self):
        """
        @brief Copies the list of output files to the `files_to_delete` list.

        This method creates a copy of the `self.outfile` list, which contains paths to the output files, 
        and assigns it to `self.files_to_delete`. This allows for file deletion operations to be handled 
        without modifying the original list.

        Example usage:
            self.copyfiles()
        """
        self.files_to_delete = self.outfile.copy()         
    
    
    
    
    def Save_file(self):
        """
        @brief Saves the temperature, MSD (X, Y, Z components), and Mossbauer factor data to a file.

        This method allows the user to select a location to save the data. The file is saved as a text file 
        with columns representing temperature, MSD (X, Y, Z components), and Mossbauer factor values. 
        The data saved depends on whether files are loaded or not, determining if `self.sing_temperature` 
        or `self.temp_list` is used.

        Behavior:
            - If no files are loaded, uses `self.sing_temperature` for temperature values.
            - If files are loaded, uses `self.temp_list` for temperature values.
            - Opens a file dialog for the user to choose the save location and file name.
            - Writes the data in tab-separated format: temperature, MSD (X, Y, Z components), and factor.

        File format:
            - Columns: Temperature, MSD_x, MSD_y, MSD_z, Factor.

        Example usage:
            self.Save_file()
        """

        if not self.loaded_files3 and not self.loaded_files4:
            temperature = self.sing_temperature
        else:
            temperature = self.temp_list
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        i = 0 
        if file_path:
            with open(file_path, 'w') as file:
                for i in range(len(temperature) ):
                    temperature_str = f"{temperature[i]:0.10f}"
                    mx1_str = f"{self.mx1[int(self.i -1)][i]:0.10f}"
                    my1_str = f"{self.my1[int(self.i -1)][i]:0.10f}"
                    mz1_str = f"{self.mz1[int(self.i -1)][i]:0.10f}"
                    factor_str = f"{self.factor_list[int(self.i -1)][i]:0.10f}"
                    file.write(f"{temperature_str}\t{mx1_str}\t{my1_str}\t{mz1_str}\t{factor_str}\n")


    
    
    def PROCESSING(self):
        """
        @brief Processes atomic data, mean-square displacements, and Mossbauer factor calculations.

        This method handles the entire data processing workflow for both cases where thermal-displacement 
        files (`loaded_files3` and `loaded_files4`) are loaded and where they are not. It clears previous 
        data, retrieves atomic information, extracts temperature and volume data, processes mean-square 
        displacements (MSD), and calculates the Mossbauer factor.

        Behavior:
            - Clears various data structures used in the processing (e.g., temperature, MSD, factor, atom info).
            - Depending on whether thermal-displacement files are loaded:
                - If no files are loaded:
                    - Extracts temperature data from a single thermal-displacement file.
                    - Cleans and processes the MSD data for interpolation.
                    - Calculates Mossbauer factors and updates the combo box.
                - If files are loaded:
                    - Extracts volume and temperature data, processes MSD, interpolates results, and calculates 
                    Mossbauer factors.
            - Calls several helper methods to perform specific tasks during the workflow.
            - Deletes cleaned files after processing is complete.

        Workflow for no thermal-displacement files:
            - Clears existing data.
            - Extracts atomic information and maps atom names to numbers.
            - Extracts temperature data.
            - Cleans data and copies files for processing.
            - Interpolates MSD data and calculates Mossbauer factors.
            - Updates the combo box with new data and deletes cleaned files.

        Workflow for loaded thermal-displacement files:
            - Clears existing data.
            - Extracts atomic information and maps atom names to numbers.
            - Extracts volume and temperature data.
            - Cleans data and copies files for processing.
            - Counts values smaller than the first volume, removes unphysical values.
            - Processes MSD and performs interpolation.
            - Updates the combo box with new data and deletes cleaned files.

        Example usage:
            self.PROCESSING()
        """
        if not self.loaded_files3 and not self.loaded_files4:   
            self.Er_const_list.clear() 
            self.real_temp.clear()
            self.data_list_x.clear()
            self.data_list_y.clear()
            self.data_list_z.clear()
            self.data_sing_list.clear()
            self.result.clear()
            self.outfile.clear()
            self.mx1.clear()
            self.my1.clear()
            self.mz1.clear()
            self.mx.clear()
            self.my.clear()
            self.mz.clear()
            self.ev_vol_list.clear()
            self.factor_list.clear()
            self.mx2.clear()
            self.my2.clear()
            self.mz2.clear()
            self.atom_masses.clear()
            self.atom_names.clear()
            self.atom_numbers.clear()
            self.count.clear() 
            self.sing_temperature.clear()
            
            self.get_atom_info()
            self.map_names_to_numbers()
            self.extract_temperatures()
            self.Cleaning()
            self.copyfiles()
            self.Msd_sing()
            self.sing_Msd_interpol()
            self.GenerateComboBox()
            self.Mfactor()
            
            
            #self.sing_Msd_interpol()
            #self.GenerateComboBox()
            #self.Mfactor()
            self.DeletingCleanedFiles()

        else:   
            self.Er_const_list.clear() 
            self.real_temp.clear()
            self.data_list_x.clear()
            self.data_list_y.clear()
            self.data_list_z.clear()
            self.result.clear()
            self.outfile.clear()
            self.mx1.clear()
            self.my1.clear()
            self.mz1.clear()
            self.mx.clear()
            self.my.clear()
            self.mz.clear()
            self.ev_vol_list.clear()
            self.factor_list.clear()
            self.mx2.clear()
            self.my2.clear()
            self.mz2.clear()
            self.atom_masses.clear()
            self.atom_names.clear()
            self.atom_numbers.clear()
            self.count.clear()
            self.fit_list_x_temp_ordered.clear()
            self.fit_list_y_temp_ordered.clear()
            self.fit_list_z_temp_ordered.clear()
            self.fit_list_x.clear()
            self.fit_list_y.clear()
            self.fit_list_z.clear()


            self.get_atom_info()
            self.map_names_to_numbers()
            self.ev_volume()
            self.temp_vol()
            self.Cleaning()
            self.copyfiles()
            self.Msd()
            
            #self.Msd_interpol()
            self.Sort()
            
            self.Fitting()
            
            
            self.Imputing()
            
            self.GenerateComboBox()
            
            self.Mfactor()
            self.DeletingCleanedFiles()

    
    

    
    #def exception_hook(self, exctype, value, traceback):
        
        """
        @brief Handles uncaught exceptions by displaying an error message in a message box.

        This method catches uncaught exceptions and displays an error message in a `QMessageBox`. 
        The exception type and message are shown to the user.

        Parameters:
            - exctype: The type of the exception that was raised.
            - value: The exception instance or value.
            - traceback: The traceback object representing the call stack at the point the exception was raised.

        Behavior:
            - Constructs an error message using the exception type and message.
            - Displays the error message in a critical `QMessageBox`.

        Example usage:
            sys.excepthook = self.exception_hook
        """
        
        #error_message = f"An error occurred: {exctype.__name__}: {value}"
        #QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
        


    def closeEvent(self, event):
        """
        @brief Handles the window close event by prompting the user for confirmation.

        This method is called when the user attempts to close the window. It displays a confirmation dialog asking 
        if the user is sure they want to close the window. If the user confirms, the window is closed, and cleaned 
        files are deleted. Otherwise, the close event is ignored.

        Parameters:
            - event (QCloseEvent): The event triggered by attempting to close the window.

        Behavior:
            - Displays a confirmation dialog with Yes and No options.
            - If Yes is selected, closes the window and deletes cleaned files.
            - If No is selected, ignores the close event and keeps the window open.

        Example usage:
            This method is automatically called when the window close event occurs.
        """
        reply = QMessageBox.question(self, "Close Window", "Are you sure you want to close the window?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.DeletingCleanedFiles()
        else:
            event.ignore()




def window ():
    """
    @brief Initializes and starts the main application window.

    This function creates the QApplication instance and initializes the main window (`my_window`). 
    It sets the window icon, shows the window, and enters the application's main event loop.

    Example usage:
        window()  # This will start the application.
    """
    app = QApplication(sys.argv)
    win = my_window()
    app.setWindowIcon(QIcon("Logo.jpg"))
        

    win.show()

    sys.exit(app.exec_())



window()