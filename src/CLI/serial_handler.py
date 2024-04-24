import serial.tools.list_ports as serial_ports
import serial
import time

def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool, waitForUS: bool = False):
    portList = serial_ports.comports()
    
    for port in portList:
        if "STM" in str(port):
            print(str(port))
            STMPort = str(port.device)
            input()

    if STMPort == None:
        input("STM32 Not found! Check Connection.\n\nPress ENTER to return to main menu")
        raise AssertionError


    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n" + 
        f"Ultrasonic Sensor: {'On' if ultrasonicState else 'Off'} \n" +
        f"Wait for US to begin recording: {'Yes' if waitForUS else 'No'} \n\n" +
        "Your audio has been saved to outputs as a .wav (Test). \n")