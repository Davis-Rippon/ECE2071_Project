"""
Main code for CLI.

**NOTE: for file access to work, must be run from the root folder "ECE2071_PROJECT"

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024

Dependencies:
-simple-term-menu
- matplotlib
- numpy
"""

import menu
import plot
import recording


def plot_option():
    menu.clear()
    print("Select files to plot (SPACEBAR to select, ENTER to confirm) \n")

    files = menu.Menu.list_datafile_names("./data/wav")
    indexes = menu.Menu.multi_select(files)

    plot.plot_wav([('data/wav/' + files[i]) for i in indexes]) # list of all file names with 'data/' at the beginning 

def record_option():
    recording.main()

def back():
    raise AssertionError

def main():
    options = {
        "Plot" : plot_option,
        "Record" : record_option,
        "Exit" : back
    }
    while True:
        menu.clear()
        print("Main Menu")
        try: 
            menu.Menu.dict_menu(options)

        except AssertionError as e:
            menu.clear()
            print("Exiting program... ")
            break



main()