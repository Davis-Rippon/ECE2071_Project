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
        self.samplingRate = 6000
        self.audioDuration = 120
        self.acceptableRange = 10
        self.ultrasonicState = True



    def print(self):
        print(f"Sampling Rate: {self.samplingRate}\n" +
        f"Audio Duration: {self.audioDuration}\n" + 
        f"Acceptable Range: {self.acceptableRange}\n"
        f"Ultrasonic Sensor: {'On' if self.ultrasonicState else 'Off'} \n")

    def set_sampling_rate(self):
        self.samplingRate = input("New Sampling Rate: ")

    def set_audio_duration(self):
        self.audioDuration = input("New Audio Duration: ")

    def set_acceptable_range(self):
        self.acceptableRange = input("New Sensor Range: ")

    def toggle_US(self):
        self.ultrasonicState = not self.ultrasonicState

    def reset(self):
        self.__init__()


# Create recording data object upon IMPORTING this file to main.py

global recordingData

recordingData = RecordingData()

def settings() -> None:
   
    options = {
        "Adjust Sampling Rate" : RecordingData.set_sampling_rate,
        "Adjust Audio Duration" : RecordingData.set_audio_duration,
        "Adjust Ultrasonic Range" : RecordingData.set_acceptable_range,
        "Toggle Ultrasonic Sensor" : RecordingData.toggle_US,
        "Reset to defaults" : RecordingData.reset,
        "Back" : back
    }
    while True:
        menu.clear()
        recordingData.print()
        try: 
            menu.Menu.dict_menu(options, recordingData)

        except:
            menu.clear()
            break

def start():
    serial_handler.start_recording(recordingData.samplingRate, recordingData.audioDuration, recordingData.acceptableRange, recordingData.ultrasonicState)
    

def back():
    raise AssertionError

def main():
    menu.clear()
    options = {
        "Start Recording" : start,
        "Recording Settings" : settings,
        "Back" : back
    }
    while True:
        try: 
            menu.Menu.dict_menu(options)

        except AssertionError as e:
            break

