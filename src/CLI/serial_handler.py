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

    while True:
        try:
            print("0")
            if serialPort.in_waiting >= 1:
                data = serialPort.read(1)
                print(data)

                if data == b'S':
                    print("2")
                    byteValue = serialPort.read(4)
                    integerValue = int.from_bytes(byteValue, byteorder="little", signed=False)

                    print("Recieved Data: " + integerValue)

        except KeyboardInterrupt as e:
            print("Exiting and closing ports")
            break
    
    serialPort.close()

    




    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n" + 
        f"Ultrasonic Sensor: {'On' if ultrasonicState else 'Off'} \n" +
        f"Wait for US to begin recording: {'Yes' if waitForUS else 'No'} \n\n" +
        "Your audio has been saved to outputs as a .wav (Test). \n")