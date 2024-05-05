import serial.tools.list_ports as serial_ports
import serial
import menu
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

    serialPort = serial.Serial(STMPort, 460800)

    if not serialPort.is_open:
        input("Port failed to open! \n\nPress ENTER to return to recording menu")
        raise AssertionError

    fileName = input("Name the .data file ('<name>.data'): ")
    menu.clear()

    f = open(fileName + '.data', 'w')

    # Adjustible sampling rate logic:
    numTaken = 1
    numTotal = 1

    removeNum = 6000 - samplingRate

    # So that we can count the time/interrupt recording when maxAudio has been exceeded:
    endTime = time.time() + audioDuration

    print("Started recording...\n\n" +
        f"Sampling Rate: {samplingRate} Hz\n" +
        f"Maximum Audio Duration: {audioDuration} seconds\n" + 
        f"Acceptable Range: {acceptableRange} cm\n" + 
        "\nPress ctrl + c to stop recording.")
    try:
        while True:
            if time.time() > endTime:
                raise AssertionError

            if serialPort.in_waiting >= 1:
                data = serialPort.read(2)            
                value = int.from_bytes(data, byteorder="little", signed=False)
                
                if 30000 > value > 10100: # valid ultrasonic values are all > 10100 and < 30,000
                    distance = 340*(value-10000)*(10**(-4))/2 # Distance in cm
                    if not distance > acceptableRange and ultrasonicState: # if not out of range and ultrasonic is being considered
                        f.write(f"{value}\n")
                        continue

                    elif ultrasonicState: # 
                        input("Moved out of range, recording stopped.\n")
                        raise AssertionError
                        continue

                if value > 30000: # flipped bytes due to high speed
                    value = int.from_bytes(data, byteorder="big", signed=False)

                
                if (numTaken+1)*(6000-2) - (numTotal + 1)*(6000-removeNum) < (6000-2)/2: # Algorithm for ignoring values based on sampling rate.
                    numTaken += 1
                    numTotal += 1
                    f.write(f"{value}\n")

                else:
                    numTotal +=1

    except KeyboardInterrupt:
        serialPort.close()
        f.close()
        raise AssertionError
    
def start_recording_us(samplingRate: int, audioDuration: int, acceptableRange: int):
    portList = serial_ports.comports()

    STMPort = None
    
    for port in portList:
        if "STM" in str(port):
            STMPort = str(port.device)
            print("STM32 Found at port '" + str(port) + "'\n")

    if STMPort is None:
        input("STM32 Not found! Check Connection.\n\nPress ENTER to return to main menu ")
        raise AssertionError

    serialPort = serial.Serial(STMPort, 460800)

    if not serialPort.is_open:
        input("Port failed to open! \n\nPress ENTER to return to recording menu")
        raise AssertionError

    fileName = input("Name the .data file ('<name>.data'): ")
    menu.clear()

    f = open(fileName + '.data', 'w')

    # Adjustible sampling rate logic:
    numTaken = 1
    numTotal = 1

    removeNum = 6000 - samplingRate

    # So that we can count the time/interrupt recording when maxAudio has been exceeded:
    endTime = time.time() + audioDuration

    print("Waiting for user to be in range...")
    
    try:
        while True:

            if serialPort.in_waiting >= 1:
                data = serialPort.read(2)            
                value = int.from_bytes(data, byteorder="little", signed=False)
                
                if 30000 > value > 10100: # valid ultrasonic values are all > 10100 and < 30,000
                    distance = 340*(value-10000)*(10**(-4))/2 # Distance in cm
                    if not distance > acceptableRange: # if not out of range and ultrasonic is being considered
                        break

    except KeyboardInterrupt:
        serialPort.close()
        f.close()
        raise AssertionError

    print("\nStarted Recording... \n" + 
        f"Sampling Rate: {samplingRate} Hz\n" +
        f"Maximum Audio Duration: {audioDuration} seconds\n" + 
        f"Acceptable Range: {acceptableRange} cm\n" + 
        "\nPress ctrl + c to stop recording.")

    try:
        while True:
            if time.time() > endTime:
                raise AssertionError

            if serialPort.in_waiting >= 1:
                data = serialPort.read(2)            
                value = int.from_bytes(data, byteorder="little", signed=False)
                
                if 30000 > value > 10050: # valid ultrasonic values are all > 10050 and < 30,000
                    distance = 340*(value-10000)*(10**(-4))/2 # Distance in cm
                    if not distance > acceptableRange: # if not out of range and ultrasonic is being considered
                        f.write(f"{value}\n")
                        continue

                    else: 
                        input("Moved out of range, recording stopped.\n")
                        raise AssertionError
                        continue

                if value > 30000: # flipped bytes due to high speed
                    value = int.from_bytes(data, byteorder="big", signed=False)

                
                if (numTaken+1)*(6000-2) - (numTotal + 1)*(6000-removeNum) < (6000-2)/2: # Algorithm for ignoring values based on sampling rate.
                    numTaken += 1
                    numTotal += 1
                    f.write(f"{value}\n")

                else:
                    numTotal +=1

    except KeyboardInterrupt:
        serialPort.close()
        f.close()
        raise AssertionError
