#!/bin/env python

from hooks.core import *

container = ProcessContainer()
a = Hook('sample.sh','bash')
b = Hook('py-sample.py','python')
container.add(a)
container.add(b)
container.run() 
