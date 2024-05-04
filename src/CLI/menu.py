"""
This file contains the logic that is used to handle all multiple choice prompts in our CLI.

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024

Dependencies: 
None
"""


from simple_term_menu import TerminalMenu
import os

"""
Menu Class.

Creates real-time, interactible menus in command prompt 
"""
class Menu:
    def multi_select(selections: list) -> None:
        """
        Displays Selection of numbered options and takes multiple user inputs 
        """
        selectedIndexes = set() # Represents the selections the user currently has. A set cannot have duplicates, just like a 
                                # user selection cannot have duplicates

        while True:
            clear()
            print("Select files to plot \n")

            for index, selectionOption in enumerate(selections): # Print the options to select
                print(f"{index+1}. ({'*' if index in selectedIndexes else ' '}) {selectionOption}")
            
            indexSelection = input("\nSelect an option (Multi-Select), or press ENTER to confirm: ")

            if indexSelection == "": # I
                break

            try: 
                indexSelection = int(indexSelection) - 1
                assert indexSelection >= 0 and indexSelection < len(selections)
                
                if indexSelection in selectedIndexes:
                    selectedIndexes.remove(indexSelection) #Remove if the user has already selected the index
                else:
                    selectedIndexes.add(indexSelection) # add if it's not already selected
            except:
                continue

        if len(selectedIndexes) == 0:
            raise AssertionError

        return [indexes for indexes in selectedIndexes]
        

    def list_menu(selections: list) -> None: 
        """
        Prints a list of selections and lets the user make a selection from them.
        """
        while True:
            for index, selectionOption in enumerate(selections):
                print(f"{index+1}. {selectionOption}")
            
            try: # An invalid choice will throw an error
                selection_index = int(input(f"Select an option (1-{len(selections)}): ")) - 1 
                selection = selections[selection_index] # select the key they chose
            except: # If invalid choice, clear and try again
                clear()
                continue

            return selection #if valid choice, return 


    def dict_menu(selections: dict, arg=None) -> None:
        """.
        This method takes a dictionary that maps keys to functions, uses TerminalMenu 
        to get a user's selected key, then runs the function associated with that key
        """
        selection = Menu.list_menu(list(selections.keys())) # Passes a list of keys to list_menu and gets what key the user selects
        selected_function = selections.get(selection)  # Gets the value of that key, which is a function
        if arg is not None:
            selected_function(arg)
            return
        selected_function() #runs that function

    def list_datafile_names(directory="./data/wav"):
        """
        Returns a list of the files in a diretory. By default, this is the /data/wav directory
        """
        return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


def clear():
    """
    Clears the terminal on windows, linux and mac
    """
    os.system('cls' if os.name == 'nt' else 'clear')
