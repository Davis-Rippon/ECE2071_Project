"""
Recording related functions/class, intended to control the state of the serial handler (and consequently, the embedded system)

Author: Davis Rippon
Version: 1.0
Date Last Edited: April 21st 2024

Dependencies:
None
"""
import serial_handler
import menu
import os

class RecordingData:
    """
    This class carries all the settings for recording, and contains methods for changing/accessing attributes
    """

    def __init__(self):
        """
        Set the default values for recording
        """
        self.samplingRate = 6000
        self.audioDuration = 120
        self.acceptableRange = 10

    def print(self):
        """
        Print the current settings
        """
        print(f"Sampling Rate: {self.samplingRate} Hz\n" +
        f"Max Audio Duration: {self.audioDuration} seconds\n" + 
        f"Acceptable Range: <{self.acceptableRange} cm\n" )


    def set_sampling_rate(self):
        """
        Prompt the user for a new sampling rate
        """
        self.samplingRate = input("New Sampling Rate: ")

    def set_audio_duration(self):
        """
        Prompt the user for a new audio duration
        """
        self.audioDuration = input("New Audio Duration: ")

    def set_acceptable_range(self):
        """
        Prompt the user for a new US sensor range
        """
        self.acceptableRange = input("New Sensor Range: ")



    def reset(self):
        """
        Reset to default values
        """
        self.__init__() # Calling the constructor will reset all the values back to default

"""`
This RecordingData object gets created when we IMPORT it to main (before we invoke main())
Because of this this, all of the recording attributes stay the same, regardless of what's happening in the program
"""

recordingData = RecordingData()

def settings() -> None:
   
    options = {
        "Adjust Sampling Rate" : RecordingData.set_sampling_rate,
        "Adjust Audio Duration" : RecordingData.set_audio_duration,
        "Adjust Ultrasonic Range" : RecordingData.set_acceptable_range,
        "Reset to defaults" : RecordingData.reset,
        "Back" : back
    }
    while True:
        menu.clear()
        print("Recording Settings\n")
        recordingData.print()
        try: 
            menu.Menu.dict_menu(options, recordingData)

        except:
            menu.clear()
            break



def start():
    menu.clear()
    options = {
        "Stop/Start Mode" : serial_handler.ss_recording,
        "Ultrasonic Mode" : serial_handler.us_recording,
    }

    while True:
        try:
            print("Recording Mode")
            menu.Menu.dict_menu(options)
        except AssertionError as e:
            break

def main():
    menu.clear()
    options = {
        "Start Recording" : start,
        "Recording Settings" : settings,
        "Back" : back
    }
    while True:
        try: 
            print("Recording Options")
            menu.Menu.dict_menu(options)

        except AssertionError as e:
            break

def back():
    raise AssertionError