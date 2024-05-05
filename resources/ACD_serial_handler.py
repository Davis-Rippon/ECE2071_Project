import serial.tools.list_ports as serial_ports
import serial
import time
import struct

portList = serial_ports.comports()
STMPort = None

for port in portList:
    if "STM" in str(port):
        print(str(port))
        STMPort = str(port.device)

if STMPort is not None:
    serialPort = serial.Serial(STMPort, 460800)
    if not serialPort.is_open:
        print("ERROR: Port failed to open")
    print("Port opened successfully!")
else:
    print("Port not found!")

f = open('myfile.txt', 'w')

try:
    while True:
        if serialPort.in_waiting >= 1:
            data = serialPort.read(2)            
            value = int.from_bytes(data, byteorder="little", signed=False)
            if value > 5000:
                value = int.from_bytes(data, byteorder="big", signed=False)
            f.write(f"{value}\n")
            print(f"{value}")
except KeyboardInterrupt:
    serialPort.close()
    f.close()
    exit(0)



