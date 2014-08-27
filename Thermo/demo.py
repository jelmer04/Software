from max31855 import MAX31855, MAX31855Error
from time import sleep

delay = 0.5
cs_pin = 2
clk_pin = 3
data_pin = 4
unit = "c"

thermocouple = MAX31855(cs_pin, clk_pin, data_pin, unit)

for i in range(int(30/delay)):
    print(thermocouple.get(), "C\t", thermocouple.get_rj(), "C")
    sleep(delay)

thermocouple.cleanup()
