# Copied from https://stackoverflow.com/a/1695250

def create(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
