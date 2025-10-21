import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        s = bin(number)[2:].zfill(8)
        s = [int(i) for i in s]
        GPIO.output(self.bits_gpio, s)

    def sequential_couting_adc(self):
        for i in range (256):
            R2R_ADC.number_to_dac(self, i)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                return(i)
            if i == 255:
                return(i)

    def get_sc_voltage(self):
        number = R2R_ADC.sequential_couting_adc(self)
        voltage = number/ 255 * self.dynamic_range
        print(number, f"{voltage:.3f}")

if __name__ =="__main__":
    try:
        adc = R2R_ADC(3.29)
        while True:
            voltage = adc.get_sc_voltage()

    finally:
        adc.deinit()