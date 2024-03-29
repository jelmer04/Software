from max31855 import MAX31855, MAX31855Error
import PID
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
cs_pin = 4
clk_pin = 3
data_pin = 2
unit = "c"

thermocouple = MAX31855(cs_pin, clk_pin, data_pin, unit)

# PID
kp = 5
ki = 0
kd = 0
sampletime = 0.5
setpoint = float(input("Enter set point: "))

pidcontroller = PID.Controller(kp=kp, ki=ki, kd=kd, sampletime=sampletime, setpoint=setpoint, min=0, max=100)

while True:
    temperature = thermocouple.get()

    output = pidcontroller.compute(temperature)

    heater.ChangeDutyCycle(output)

    print("{}\tTemp:\t{:.2f}\t\tOutput:\t{:.2f}%".format(pidcontroller.counter, temperature, output))

    sleep(sampletime/2)
