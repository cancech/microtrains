import sys
sys.path.append('src')

import mocks.micropython.mock_utime

import mocks.micropython.mock_machine
sys.modules['machine'] = sys.modules['mocks.micropython.mock_machine']