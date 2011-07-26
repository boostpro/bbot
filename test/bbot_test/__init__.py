# Get bbot into the path
import inspect, sys, os
from os.path import dirname, join
sys.path.append(
    dirname( dirname( dirname( dirname(
        os.path.join(os.getcwd(), inspect.stack()[0][1]))))))
