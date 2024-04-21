"""
Main code for CLI.

**NOTE: for file access to work, must be run from the root folder "ECE2071_PROJECT"

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024
"""

import menu 
import plot
import os

def plot_option():
    options = {
        "Plot .wav (Raw)" : plotw,
        "Plot .wav (Filtered)" : plotw,
        "Go Back" : back
    }
    while True:
        try: 
            menu.Menu.dict_menu(options)

        except AssertionError as e:
            break

def plotw(): 
    wav_file = input("Enter the path of a .wav file to plot: ")
    plot.plot_wav(wav_file)

def back():
    raise AssertionError


def main():
    options = {
        "Plot" : plot_option,
        "Exit" : back
    }
    while True:
        try: 
            menu.Menu.dict_menu(options)

        except AssertionError as e:
            print("Exiting program... ")
            break



main()