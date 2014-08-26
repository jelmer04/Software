from max31855 import MAX31855, MAX31855Error
from PID import PID
import RPi.GPIO as GPIO
from time import sleep

# Heater
out_pin = 17
freq = 1000
GPIO.setmode(GPIO.BCM)
GPIO.setup(out_pin, GPIO.OUT)
heater = GPIO.PWM(out_pin, freq)
heater.start(0)

# Thermocouple
cs_pin = 2
clk_pin = 3
data_pin = 4
unit = "c"

thermocouple = MAX31855(cs_pin, clk_pin, data_pin, unit)

# PID
kp = 1
ki = 0
kd = 0
sampletime = 0.1

pidcontroller = PID
pidcontroller.tune(pidcontroller, kp, ki, kd)
pidcontroller.set_sample_time(pidcontroller, sampletime)
pidcontroller.set_limits(pidcontroller, 100, 0)

while True:
    temperature = thermocouple.get()

    output = pidcontroller.compute(pidcontroller, temperature)

    heater.ChangeDutyCycle(output)

    print("Temperature:\t", temperature, "\tOutput:", output)

    sleep(sampletime)
