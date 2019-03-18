import pyaudio
import wave
 
def record_audio(ten, output):
    #--------- SETTING PARAMS FOR OUR AUDIO FILE ------------#
    FORMAT = pyaudio.paInt16    # format of wave
    CHANNELS = 2                # no. of audio channels
    RATE = 44100                # frame rate
    CHUNK = 1024                # frames per audio sample
    #--------------------------------------------------------#
 
    # creating PyAudio object
    audio = pyaudio.PyAudio()
 
    # open a new stream for microphone
    # It creates a PortAudio Stream Wrapper class object
    stream = audio.open(format=FORMAT,channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
 
    #----------------- start of recording -------------------#
    print("Listening...")
 
    # list to save all audio frames
    frames = []
 
    for i in range(int(RATE / CHUNK * ten)):
        # read audio stream from microphone
        data = stream.read(CHUNK)
        # append audio data to frames list
        frames.append(data)
 
    #------------------ end of recording --------------------#
    print("Finished recording.")
 
    stream.stop_stream()    # stop the stream object
    stream.close()          # close the stream object
    audio.terminate()       # terminate PortAudio
 
    #------------------ saving audio ------------------------#
 
    # create wave file object
    waveFile = wave.open(output, 'wb')
 
    # settings for wave file object
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
 
    # closing the wave file object
    waveFile.close()
 
def read_audio(output):
    # function to read audio(wav) file
    with open(output, 'rb') as f:
        audio = f.read()
    return audio
