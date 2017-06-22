from machine import Pin
import time

# Pin: P14 for Pysense board
# Pin: G17 for Extension board

button = Pin("G17", mode=Pin.IN, pull=Pin.PULL_UP)

is_pressed = False

while True:
    if button() == 0 and not is_pressed:
        print("Button pressed")
        is_pressed = True
    elif button() == 1 and is_pressed:
        print("Button released")
        is_pressed = False
    else:
        pass
