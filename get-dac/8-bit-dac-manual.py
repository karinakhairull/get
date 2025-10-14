import RPi.GPIO as GPIO #импортирую модуль работыс GPIO
import time

GPIO.setmode(GPIO.BCM) #создаю перемнную со списком GPI-пинов, подключенных ко входам R2R ЦАП в блоке 8-bit DAc
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(dac_bits, GPIO.OUT) #настраиваю пины, как выходы
dynamic_range = 3.137 #создаю переменную с динамическим диапазоном R2R ЦАП(3.3В)

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"напряжение выходит за динамический диапазон цап (0.00 - {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 B")
        return 0

    return int(voltage / dynamic_range * 255)
    
def number_to_dac(number):
    print(number)
    s = bin(number)[2:].zfill(8)
    s = [int(i) for i in s]
    GPIO.output(dac_bits, s)
            
try: #дополняю скрипт его рабочей частью
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольах:"))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()