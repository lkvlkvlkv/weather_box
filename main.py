import mwifi
import mweather
import urequests
import _thread
from mservo import *
from utils import *

SSID = ''
PASSWORD = ''
AUTHORIZATION = ''
CITY = urlencode("臺北市")
# TIME = urlencode(get_next_six_hour())

mwifi.Wifi(SSID, PASSWORD)

# URL = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={AUTHORIZATION}&format=JSON&locationName={CITY}&sort=time&startTime={TIME}"
URL = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={AUTHORIZATION}&format=JSON&locationName={CITY}&sort=time"

w = mweather.Weather(URL)

weather = w.wx
degree = score_weather(weather)
print(degree)

servo = Servo(0, True)
servo.rotate(degree)

pop = w.pop
numpix = num_of_pix(pop)
print(numpix)

info = w.info()
print(info)

_thread.start_new_thread(display_LCD, (info, ))
display_LED(numpix)