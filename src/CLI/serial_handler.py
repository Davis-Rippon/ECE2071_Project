def start_recording(samplingRate: int, audioDuration: int, acceptableRange: int, ultrasonicState: bool, waitForUS: bool = False):
    print("started recording with: \n" +
        f"Sampling Rate: {samplingRate}\n" +
        f"Audio Duration: {audioDuration}\n" + 
        f"Acceptable Range: {acceptableRange}\n" + 
        f"Ultrasonic Sensor: {'On' if ultrasonicState else 'Off'} \n" +
        f"Wait for US to begin recording: {'Yes' if waitForUS else 'No'} \n\n" +
        "Your audio has been saved to outputs as a .wav (Test). \n")