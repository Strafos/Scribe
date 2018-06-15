"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import audioop
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = "output.wav"
THRESHOLD = 400

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def record_segments(pause):
    # After pause, segment will be stopped
    pause_len = RATE / CHUNK * pause
    frames = []

    counter = 0
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        rms = audioop.rms(data, 2)
        if rms < THRESHOLD:
            counter += 1
            if counter < pause_len: 
                return frames
        else:
            counter = 0

count = 0
while True:
    print("Written to file")
    frames = record_segments(2)

    stream.stop_stream()
    stream.close()
    p.terminate()

    filename = WAVE_OUTPUT_FILENAME + str(count)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()