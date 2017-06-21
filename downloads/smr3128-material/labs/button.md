**Button**: Detecting extension board button pressure

# Button

## Introduction

In this example, we will detect the pressure of the button on the pycom expansion board. Because the board does not have a keyboard (or mouse), we will use the USB connection between the board and the development PC to detect the pressure of the button.
 
The expansion board has one button as shown at the bottom in the picture below.

![lopy-expansion-board.png](http://i.imgur.com/byWzsc2.png)


## Learning outcomes

You will learn how to:
* detect the pressure of the button;
* implement Polling and Interrupts techniques
* tackle iteratively a coding "challenge" (from naive but functioning programs to implementations fostering reusability and modularity)

## Required Components

For this example you will need:

- a LoPy or WiPy module
- a microUSB cable
- a development PC

The source code is in the `src/button` directory.


> Make sure you press the button on the expansion board (highlighted by a red rectangle in image above) and not the one on the LoPy module (reset button).

## Code

### boot.py
```python
from machine import UART
import os
uart = UART(0, 115200)
os.dupterm(uart)
```

The boot.py file should always start with the above code, so we can run our python scripts over Serial or Telnet. Newer Pycom boards have this code already in the boot.py file.

### Version 1: Polling button state
Even for simple program like this one, there are numerous possible implementations. We should aim for a straighforward solution first. Premature optimization or abstraction are common pitfalls. 

The use case we want to address is the following:
1. when the button of the expansion board is pressed, display a message "Button pressed" **once** in Atom's console;
2. when released, display a message "Button released" **once**.

### main.py
```python
from machine import Pin

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
```

Let's go through the snippet code above:
```python
# we import the Pin `class` from machine Pycom modules
from machine import Pin

# then we create a `pin` object
button = Pin("G17", mode=Pin.IN, pull=Pin.PULL_UP)
```

You notice that to create a `Pin` object we need to specify three arguments:
1. pin's `id` `"G17"` - see "Expansion board user manual" in `/labs/references`;
2. pin's mode `Pin.IN` specifying that this is an input
3. pull method `Pin.PULL_UP` specifying we want a pull-up resistor. Loosely speaking, a pull-up or pull-down resistor will ensure that the pin is in either a high or low state, while also using a low amount of current and as a result prevents unknown state of the input. You can consult this blog post for further information [https://learn.sparkfun.com/tutorials/pull-up-resistors](https://learn.sparkfun.com/tutorials/pull-up-resistors).


Now that we have a button object, let's read repeatedly the state of the input. In our case when not pressed the button's value `button()` should be 1 and 0 when pressed (pull-up resistor).

```python
# flag saving previous state of the button
is_pressed = False

# we keep reading the input value 
while True:
    # when pressed and was not previously pressed
    if button() == 0 and not is_pressed:
        print("Button pressed")
        # as it has been pressed we update button's status
        is_pressed = True
    # if no pressed and was pressed previously
    elif button() == 1 and is_pressed:
        print("Button released")
        is_pressed = False
    else:
        pass
```

To read the value/state of the button, simply call `button()`.

The flag `is_pressed` allows to display messages once otherwise the message would be printed as long as you press or release the button which is not the expected use case.

This is important to note that in the implementation above, we keep reading the state of the button potentially every 100μs given that the clock rate is 160MHz. This is most probably a waste of CPU time and energy (remember that low consumption is key in IoT world) given that button pressure might not be a so much frequent event and that we might not require a response time of micro seconds. 

A first slight improvement could be to pause the execution for half a second for instance: `time.sleep_ms(500)` (insert it somewhere in the `while` loop into `main.py`).

A better alternative might be however to use in that situation Interrupts.


### Version 2: Interrupt Service Routine (ISR)
We do not want to waste time checking button's state every `100μs` (just an order of magnitude in our use case), instead we will use a technique called "**Interrupt Service Routine (ISR)**". 

ISR, is a special block of code associated with a specific interrupt condition, here button status. When this condition is met, a `handler` (a function) will be called to "do something" in response.

When an interrupt occurs, the current task is halted (preempts the current flow of control), execution context is saved, the interrupt handler "do something" (in our case simply print a message) and then previous execution is restored. For many reasons, it is highly desired that the interrupt handler executes as briefly as possible. Consider for instance that several interrupts might occur more or less simultaneously and the system need to manage priorities and concurrency.

In our case this is simple:

```python
from machine import Pin

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
```
Let's unpack the code above:

```python
from machine import Pin

is_pressed = False
````
Nothing new here, just import the Pin `class` from `machine` module and intialize our button flag.

```python
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
```
We define a function (the handler), that will we called when an interrupts occur. The body of the handler is the same as in previous implementation.

```python
# we create the pin object
btn = Pin("G17", mode=Pin.IN, pull=Pin.PULL_UP)

btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, handler)
```
In the last line, we specify that our `handler` will be called (callback) when the pin' state is either transitioning from 1 to 0 (IRQ_FALLING) or from  0 to 1 (IRQ_RISING).

## Advanced code: a bit of abstraction 
In the previous example, we had to use the `global` keyword to save a state. There is no good reason to store such state globally; this should remain the button's business. Using `global` is fine for snippet code of that size but it scales poorly and leads to non robust code (you will sooner or later loose track of which function and where you modified these global states). 

In such situation, using a `class`, we can encapsulate such state, add extra  behaviours, create various instances of the Button classes. 


```python
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
```
In this implementation, button's state is **encapsulated** in the object itself and we can create various instances (objects) of Button simply by calling `Button('button_id')`. That way we can re-use safely our code.

Let's unpack it a bit:
```python
def __init__(self, id):
    self.pressed = False
    self.btn = Pin(id, mode=Pin.IN, pull=Pin.PULL_UP)
````
`__init___` is a special method called at instance/object creation (when we call `Button('button_id')`actually). We initialize here button's state and create it.

```python
def on(self):
    self.btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING,
                          self._handler)

# To disable it just pass None (no handler)
def off(self):
    self.btn.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING,
                          None)
```

We create two methods to enable or disable our button. And finally,

```python
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
```
we define a method/handler as in previous implementation. The prefixed `_`in `_handler` is just a naming convention indicating that this method is supposed to be used internally by other class' methods and not exposed publicly as it is for `on` and `off` methods.


## Exercises
1. Toggle the LED each time the button is pressed. If the LED is OFF, turn it ON by pressing the button. If the LED is ON, turn it OFF by pressing the button.

2. Increase a counter every time the button is pressed and visualize it. 

3. Turn the red light on whenever the button is pressed for more than 3 seconds. 
