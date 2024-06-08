#!/usr/bin/python3
import RPi.GPIO as GPIO
import os
import subprocess
import time
import signal

basepath = "/home/rfgoat/MemophonOnPi/"
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
    proc_args = ['arecord', '-D', 'plughw:2,0', '-c1', '-r', '44100', '-f',
                 'S32_LE', '-t', 'wav', '-V', 'mono', '-v', str(filename)]
    rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
    print("startRecordingArecord()> rec_proc pid= " + str(rec_proc.pid))
    print("startRecordingArecord()> recording started")

    # time.sleep(20)
    GPIO.wait_for_edge(18, GPIO.FALLING)
    print('aufgelegt\n')
    time.sleep(0.5)  # bounce verhindern

    os.killpg(rec_proc.pid, signal.SIGTERM)
    rec_proc.terminate()
    rec_proc = None
    print("stopRecordingArecord()> Recording stopped")


# *****************START***************************

while 1:
    # wait for phone to be lifted
    GPIO.wait_for_edge(18, GPIO.RISING)
    print('abgenommen\n')
    time.sleep(0.1)  # wait 100 ms to give CPU chance to do other things

    Pulses = PulseCounter()
    print('Pulses: ' + str(Pulses))

    player = subprocess.run(["mpg123", basepath + str(Pulses) + ".mp3", "-q"])
    playBeep = subprocess.run(["mpg123", basepath + "beep.mp3", "-q"])
    # Record and save
    CurrTime = str(time.strftime("%d_%b_%Y_%H:%M:%S__"))
    filename = basepath + "records/" + CurrTime + str(Pulses) + ".wav"
    print("\nfilename\n")
    Record(filename)



