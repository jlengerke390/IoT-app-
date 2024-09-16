import machine
import time

def blinkLed(pin, blink):
    pin_mode = machine.Pin(pin, machine.Pin.OUT)
      
    for i in range (blink):
        pin_mode.value(1)
        time.sleep(0.5)
        pin_mode.value(0)
        time.sleep(0.5)
              
def onLed(pin):
     pin_mode = machine.Pin(pin, machine.Pin.OUT)
     pin_mode.value(1)
     time.sleep(5)
     pin_mode.value(0)
     