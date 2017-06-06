from machine import Pin
import time


is_pressed = False
def handler(pin):
    global is_pressed
    value = pin.value()
    if not value and not is_pressed:
        print('Button pressed')
        is_pressed = True
    elif value and is_pressed:
        print('Button released')
        is_pressed = False
    else:
        pass

btn = Pin("G17", mode=Pin.IN, pull=Pin.PULL_UP)
btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, handler)
