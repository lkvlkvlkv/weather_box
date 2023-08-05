from machine import *
from utime import *
 
class Servo:
    def __init__(self, pin, reset=False):
        self.servo = PWM(Pin(pin))
        self.servo.freq(50)
        if reset:
            self.rotate(0)
         
    def rotate(self, degree, delay=0.4):
        self.degree = 180 - degree
        dc = (0.12 - 0.025) / 180 * self.degree + 0.025
        self.servo.duty_u16(int(65535 * dc))
        sleep(delay)
         
    def close(self):
        self.servo.deinit()

if __name__ == '__main__':
    servo = Servo(0, True)
    servo.rotate(0)
    sleep(3)
    servo.rotate(60)
    sleep(3)
    servo.rotate(120)
    sleep(3)
    servo.rotate(180)
    sleep(3)
    servo.close()