from lights.trafficlight import IntersectionBuilder
import lights.trafficlight as trafficlight

builder = IntersectionBuilder(IntersectionBuilder.TYPE.RED_REDYELLOW_GREEN_YELLOW, 1)
builder.addTrafficLight(0, 1, 2, 1)
builder.addTrafficLight(10, 11, 12, 2)
builder.addTrafficLight(18, 17, 16, 3)
builder.addTrafficLight(28, 27, 26, 4)
builder.build()

trafficlight.start()
