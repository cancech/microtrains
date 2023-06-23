from unittest.mock import call, MagicMock
import sys

"""
Mocking of the micropython utime module
"""
mockutime = MagicMock()
sys.modules['utime'] = mockutime

def assertWaitCalled(*expectedSleepTimes):
    calls = map(lambda i: call(i), expectedSleepTimes)
    mockutime.sleep.assert_has_calls(calls)