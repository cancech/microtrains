import unittest
import mocks.mock_micropython
import mocks.micropython.mock_utime as mu
import src.driver as driver

class TestDriver(unittest.TestCase):

    def setUp(self):
        self.testDriver = driver.Driver()

    """
    When trying to start the driver without any tasks registered, an exception is raised
    """
    def testStartNothingRegistered(self):
        self.assertRaises(Exception, self.testDriver.start)

    """
    Ensure that the registered tasks are executed, but only in as far as the driver is allowed to execute
    """
    def testRunDriverSingleIteration(self):
        # Create some tasks
        action1 = TestTask()
        action2 = TestTask()
        action3 = TestTask()
        action4 = TestTask()
        action5 = TestTask()
        action6 = TestTask()
        action7 = TestTask()
        action8 = TestTask()

        # Register the tasks, at time 1235 the driver will be stopped
        self.testDriver.register(1234, action3.call)
        self.testDriver.register(1, action6.call)
        self.testDriver.register(5, action2.call)
        self.testDriver.register(1235, self.testDriver.stop)
        self.testDriver.register(1, action1.call)
        self.testDriver.register(1235, action4.call)
        self.testDriver.register(1236, action5.call)
        self.testDriver.register(1, action7.call)
        self.testDriver.register(1, action8.call)

        # Sanity check - nothing will have been called yet
        self.assertEqual(0, action1.getTimesCalled())
        self.assertEqual(0, action2.getTimesCalled())
        self.assertEqual(0, action3.getTimesCalled())
        self.assertEqual(0, action4.getTimesCalled())
        self.assertEqual(0, action5.getTimesCalled())
        self.assertEqual(0, action6.getTimesCalled())
        self.assertEqual(0, action7.getTimesCalled())
        self.assertEqual(0, action8.getTimesCalled())

        self.testDriver.start()
        mu.assertWaitCalled(1, 4, 1229, 1)

        # After the driver finished running, everything prior to the stop should have been called exactly once
        self.assertEqual(1, action1.getTimesCalled())
        self.assertEqual(1, action2.getTimesCalled())
        self.assertEqual(1, action3.getTimesCalled())
        self.assertEqual(1, action4.getTimesCalled())
        self.assertEqual(0, action5.getTimesCalled())
        self.assertEqual(1, action6.getTimesCalled())
        self.assertEqual(1, action7.getTimesCalled())
        self.assertEqual(1, action8.getTimesCalled())

    """
    When allowed to loop multiple times, ensure that the tasks are all triggered that number of times
    """
    def testDriverMultipleLoops(self):
        action1 = TestTask()
        action2 = StopDriverAfterLoops(self.testDriver, 3)
        self.testDriver.register(1,  action1.call)
        self.testDriver.register(2, action2.call)

        self.assertEqual(0, action1.getTimesCalled())
        self.assertEqual(0, action2.getTimesCalled())
        self.testDriver.start()
        mu.assertWaitCalled(1, 1, 1, 1, 1, 1)
        self.assertEqual(3, action1.getTimesCalled())
        self.assertEqual(3, action2.getTimesCalled())

# Helper for tracking how many times a task is called
class TestTask():
    def __init__(self):
        self._timesCalled = 0

    def call(self):
        self._timesCalled += 1

    def getTimesCalled(self):
        return self._timesCalled

# Helper which stops the driver after being called the appropriate number of times
class StopDriverAfterLoops():
    def __init__(self, driver, loopLimit):
        self._driver = driver
        self._timesCalled = 0
        self._loopLimit = loopLimit

    def call(self):
        self._timesCalled += 1
        if (self._timesCalled >= self._loopLimit):
            self._driver.stop()

    def getTimesCalled(self):
        return self._timesCalled

if __name__ == '__main__':
    unittest.main()