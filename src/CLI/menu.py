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
    """
    Displays a list of strings as an interactible menu and returns the string of the user's selection 
    """
    def list_menu(selections: list) -> None: 
        terminalMenu = TerminalMenu(selections) # Create TerminalMenu Object with the selections
        selection_index = terminalMenu.show() # store the user's selection in "selection_index"
        selection = selections[selection_index] # select the key they chose
        return selection

    """.
    This method takes a dictionary that maps keys to functions, uses TerminalMenu 
    to get a user's selected key, then runs the function associated with that key
    """
    def dict_menu(selections: dict, arg=None) -> None:
        selection = Menu.list_menu(list(selections.keys())) # Passes a list of keys to list_menu and gets what key the user selects
        selected_function = selections.get(selection)  # Gets the value of that key, which is a function
        if arg is not None:
            selected_function(arg)
            return
        selected_function() #runs that function

def clear():
    """
    Clears the terminal on windows, linux and mac
    """
    os.system('cls' if os.name == 'nt' else 'clear')


"""
# example usage of this menu system, uncomment and run menu.py to see how it works. To be removed.

def start():
    print("start")

def create_recording():
    print("create recording")

def view_status(): 
    print("view_status")

def quit(): 
    print("quit")

def main():
    options = {
      "Start": start,
      "Create Recording": create_recording,
      "View Status": view_status,
      "Quit": quit
      }
    Menu.dict_menu(options)

main()
"""