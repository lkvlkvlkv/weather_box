from machine import *
from pico_i2c_lcd import *
from utime import *
from mneopixel import *
import math

# Check if a year is a leap year
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Get the number of days in a month
def days_in_month(year, month):
    if month == 2:
        return 29 if is_leap(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

# Get the next six hour
def get_next_six_hour():
    now = localtime()
    year, month, day, hour = now[0], now[1], now[2], now[3]
    next_six_hour = ((hour // 6) + 1) * 6
    if next_six_hour == 24:
        next_six_hour = 0
        day += 1
        if day > days_in_month(year, month):
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
    next_time = (year, month, day, next_six_hour, 0, 0)
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(*next_time)

# Replace the special characters in the url
def urlencode(s):
    s = s.replace(':', '%3A')
    s = s.replace(' ', '%20')
    s = s.replace('/', '%2F')
    s = s.replace('臺', '%E8%87%BA')
    s = s.replace('北', '%E5%8C%97')
    s = s.replace('市', '%E5%B8%82')
    return s

# Score the weather
def score_weather(weather):
    scores = []
    if '雷' in weather:
        scores.append(180)
    if '雨' in weather:
        scores.append(120)
    if '陰' in weather:
        scores.append(60)
    if '晴' in weather:
        scores.append(0)
    
    if len(scores) == 1:
        return scores[0]
    return sum(scores[:2]) / 2

# Leveling the probability of precipitation
def num_of_pix(pop):
    return max(1, int(math.ceil(float(pop) / 12.5)))

# Display some information on the LCD
def display_LCD(info):
    # 查詢硬體位置
    i2c = I2C(0, sda=Pin(16), scl=Pin(17))
    # print(i2c.scan())

    # 硬體位置
    I2C_ADDR     = 39
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
     
    i2c = I2C(0, sda=Pin(16), scl=Pin(17))
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

    # https://maxpromer.github.io/LCD-Character-Creator/

    # Custom character 0
    lcd.custom_char(0, [
        0b00111,
        0b01000,
        0b10001,
        0b10010,
        0b10010,
        0b10001,
        0b01000,
        0b00111
    ])
    # Custom character 1
    lcd.custom_char(1, [
        0b11100,
        0b00010,
        0b11001,
        0b00001,
        0b00001,
        0b11001,
        0b00010,
        0b11100
    ])
    # Custom character 2
    lcd.custom_char(2, [
        0b00100,
        0b01010,
        0b00100,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000
    ])
    
    copyRight = chr(0) + chr(1) + " 2023 Copyright lkvlkvlkv. All rights reserved. "
    
    # Display the information and copy right
    while True:
        lcd.putstr(info[:16])
        lcd.putstr(copyRight[:16])
        # Circulate the information and copy right
        info = info[1:] + info[0]
        copyRight = copyRight[1:] + copyRight[0]
        sleep(0.3)

# Display the LED
def display_LED(numpix):
    pin = 20
    state_machine = 0
    
    led_arr = [
        (255, 0, 0),   # red
        (255, 165, 0), # orange
        (255, 150, 0), # yellow
        (0, 255, 0),   # green
        (0, 0, 255),   # blue
        (75, 0, 130),  # indigo
        (138, 43, 226),# violet
        (255, 255, 255)# white
    ]
    
    neo = Neopixel(8, state_machine, pin, 'GRB')
    for index, color in enumerate(led_arr):
        neo.set_pixel(index, color)
    neo.show()
    sleep(1)
    neo.clear()
    neo.show()
    
    neo = Neopixel(numpix, state_machine, pin, 'GRB')

    neo.brightness(16)
    
    # only show numpix of LEDs
    while True:
        for i in range(16):
            colors = (led_arr[(i) % 8], led_arr[(i+1) % 8], led_arr[(i+2) % 8], led_arr[(i+3) %
                    8], led_arr[(i+4) % 8], led_arr[(i+5) % 8], led_arr[(i+6) % 8], led_arr[(i+7) % 8])[:numpix]

            for index, color in enumerate(colors):
                neo.set_pixel(index, color)
            neo.show()
            sleep(0.3)
        for i in range(8):
            colors = (led_arr[i],) * numpix

            for index, color in enumerate(colors):
                neo.set_pixel(index, color)
            neo.show()
            sleep(0.3)
        for i in range(16):
            colors = (led_arr[(i) % 8], led_arr[(i+7) % 8], led_arr[(i+6) % 8], led_arr[(i+5) %
                    8], led_arr[(i+4) % 8], led_arr[(i+3) % 8], led_arr[(i+2) % 8], led_arr[(i+1) % 8])[:numpix]

            for index, color in enumerate(colors):
                neo.set_pixel(index, color)
            neo.show()
            sleep(0.3)
        for i in range(8):
            colors = (led_arr[7 - i],) * numpix

            for index, color in enumerate(colors):
                neo.set_pixel(index, color)
            neo.show()
            sleep(0.3)
