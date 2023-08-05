import network
import time
 
class Wifi:
    def __init__(self, ssid, password=None):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
 
        while not (wlan.isconnected() or wlan.status() == network.STAT_GOT_IP):
            print("Waiting to connect:")
            time.sleep(1)
     
        print(wlan.ifconfig())
         
if __name__ == '__main__':
    Wifi('YOUR_SSID', 'YOUR_PASSWORD')