print("Simplest")

from machine import Pin
import time

button = Pin("P14", mode=Pin.IN, pull=Pin.PULL_UP)

is_pressed = False

# while True:
#     if button() == 0 and not is_pressed:
#         print("Button pressed")
#         is_pressed = True
#     elif button() == 1 and is_pressed:
#         print("Button reloeased")
#         is_pressed = False
#     else:
#         pass
