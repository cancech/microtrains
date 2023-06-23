# Copied from https://stackoverflow.com/a/1695250

"""
Creates a C++ Enum class with the specified elements as values. The first has a value of 0, incrementing for each subsequent
value. In otherwords the name becomes the name of the Enum value and it's zero-based position the value.

Example:

myEnum = create('A', 'B', 'C')
myEnum.A == 0
myEnum.B == 1
myEnum.C == 2

Equivalent to C++

enum myEnum { A, B, C };
"""
def create(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
