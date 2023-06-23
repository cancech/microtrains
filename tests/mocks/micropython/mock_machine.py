from unittest.mock import MagicMock
import mocks.micropython.mock_utime
import sys

"""
Mocking of the micropython machine module
"""

class Pin():

    IN = 'IN'
    OUT = 'OUT'
    
    def __init__(self, pinNum, pinType):
        self._pinNum = pinNum
        self._pinType = pinType
        self._state = False

    def low(self):
        self._state = False

    def high(self):
        self._state = True

    def assertPin(self, expectedNum, expectedType):
        assert expectedNum == self._pinNum, 'Incorrect pin number, expected ' + str(expectedNum) +  ' but was ' + str(self._pinNum)
        assert expectedType == self._pinType, 'Incorrect pin type, expected ' + str(expectedType) +  ' but was ' + str(self._pinType)

    def assertState(self, expectedState):
        assert expectedState == self._state, 'Incorrect state, expected ' + str(expectedState) + ' but was ' + str(self._state)


