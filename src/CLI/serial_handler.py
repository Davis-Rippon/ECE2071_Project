def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool, waitForUS: bool = False):
    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n"
        f"Ultrasonic Sensor: {ultrasonicState} \n" + 
        "Your audio has been saved to outputs as a .wav (Test). \n")