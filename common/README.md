# common

Containing the shared capabilities, this is not a module that is expected to be used by the end user. It is of course available for anything and everything that is of use to client code, but the expectation is that the other modules provide the specific capabilities desireable to an end user. The following modules are available within.

## driver

Acting as the driving force behind repetitive behavior, it allows for actions or tasks to be scheduled at intervals, which are then executed synchronously at the indicating timings when the driver is started. Due to the synchronous nature of the driver a subsequent task is started only when the executing task completes. This also include transitioning from one scheduled task to another, and more importantly the delay between one and the next. For example, taskA is scheduled to run at 1 second, and taskB at 2 seconds; due to the synchronous nature the 1 second delay between taskA and taskB doesn't start ticking until after taskA completes. If multiple tasks are register to execute at the same time, they will be executed in the same order as they were registered, sequentially one after the other. Delay for actions at subsequent timings does not start until all tasks for the current time are completed.

Example

```
driver = Driver()
driver.register(1, myTask1)
driver.register(2, myTask2)
driver.register(10, myTask3)
driver.start()
```

## enum

As micropython lacks a proper enum capability, this utility allows for "faking it". It creates a runtime C++ style Enum class (each element in the enum resolves to an integer), which includes all of the specified entries. The index of the order in which the entries are added is applies as the value of the Enum entry. Note that since the generated Enum is runtime only, many/most (all?) IDEs will struggle with Enum entries as they cannot be resolved statically to legitimate values (i.e.: VS Code pylance marks all entries as "unknown" and treats them as an error even though they're not)

Example

```
COLOUR = enum.create('RED', 'GREEN', 'BLUE', 'YELLOW')
assert COLOUR.RED == 0
assert COLOUR.GREEN == 1
assert COLOUR.BLUE == 2
assert COLOUR.YELLOW == 3
```
