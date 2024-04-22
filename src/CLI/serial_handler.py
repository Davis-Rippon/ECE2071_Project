def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool):
    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n"
        f"Ultrasonic Sensor: {ultrasonicState} \n")