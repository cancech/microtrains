# lights

This package contains logic and capabilites that allow for controlling LEDs via GPIO ports, as well as higher level capabilities for using these lights in a particular manner to achieve a desired effect.

## Traffic Lights

Traffic lights are handles at the intersection level under the following assumptions:

* There can be any number of streets intersecting at a given intersection
* Traffic lights alternate who has the right to enter the intersection sequentially (in the order aded)
* Traffic lights for a "single street" are handled as a single entry (i.e.: one GPIO pin is turned on for each traffic light (state) and if multiple traffic lights are employed for a single streen, multiple LEDs should be fed by the single GPIO pin)
* For simplicity, the duration of the yellow light is the same across the entire intersection
* Additional lights (such as for a bike lane) can be included by wiring them to the same GPIO pins (i.e.: if bike lane has only red/green lights, then these can be wired red+yellow to bike red, and green to bike green)

What this means: for a normal cross intersection, two entries are required (one for each of the two streets), with the lights for each direction wired to the same GPIO pins. For a T intersection, the same applies except that the street terminating in the T would only require a single set of LEDs.

Two types of intersection light behaviors are supported:

* North American style Red -> Green -> Yellow -> Red (via IntersectionBuilder.TYPE.RED_GREEN_YELLOW)
* European style Red -> Red+Yellow -> Green -> Yellow (via IntersectionBuilder.TYPE.RED_REDYELLOW_GREEN_YELLOW)

The duration of the yellow and green lights can be specified by the client code (yellow at the IntersectionBuilder, green when adding a light) but they have sane defaults applied (yellow = 3 seconds, green = 45 seconds). The duration of the red light is determined based on the number of traffic lights added, and the durations applied to the green and yellow lights.

Example

```
from lights.trafficlight import IntersectionBuilder
import lights.trafficlight as trafficlight

builder = IntersectionBuilder(IntersectionBuilder.TYPE.RED_GREEN_YELLOW)
builder.addTrafficLight(0, 1, 2)
builder.addTrafficLight(10, 11, 12)
builder.build()

trafficlight.start()
```
