"""
This file contains the function for plotting .wav

TODO: Add function for plotting .csv

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024

Dependencies: 
- matplotlib
- numpy
"""

import matplotlib.pyplot as plt
import numpy as np
import wave


def plot_wav(filePaths: list[str]):
    """
    plots multiple .wavs in one figure.
    """

    plt.figure(1)
    plt.title("Wave Data Plot")


    for filePath in filePaths:
        print(filePath)
        # open the file using wave 
        file = wave.open(filePath,"r")

        # Read the wav as 16 bit integers
        raw = file.readframes(-1)
        signal = np.frombuffer(raw,"int16")
        
        #Plot
        plt.plot(signal,label=filePath)
        
    plt.legend(loc="upper left")

    usrFileName = input("\nWhat would you like to name the plot?\n")

    plt.savefig('outputs/' + usrFileName + '.png')
    input(f"\nSuccessfully saved at {'outputs/' + usrFileName + '.png'}. Press ENTER to go back to main menu. ")
    plt.close()

