import utime

class Driver:
    
    def __init__(self):
        self._tasks = {}
        self._timings = []
        self._index = 0
        self._currentTime = 0
        
    def register(self, time, task):
        if not time in self._tasks:
            self._tasks[time] = []
        self._tasks[time].append(task)

    def start(self):
        if not bool(self._tasks):
            raise Exception("Cannot start driver if it has no tasks registered")
        
        self._timings = list(self._tasks.keys())
        self._timings.sort()
        
        
        # Some kind of output is required for VS Code/pico-w-go to connect and control the execution
        print('Driver starting...')
        while True:
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

instance = Driver()
