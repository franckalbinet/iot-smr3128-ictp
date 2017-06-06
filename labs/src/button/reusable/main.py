from machine import Pin
import time


from machine import Pin

class Button:
    def __init__(self, id):
        self.pressed = False
        self.btn = Pin(id, mode=Pin.IN, pull=Pin.PULL_UP)

    def on(self):
        self.btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING,
                          self._handler)
    def off(self):
        self.btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING,
                          None)

    def _handler(self, pin):
        value = pin.value()
        if not value and not self.pressed:
            print('Button pushed')
            self.pressed = True
        elif value and self.pressed:
            print('Button released')
            self.pressed = False
        else:
            pass

btn = Button('G17')
btn.on()
