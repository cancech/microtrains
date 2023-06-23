import unittest
import mocks.mock_micropython
import mocks.micropython.mock_machine as mm
import common.driver
import mocks.common.mock_driver as md

import lights.trafficlight as tl

class TestTrafficLight(unittest.TestCase):

    def setUp(self):
        self._light = tl.TrafficLight(1, 2, 3, 4)

    def testSpecifiedValues(self):
        self._light._lights[0].assertPin(1, mm.Pin.OUT)
        self._light._lights[1].assertPin(2, mm.Pin.OUT)
        self._light._lights[2].assertPin(3, mm.Pin.OUT)
        self.assertEqual(4, self._light._greenTime)

    def testRedLed(self):
        self._light._lights[0].assertState(False)
        self._light.onRed()
        self._light._lights[0].assertState(True)
        self._light.offRed()
        self._light._lights[0].assertState(False)

    def testYellowLed(self):
        self._light._lights[1].assertState(False)
        self._light.onYellow()
        self._light._lights[1].assertState(True)
        self._light.offYellow()
        self._light._lights[1].assertState(False)
        
    def testGreenLed(self):
        self._light._lights[2].assertState(False)
        self._light.onGreen()
        self._light._lights[2].assertState(True)
        self._light.offGreen()
        self._light._lights[2].assertState(False)

class TestLightAction(unittest.TestCase):

    def testVerifyRedColor(self):
        act = tl.LightAction(tl.TrafficLight.COLOUR.RED, True, 123)
        self.assertEqual(tl.TrafficLight.COLOUR.RED, act._colour)
        self.assertEqual(True, act._isOn)
        self.assertEqual(123, act._time)

    def testVerifyYellowColor(self):
        act = tl.LightAction(tl.TrafficLight.COLOUR.YELLOW, False, 879)
        self.assertEqual(tl.TrafficLight.COLOUR.YELLOW, act._colour)
        self.assertEqual(False, act._isOn)
        self.assertEqual(879, act._time)

    def testVerifyGreenColor(self):
        act = tl.LightAction(tl.TrafficLight.COLOUR.GREEN, True, -8654)
        self.assertEqual(tl.TrafficLight.COLOUR.GREEN, act._colour)
        self.assertEqual(True, act._isOn)
        self.assertEqual(-8654, act._time)

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        self._light = tl.TrafficLight(1, 2, 3, 4)
    
    def tearDown(self):
        md.mockDriver.reset()

    def testCallForTrafficLightReferences(self):
        self.assertEqual(self._light.onRed, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.RED, True))
        self.assertEqual(self._light.offRed, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.RED, False))
        self.assertEqual(self._light.onGreen, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.GREEN, True))
        self.assertEqual(self._light.offGreen, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.GREEN, False))
        self.assertEqual(self._light.onYellow, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.YELLOW, True))
        self.assertEqual(self._light.offYellow, tl._callForTrafficLight(self._light, tl.TrafficLight.COLOUR.YELLOW, False))

    def testRegisterPattern(self):
        actions = [tl.LightAction(tl.TrafficLight.COLOUR.RED, False, 123),
                   tl.LightAction(tl.TrafficLight.COLOUR.YELLOW, False, 321),
                   tl.LightAction(tl.TrafficLight.COLOUR.GREEN, False, 123)]
        tl._registerPattern(self._light, actions)
        md.assertTasksRegistered(lightActionToTupple(self._light, actions))

    def testLimitToPeriod(self):
        # Invalid values raise error
        self.assertRaises(ValueError, tl._limitToPeriod, -1, 1)
        self.assertRaises(ValueError, tl._limitToPeriod, 0, 0)
        self.assertRaises(ValueError, tl._limitToPeriod, 1, -1)
        self.assertEqual(0, tl._limitToPeriod(0, 5))
        self.assertEqual(1, tl._limitToPeriod(1, 5))
        self.assertEqual(2, tl._limitToPeriod(2, 5))
        self.assertEqual(3, tl._limitToPeriod(3, 5))
        self.assertEqual(4, tl._limitToPeriod(4, 5))
        self.assertEqual(5, tl._limitToPeriod(5, 5))
        self.assertEqual(1, tl._limitToPeriod(6, 5))
        self.assertEqual(2, tl._limitToPeriod(7, 5))
        self.assertEqual(3, tl._limitToPeriod(8, 5))

class IntersectionBuilderTest(unittest.TestCase):
    
    def tearDown(self):
        md.mockDriver.reset()

    def testRedGreenYellowIntersection(self):
        builder = tl.IntersectionBuilder(tl.IntersectionBuilder.TYPE.RED_GREEN_YELLOW)
        builder.addTrafficLight(1, 2, 3)
        builder.addTrafficLight(4, 5, 6)
        builder.build()
        md.assertNumTasksRegistered(12)
        traffic1 = builder._trafficLight[0]
        traffic2 = builder._trafficLight[1]

        # At start 1 = green, 2 = red
        tl.start()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick0: 1 - green, 2 = red
        md.mockDriver.step()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick1: 1 = yellow, 2 = red
        md.mockDriver.step()
        assertLightState(traffic1, False, True, False)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick2: 1 = red, 2 = green
        md.mockDriver.step()
        assertLightState(traffic1, True, False, False)
        assertLightState(traffic2, False, False, True)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick3: 1 = red, 2 = yellow
        md.mockDriver.step()
        assertLightState(traffic1, True, False, False)
        assertLightState(traffic2, False, True, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick4: 1 = none, 2 = red
        md.mockDriver.step()
        assertLightState(traffic1, False, False, False)
        assertLightState(traffic2, True, False, False)
        self.assertTrue(md.mockDriver.hasLooped())

        # Tick5: 1 = green, 2 = red
        # This is when it returns to the start and turn on green again
        # Previous ticks is just half the transition
        md.mockDriver.step()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

    def testRedRedYellowGreenYellowIntersection(self):
        builder = tl.IntersectionBuilder(tl.IntersectionBuilder.TYPE.RED_REDYELLOW_GREEN_YELLOW, 1)
        builder.addTrafficLight(1, 2, 3, 1)
        builder.addTrafficLight(4, 5, 6, 2)
        builder.build()
        md.assertNumTasksRegistered(16)
        traffic1 = builder._trafficLight[0]
        traffic2 = builder._trafficLight[1]

        # At start 1 = green, 2 = red
        tl.start()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick0: 1 - green, 2 = red
        md.mockDriver.step()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick1: 1 = yellow, 2 = red+yellow
        md.mockDriver.step()
        assertLightState(traffic1, False, True, False)
        assertLightState(traffic2, True, True, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick2: 1 = red, 2 = green
        md.mockDriver.step()
        assertLightState(traffic1, True, False, False)
        assertLightState(traffic2, False, False, True)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick3: 1 = red+yellow, 2 = yellow
        md.mockDriver.step()
        assertLightState(traffic1, True, True, False)
        assertLightState(traffic2, False, True, False)
        self.assertFalse(md.mockDriver.hasLooped())

        # Tick4: 1 = none, 2 = red
        md.mockDriver.step()
        assertLightState(traffic1, False, False, False)
        assertLightState(traffic2, True, False, False)
        self.assertTrue(md.mockDriver.hasLooped())

        # Tick5: 1 = green, 2 = red
        # This is when it returns to the start and turn on green again
        # Previous ticks is just half the transition
        md.mockDriver.step()
        assertLightState(traffic1, False, False, True)
        assertLightState(traffic2, True, False, False)
        self.assertFalse(md.mockDriver.hasLooped())

def lightActionToTupple(light, lightActions):
    converted = []
    for act in lightActions:
        converted.append(md.TaskTupple(act._time, tl._callForTrafficLight(light, act._colour, act._isOn)))
    return converted

def assertLightState(trafficLight, redState, yellowState, greenState):
    trafficLight._lights[0].assertState(redState)
    trafficLight._lights[1].assertState(yellowState)
    trafficLight._lights[2].assertState(greenState)

if __name__ == '__main__':
    unittest.main()
