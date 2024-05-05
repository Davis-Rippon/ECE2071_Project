import serial.tools.list_ports as serial_ports
import serial
import time

def ss_recording():
    """
    Record on Stop/Start mode.
    """


def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool, waitForUS: bool = False):
    portList = serial_ports.comports()

    STMPort = None
    
    for port in portList:
        if "STM" in str(port):
            STMPort = str(port.device)
            print("STM32 Found at port '" + str(port) + "'\n")

    if STMPort is None:
        input("STM32 Not found! Check Connection.\n\nPress ENTER to return to main menu ")
        raise AssertionError

    serialPort = serial.Serial(STMPort, 115200)

    if not serialPort.is_open:
        input("Port failed to open! \n\nPress ENTER to return to recording menu")
        raise AssertionError
    
    serialPort.close()

    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n")