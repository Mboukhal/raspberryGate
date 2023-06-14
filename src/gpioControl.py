#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import os

RELAY_1 = 14
RELAY_2 = 15

def openGate( gate ):
    
    relay = RELAY_1

    if gate == "out":
        relay = RELAY_2

    GPIO.output( RELAY_1 + gate, GPIO.HIGH )
    sleep( 0.8 )
    GPIO.output( RELAY_1 + gate, GPIO.LOW )


def initGpio():

    try:
        GPIO.setwarnings(False)

        try:
            GPIO.cleanup()
        except:
            pass

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( RELAY_1, GPIO.OUT )
        GPIO.output( RELAY_1, GPIO.LOW )
        GPIO.setup( RELAY_2, GPIO.OUT )
        GPIO.output( RELAY_2, GPIO.LOW )
    except:
        pass

    GPIO.setmode( GPIO.BCM )
    GPIO.setup( RELAY_1, GPIO.OUT )
    GPIO.output( RELAY_1, GPIO.LOW )
    GPIO.setup( RELAY_2, GPIO.OUT )
    GPIO.output( RELAY_2, GPIO.LOW )