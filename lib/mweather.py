import urequests

class Weather:
    def __init__(self, url):
        res = urequests.get(url=url)
        self.json = res.json()
        self.parse()
        
    def parse(self, hour=0):
        city = self.json['records']['location'][0]
        self.cityname = city['locationName']
        self.startTime = city['weatherElement'][0]['time'][hour]['startTime']
        self.endTime = city['weatherElement'][0]['time'][hour]['endTime']
        self.wx = city['weatherElement'][0]['time'][hour]['parameter']['parameterName']
        self.wxvalue = city['weatherElement'][0]['time'][hour]['parameter']['parameterValue']
        self.pop = city['weatherElement'][1]['time'][hour]['parameter']['parameterName']
        self.minT = city['weatherElement'][2]['time'][hour]['parameter']['parameterName']
        self.ci = city['weatherElement'][3]['time'][hour]['parameter']['parameterName']
        self.maxT = city['weatherElement'][4]['time'][hour]['parameter']['parameterName']
        
    def repr(self):
        print(f'cityname: {self.cityname}')
        print(f'startTime: {self.startTime}')
        print(f'endTime: {self.endTime}')
        print(f'wx: {self.wx}')
        print(f'降雨機率: {self.pop}%')
        print(f'ci: {self.ci}')
        print(f'最低溫度: {self.minT}度')
        print(f'最高溫度: {self.maxT}度')
    
    def info(self):
        return f"MinT: {self.minT}" + chr(2) + f"C MaxT: {self.maxT}" + chr(2) + f"C PoP: {self.pop}% "
'''
        v = int(self.wxvalue)
        if v <= 4:
            self.wxdes = 'sun'
        else if v <= 7:
            self.wxdes = 'cloudy'
        else if v <= 22:
            self.wxdes = 'rain'
'''            
