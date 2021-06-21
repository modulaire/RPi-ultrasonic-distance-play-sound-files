#!/usr/bin/python3
'''
The following code will active different sound files in loop according to
pre-defined distances received by an HC-SR04 sound sensor.
A bug in the program remains. If distance sensor reads less than 3 to 5 cm
the program freezes. Haven't taken the time yet to clean this up. Otherwise
everything works pretty well.
'''
import RPi.GPIO as GPIO
import time
from threading import Thread
from pygame import mixer

distance = 0

#GPIO setup for ultrasonic sensor HC-SR04
GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.output(PIN_TRIGGER, GPIO.LOW)

mixer.init()
mixer.music.set_volume(1.0)
#Don't know if this is entirely necessary
print("Waiting for sensor to settle")
time.sleep(1)

def sensor():
    global distance
    while True:
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        #print("Distance:",distance,"cm")

t1 = Thread(target=sensor, daemon=True)
t1.start()

sound = ['clip0.wav', 'clip1.wav', 'clip2.wav']
myFlag = [False, False, False]
spacing = [15, 25, 35]

while True:
    #do nothing
    time.sleep(.2)
    print("Distance:",distance,"cm")

    for x in range(3):
        if myFlag[x] == False and distance < (spacing[x]+5) and distance > (spacing[x]-5):
            mixer.music.stop()
            mixer.music.load(sound[x])
            mixer.music.play()
            for y in range(3):
                if y == x:
                    myFlag[y] = True
                else:
                    myFlag[y] = False


