from driver import instance as driver
from machine import Pin
import src.enum as enum

'''
Provides controls for all of the lights (LEDs) that belond to a given traffic light.
'''
class TrafficLight:   
    COLOUR = enum.create('RED', 'YELLOW', 'GREEN')

    '''
    CTOR - for a single set of lights

    * redPinNum - the number of the pin on the board through which to control the RED LED of the traffic light
    * yellowPinNum - the number of the pin on the board through which to control the YELLOW LED of the traffic light
    * greenPinNum - the number of the pin on the board through which to control the GREEN LED of the traffic light
    * greenTimeSec - the number of seconds the green light will be lit
    '''         
    def __init__(self, redPinNum, yellowPinNum, greenPinNum, greenTimeSec):
        self._lights = [Pin(redPinNum, Pin.OUT), Pin(yellowPinNum, Pin.OUT), Pin(greenPinNum, Pin.OUT)]
        self.__allOff()
        self._greenTime = greenTimeSec
        
    '''
    Turns off all LEDs
    '''
    def __allOff(self):
        for led in self._lights:
            led.low()
            
    '''
    Turns on the LED at the given index
    '''
    def __on(self, index):
        self._lights[index].high()
        
    '''
    Turns off the LED at the given index
    '''
    def __off(self, index):
        self._lights[index].low()
    
    '''
    Turns on the RED LED
    '''
    def onRed(self):
        self.__on(self.COLOUR.RED)
            
    '''
    Turns off the RED LED
    '''
    def offRed(self):
        self.__off(self.COLOUR.RED)
            
    '''
    Turns on the YELLOW LED
    '''
    def onYellow(self):
        self.__on(self.COLOUR.YELLOW)
            
    '''
    Turns off the YELLOW LED
    '''
    def offYellow(self):
        self.__off(self.COLOUR.YELLOW)
            
    '''
    Turns on the Green LED
    '''
    def onGreen(self):
        self.__on(self.COLOUR.GREEN)
            
    '''
    Turns off the RED LED
    '''
    def offGreen(self):
        self.__off(self.COLOUR.GREEN)

'''
Helper that acts as a tupple associating which colour LED turn on/off at what time.
'''
class LightAction:
    def __init__(self, colour, isOn, time):
        self._colour = colour
        self._isOn = isOn
        self._time = time

'''
Get a reference to the method which places the LED of the specified colour into the specified state

* trafficLight - whose LEDs to update
* colour - the colour of the traffic light to update
* isOn - true if the light should turn on
'''
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

'''
Register the specified LightActions with the driver

* trafficLight - on which the action is to take place
* actions - array of actions to perform (which colour, which state, at which time)
'''
def _registerPattern(trafficLight, actions):
    for act in actions:
        driver.register(act._time, _callForTrafficLight(trafficLight, act._colour, act._isOn))

'''
Limits the value to be within 0 and the period.

* value - to ensure within the period (must be greater than or equal to 0)
* period - the limit (must be greater than 0)
'''
def _limitToPeriod(value, period):
    if (value < 0):
        raise ValueError("Negative value is not allowed", value)
    if (period <= 0):
        raise ValueError("Period must be greater than 0", period)
    if (value <= period):
        return value
    
    return value % period
    
'''
Create the blink pattern for a traffic light that goes Red -> Green -> Yellow

* trafficLight - which controls the lights
* offset - time (seconds) at which point the blink pattern should start
* greenTime - time (second) that the green light is to be on for
* yellowTime - time (seconds) that the yellow light is to be one for
* redTime - time (seconds) that the rest light is to be on for
* period - time (seconds) required for the whole intersection to cycle through
'''
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

'''
Create the blink pattern for a traffic light that goes Red -> Red+Yellow -> Green -> Yellow

* trafficLight - which controls the lights
* offset - time (seconds) at which point the blink pattern should start
* greenTime - time (second) that the green light is to be on for
* yellowTime - time (seconds) that the yellow light is to be one for
* redTime - time (seconds) that the rest light is to be on for
* period - time (seconds) required for the whole intersection to cycle through
'''
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

'''
Builder which creates all of the lights and their behaviors for an intersection.
Note that the singleton driver.instance driver is employed by the IntersectionBuilder
and once everything is defined it must be started to the intersection operation
'''
class IntersectionBuilder:
    
    # The types of lights that can be employed in the intersection
    TYPE = enum.create('RED_GREEN_YELLOW', 'RED_REDYELLOW_GREEN_YELLOW')
    # Mapping of light TYPE to the creator for desired behavior
    _creators = {
        TYPE.RED_GREEN_YELLOW: _createRed_Green_Yellow,
        TYPE.RED_REDYELLOW_GREEN_YELLOW: _createRed_RedYellow_Green_Yellow
    }
    
    '''
    CTOR

    * typeOfLight - TYPE indicating the behavior of the lights in the intersection
    * yellowTimeSec - time (seconds) that the yellow light is to be on for (default 3s)
    '''
    def __init__(self, typeOfLight, yellowTimeSec = 3):
        self._trafficLight = []
        self._creator = self._creators[typeOfLight]
        self._yellowTime = yellowTimeSec
    
    '''
    Add a traffic light to the intersection

    * redPin - the number of the GPIO pin for controlling the red LED
    * yellowPin - the number of the GPIO pin for controlling the yellow LED
    * greenPin - the number of the GPIO pin for controlling the green LED
    * greenTimeSec - time (seconds) that the green light is to be one for
    '''
    def addTrafficLight(self, redPin, yellowPin, greenPin, greenTimeSec = 42):
        self._trafficLight.append(TrafficLight(redPin, yellowPin, greenPin, greenTimeSec))

    '''
    Build the traffic lights and define their behavior.
    '''
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

'''
Starts the traffic light so that they begin blinking.

Note this starts the driver.instance that is employed by the IntersectionBuilder.
If that driver is used in multiple locations, then first register all tasks and
once ready start it once.
'''
def start():
    driver.start()
