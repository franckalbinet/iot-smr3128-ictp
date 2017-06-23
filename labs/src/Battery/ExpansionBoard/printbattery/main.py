import pycom
import micropython
import machine
import time


while True:
    # https://forum.pycom.io/topic/226/lopy-adcs
    adc = machine.ADC()
    apin = adc.channel(pin='P16')
    value = apin.value()
    print(str(value))
    time.sleep_ms(5000)
