import utime

"""
Single threaded driver which will continuously loop through registered tasks, executing them at the specified intervals.
The driver runs in the same thread in which it is started, and all tasks are executed within the same thread. It is assumed
that each task will be quick and not delay proceedings. Multiple tasks registered at the same time will all be executed in
the order they were registered when the appropriate time is reached.

The driver can be stopped, however given that the driver is synchronous, it must be called (whether directly or indirectly)
by a registered task, or asynchronously. Stop will not immediately stop the driver, but rather prevent from moving on to
calling the next task. Any wait in progress and the task waiting to trigger will still take place.

Example:

driver = Driver()
driver.register(1, myTask1)
driver.register(2, myTask2)
driver.register(10, myTask3)
driver.start()

In this case:
* 1 second after starting myTask1 will be called
* 1 second after myTask1 completes myTask2 will be called
* 8 seconds after myTask2 completes myTask3 will be called
* 1 second after myTask3 completes myTask1 will be called
* and so on

"""
class Driver:
    
    def __init__(self):
        self._tasks = {}
        self._timings = []
        self._index = 0
        self._currentTime = 0
        self._isAlive = False
    
    """
    Register a task with the driver
    
    * time = timestamp in seconds when the task should be called (i.e.: number of seconds from start)
    * task = the task to call at the specified time (must be callable as task())
    """
    def register(self, time, task):
        if not time in self._tasks:
            self._tasks[time] = []
        self._tasks[time].append(task)

    """
    Starts the driver. This is a synchronous blocking call that will not return until after the driver
    has been stopped. Stopping must be done either from a registered task or asynchronously.

    Example:

    driver.start()
    driver.stop() <--- will never be reached

    """
    def start(self):
        if not bool(self._tasks):
            raise Exception("Cannot start driver if it has no tasks registered")
        
        self._isAlive = True
        self._index = 0
        self._organizeTasks()
        
        # Some kind of output is required for VS Code/pico-w-go to connect and control the execution
        print('Driver starting...')
        while self._isAlive:
            # Wait to trigger the next task(s)
            nextTaskTime = self._timings[self._index]
            utime.sleep(nextTaskTime - self._currentTime)
            
            # Trigger the next task(s)
            for task in self._tasks[nextTaskTime]:
                task()
                
            # Move on to the next task(s)
            self._index += 1
            self._currentTime = nextTaskTime
            if self._index >= len(self._timings):
                self._index = 0
                self._currentTime = 0
    
    '''
    Organize registered tasks in preparation for running
    '''
    def _organizeTasks(self):
        self._timings = list(self._tasks.keys())
        self._timings.sort()

    """
    Stops the driver from progressing past the current task. Note that any task currently waiting to be triggered
    or in the process of being called will not be stopped, however the driver will stop once that task has completed.
    Does not interrupt any wait or task currently in progress
    """
    def stop(self):
        self._isAlive = False

"""
Singleton style instance that is avaiable for use as a shared driver among different users, so as to allow different
task creators to easily obtain the same driver and all tasks to be handled within the same thread
"""
instance = Driver()
