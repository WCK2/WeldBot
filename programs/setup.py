from rdk.nos.willrdk import *
from config import *

ROBOT = "Robot0"
MAKE = True

if ROBOT == "Robot0":     robot = rdk.Item("jaka12_0")
elif ROBOT == "Robot1":   robot = rdk.Item("jaka7_1")
elif ROBOT == "Robot2":   robot = rdk.Item("jaka7_2")
else:
    print(" >> ROBOT not selected!!")
    raise Exception
print(" >> Robot Item: ", robot.Name())

robot.setSlowSpeeds(*s_mig)
robot.setFastSpeeds(*f_mig)

# tool = rdk.Item("tool")
# frame = rdk.Item("frame_station")

rdk.Command('Trace', 'Off')
rdk.Command('Trace', 'Reset')
