"""
This file contains the logic that is used to handle all multiple choice prompts in our CLI.

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024

Dependencies: 
- simple-term-menu
"""


from simple_term_menu import TerminalMenu
import os

"""
Menu Class.

Uses simple-term-menu to create real-time interactible menus. 
"""
class Menu:
    def multi_select(selections: list) -> None:
        """
        Displays a list of strings as an interactible, multi-choice menu and returns the indexes of the user's selections in a list
        """
        terminalMenu = TerminalMenu(selections,multi_select=True,multi_select_select_on_accept=False) # Create TerminalMenu Object with the selections
        selection_indexes = list(terminalMenu.show()) # store the user's selection in "selection_index"
        return selection_indexes
        

    def list_menu(selections: list) -> None: 
        """
        Displays a list of strings as an interactible menu and returns the string of the user's selection 
        """
        terminalMenu = TerminalMenu(selections) # Create TerminalMenu Object with the selections
        selection_index = terminalMenu.show() # store the user's selection in "selection_index"
        selection = selections[selection_index] # select the key they chose
        return selection


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

    def list_datafile_names(directory="./data"):
        """
        Returns a list of the files in a diretory. By default, this is the /data directory
        """
        return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


def clear():
    """
    Clears the terminal on windows, linux and mac
    """
    os.system('cls' if os.name == 'nt' else 'clear')
