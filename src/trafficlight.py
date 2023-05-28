from driver import instance as driver
from machine import Pin
import enum

class TrafficLight:   
    COLOUR = enum.create('RED', 'YELLOW', 'GREEN')
         
    def __init__(self, redPinNum, yellowPinNum, greenPinNum, greenTimeSec):
        self._lights = [Pin(redPinNum, Pin.OUT), Pin(yellowPinNum, Pin.OUT), Pin(greenPinNum, Pin.OUT)]
        self.__allOff()
        self._greenTime = greenTimeSec
        
    def __allOff(self):
        for led in self._lights:
            led.low()
            
    def __on(self, index):
        self._lights[index].high()
        
    def __off(self, index):
        self._lights[index].low()
            
    def onRed(self):
        self.__on(self.COLOUR.RED)
            
    def offRed(self):
        self.__off(self.COLOUR.RED)
            
    def onYellow(self):
        self.__on(self.COLOUR.YELLOW)
            
    def offYellow(self):
        self.__off(self.COLOUR.YELLOW)
            
    def onGreen(self):
        self.__on(self.COLOUR.GREEN)
            
    def offGreen(self):
        self.__off(self.COLOUR.GREEN)

class LightAction:
    def __init__(self, colour, isOn, time):
        self._colour = colour
        self._isOn = isOn
        self._time = time

def _callForTrafficLight(trafficLight, colour, isOn):
    if colour == trafficLight.COLOUR.RED and isOn:
        return trafficLight.onRed
    if colour == trafficLight.COLOUR.RED:
        return trafficLight.offRed
    if colour == trafficLight.COLOUR.YELLOW and isOn:
        return trafficLight.onYellow
    if colour == trafficLight.COLOUR.YELLOW:
        return trafficLight.offYellow
    if colour == trafficLight.COLOUR.GREEN and isOn:
        return trafficLight.onGreen
    if colour == trafficLight.COLOUR.GREEN:
        return trafficLight.offGreen
    
    raise ValueError("Invalid color specified", colour)

def _registerPattern(trafficLight, actions):
    for act in actions:
        driver.register(act._time, _callForTrafficLight(trafficLight, act._colour, act._isOn))

def _limitToPeriod(value, period):
    if (value <= period):
        return value
    
    return value % period
    
def _createRed_Green_Yellow(trafficLight, offset, greenTime, yellowTime, redTime, period):
    nextTime = offset
    actions = [LightAction(trafficLight.COLOUR.GREEN, True, nextTime)]
    nextTime = _limitToPeriod(nextTime + greenTime, period)
    actions.append(LightAction(trafficLight.COLOUR.GREEN, False, nextTime))
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, True, nextTime))
    nextTime = _limitToPeriod(nextTime + yellowTime, period)
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, False, nextTime))
    actions.append(LightAction(trafficLight.COLOUR.RED, True, nextTime))
    nextTime = _limitToPeriod(nextTime + redTime, period)
    actions.append(LightAction(trafficLight.COLOUR.RED, False, nextTime))
    _registerPattern(trafficLight, actions)

def _createRed_RedYellow_Green_Yellow(trafficLight, offset, greenTime, yellowTime, redTime, period):
    nextTime = offset
    actions = [LightAction(trafficLight.COLOUR.GREEN, True, nextTime)]
    nextTime = _limitToPeriod(nextTime + greenTime, period)
    actions.append(LightAction(trafficLight.COLOUR.GREEN, False, nextTime))
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, True, nextTime))
    nextTime = _limitToPeriod(nextTime + yellowTime, period)
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, False, nextTime))
    actions.append(LightAction(trafficLight.COLOUR.RED, True, nextTime))
    nextTime = _limitToPeriod(nextTime + redTime - yellowTime, period)
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, True, nextTime))
    nextTime = _limitToPeriod(nextTime + yellowTime, period)
    actions.append(LightAction(trafficLight.COLOUR.RED, False, nextTime))
    actions.append(LightAction(trafficLight.COLOUR.YELLOW, False, nextTime))
    _registerPattern(trafficLight, actions)

class IntersectionBuilder:
    
    TYPE = enum.create('RED_GREEN_YELLOW', 'RED_REDYELLOW_GREEN_YELLOW')
    _creators = {
        TYPE.RED_GREEN_YELLOW: _createRed_Green_Yellow,
        TYPE.RED_REDYELLOW_GREEN_YELLOW: _createRed_RedYellow_Green_Yellow
    }
    
    def __init__(self, typeOfLight, yellowTimeSec = 3):
        self._trafficLight = []
        self._creator = self._creators[typeOfLight]
        self._yellowTime = yellowTimeSec
        
    def addTrafficLight(self, redPin, yellowPin, greenPin, greenTimeSec = 42):
        self._trafficLight.append(TrafficLight(redPin, yellowPin, greenPin, greenTimeSec))

    def build(self):
        period = self._yellowTime * len(self._trafficLight)
        for tl in self._trafficLight:
            period += tl._greenTime
        
        offset = 0
        for i in range(len(self._trafficLight)):
            tl = self._trafficLight[i]
            if i == 0:
                tl.onGreen()
            else:
                tl.onRed()
                
            gt = tl._greenTime
            cycle = gt + self._yellowTime
            self._creator(tl, offset, gt, self._yellowTime, period - cycle, period)
            offset += cycle

def start():
    driver.start()
