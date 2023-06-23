import driver

class MockDriver(driver.Driver):

    def __init__(self):
        super(MockDriver, self).__init__()
        self._hasTakenStep = False
        self._numTasksRegistered = 0

    def reset(self):
        self._tasks = {}
        self._timings = []
        self._index = 0
        self._currentTime = 0
        self._isAlive = False
        self._hasTakenStep = False
        self._numTasksRegistered = 0

    def register(self, time, task):
        super(MockDriver, self).register(time, task)
        self._numTasksRegistered += 1

    def start(self):
        self._isAlive = True
        self._index = 0
        self._hasTakenStep = False
        self._organizeTasks()

    def step(self):
        if not self._isAlive:
            raise Exception('Driver is not started, it cannot be stepped')
        
        self._hasTakenStep = True
        print('Stepping...')
        for task in self._tasks[self._timings[self._index]]:
            print('Executing :', task)
            task()
        
        print('Index', self._index, 'Size', len(self._timings))
        self._index = (self._index + 1) % len(self._timings)

    def stop(self):
        self._isAlive = False

    def hasLooped(self):
        return self._hasTakenStep and self._index == 0

class TaskTupple:
    def __init__(self, time, task):
        self._time = time
        self._task = task

mockDriver = MockDriver()
driver.instance = mockDriver

def assertNumTasksRegistered(expectedNumTasks):
    assert expectedNumTasks == mockDriver._numTasksRegistered, 'Incorrect number of registered tasks, expected ' + str(expectedNumTasks) +  ' but was ' + str(mockDriver._numTasksRegistered)

def assertTasksRegistered(expectedTasks):
    assertNumTasksRegistered(len(expectedTasks))

    expectedDict = {}
    for t in expectedTasks:
        if not t._time in expectedDict:
            expectedDict[t._time] = []
        expectedDict[t._time].append(t._task)

    for t in expectedDict.keys():
        exp = expectedDict[t]
        assert t in mockDriver._tasks, 'No tasks registered at time ' + str(t) + '. Expected ' + str(len(exp)) + ' task(s)'
        actual = mockDriver._tasks[t]

        assert len(exp) == len(actual), 'Different number of tasks registered for time ' + str(t) + '. Expected ' + str(len(exp)) + ' but was ' + str(len(actual))
        for i in range(len(exp)):
            assert exp[i] == actual[i], 'Different task at time ' + str(t) + ' position ' + str(i) + '. Expected ' + str(exp[i]) + ' but was ' + str(actual[i])
