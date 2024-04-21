"""
This file contains the "Menu" class that is used to handle all multiple choice prompts in our CLI.

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024
"""


from simple_term_menu import TerminalMenu

class Menu:
    def list_menu(selections: list) -> None:
        terminalMenu = TerminalMenu(selections) # Create TerminalMenu Object with the selections
        selection_index = terminalMenu.show() # store the user's selection in "selection_index"
        selection = selections[selection_index] #
        return selection

    def dict_menu(selections: dict) -> None:
        selection = Menu.list_menu(list(selections.keys())) 
        selected_function = selections.get(selection) 
        selected_function() 



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