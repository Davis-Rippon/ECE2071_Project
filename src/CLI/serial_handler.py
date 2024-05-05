import serial.tools.list_ports as serial_ports
import serial
import time

def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool):
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

    f = open('myfile.txt', 'w')

    # Adjustible sampling rate logic:
    numTaken = 1
    numTotal = 1

    removeNum = 6000 - samplingRate

    try:
        while True:
            if serialPort.in_waiting >= 1:
                data = serialPort.read(2)            
                value = int.from_bytes(data, byteorder="little", signed=False)
                
                if value > 9999: # ultrasonic values are all > 9999
                    distance = 340*(value)*(10**(-4))/2 # Distance in cm
                    if not distance > acceptableRange and ultrasonicState: # if out of range and ultrasonic is being considered
                        f.write(f"{value}\n")
                        continue

                    elif ultrasonicState:
                        input("Moved out of range, recording stopped.\n")
                        raise AssertionError
                        continue
                
                if (numTaken+1)*(6000-2) - (numTotal + 1)*(6000-removeNum) < (6000-2)/2: # Algorithm for ignoring values based on sampling rate.
                    numTaken += 1
                    numTotal += 1
                    f.write(f"{value}\n")
                    print(f"ADDED: \n\n{value}\n\n")

                else:
                    numTotal +=1

                    print(f"REMOVED***\n\n{value}\n\n")

    except KeyboardInterrupt:
        serialPort.close()
        f.close()
        raise AssertionError
    
    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n")