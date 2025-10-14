import RPi.GPIO as GPIO #импортирую модуль работыс GPIO

DAC_VREF = 3.3 #максимальное напряжение, которое может выдать ЦАП(в волтах)
DAC_BITS = 8
DAC_MAX = 255 #максимальное цифровое значение
class R2R_DAC: #объявляю класс и реализую его обязательный конструктор
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits,  GPIO.OUT, initial = 0)
        
        if self.verbose: #проверяет флаг verbose, если true, выполняет вывод отладочной информации, выводит информацию об инициализации R2R DAC
            print(f"R2R DAC инициализирован на пинах:{gpio_bits}")
            print(f"Динамический диапазон:{dynamic_range}B")

    def deinit(self): #дополняю класс "деструктором"
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        if self.verbose: #выводит сообщение о деиницилизации R2R только если включен режим подобного вывода
            print("R2R DAC деинициализирован")

    def number_to_dac(self, number):
        for i in range(len(self.gpio_bits)):
            bit = (number >> i) & 1
            GPIO.output(self.gpio_bits[i], bit) #добавила в класс реализацию метода set_number(self, number)

    def voltage_to_number(self, voltage): #добавила в класс реализацию метода set_voltage(self, voltage)
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0..{self.dynamic_range} B)")
            print("Устанавливаем 0.0 B")
            return 0
        return int(voltage / self.dynamic_range * DAC_MAX)
    
    def set_voltage(self, voltage):
        number = self.voltage_to_number(voltage)
        self.number_to_dac(number)
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.3f} В (код: {number})")

if __name__ == "__main__": #реализую основной охранник(специальная конструкция, которая позволяет контролировать выполнение кода в зависимости от способа запуска файла) создаваемого модуля для работы R2R-ЦАП
    try:
        dac = R2R_DAC([22, 27, 17, 26, 25, 21, 20, 16], 3.183, True)  # правильно создается объект
        
        while True:
            try: #дополнила скрипт его рабочей частью
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
                print()  # пустая строка для читаемости

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
            except KeyboardInterrupt:
                print("\n программа завершена пользователем")
                break

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        dac.deinit()

