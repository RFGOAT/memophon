#!/usr/bin/python3
import RPi.GPIO as GPIO
import math, sys, os
import subprocess
import time
import pyaudio
import wave


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def PulseCounter():
    P = 0
    GPIO.wait_for_edge(23, GPIO.FALLING)
    while 1:
        P = P + 1
        GPIO.wait_for_edge(23, GPIO.FALLING, timeout=1000)
        if GPIO.input(23) == 1:  # static high detected. Must be timeout
            if P == 10:  # 10 Pulses equal 0
                P = 0
            print('return')
            return P


def Record(filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    # filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# *****************START***************************


while 1:
    print('start')
    # wait for phone to be lifted
    GPIO.wait_for_edge(18, GPIO.RISING)
    print('abgenommen')
    time.sleep(0.1)  # wait 100 ms to give CPU chance to do other things

    Pulses = PulseCounter()
    print('Pulses: ' + str(Pulses))

# player = subprocess.Popen(["mpg123", "/home/rfgoat/memophon/" + str(Pulses) + ".mp3", "-q"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    player = subprocess.run(["mpg123", "/home/rfgoat/memophon/" + str(Pulses) + ".mp3", "-q"])
    # Record and save
    CurrTime = str(time.strftime("%d_%b_%Y_%H:%M:%S__"))
    filename = CurrTime + str(Pulses) + ".wav"
    print("\nfilename\n")
    Record(filename)
