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
    plt.title("Wave data")


    for filePath in filePaths:
        print(filePath)
        # open the file using wave 
        file = wave.open(filePath,"r")

        # Read the wav as 16 bit integers
        raw = file.readframes(-1)
        signal = np.frombuffer(raw,"int16")
        
        #Plot
        plt.plot(signal)

    usrFileName = input("\nWhat would you like to name the graph? (.png)\n")

    plt.savefig('outputs/' + usrFileName + '.png')

