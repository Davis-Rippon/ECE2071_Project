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
        self.ultrasonicState = True

    def print(self):
        """
        Print the current settings
        """
        print(f"Sampling Rate: {self.samplingRate} Hz\n" +
        f"Max Audio Duration: {self.audioDuration} seconds\n" + 
        f"Acceptable Range: <{self.acceptableRange} cm\n" +
        f"Ultrasonic Sensor: {'On' if self.ultrasonicState else 'Off'}\n")


    def set_sampling_rate(self):
        """
        Prompt the user for a new sampling rate
        """
        while True:

            try:
                self.samplingRate = int(input("New Sampling Rate (0-6000 Hz): "))
                if self.samplingRate > 6000 or self.samplingRate < 0:
                    raise AssertionError
                break
            except:
                pass

    def set_audio_duration(self):
        """
        Prompt the user for a new audio duration
        """
        while True:

            try:
                self.audioDuration = int(input("New audio duration (Non-Negative): "))
                if self.audioDuration < 0:
                    raise AssertionError
                break
            except:
                pass

    def set_acceptable_range(self):
        """
        Prompt the user for a new US sensor range
        """
        while True:

            try:
                self.acceptableRange = int(input("New Ultrasonic Sensor range (0-100cm): "))
                if self.acceptableRange < 0 or self.acceptableRange > 100:
                    raise AssertionError
                break
            except:
                pass

    def toggle_ultrasonicState(self):
        """
        Toggle ultrasonic sensor
        """
        self.ultrasonicState = not self.ultrasonicState


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
        "Toggle Ultrasonic Sensor" : RecordingData.toggle_ultrasonicState,
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
    serial_handler.start_recording(recordingData.samplingRate,recordingData.audioDuration, recordingData.acceptableRange, recordingData.ultrasonicState)

def start_us():
    serial_handler.start_recording_us(recordingData.samplingRate,recordingData.audioDuration, recordingData.acceptableRange)

def main():
    menu.clear()
    options = {
        "Start Recording" : start,
        "Start Recording with Ultrasonic Sensor" : start_us,
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