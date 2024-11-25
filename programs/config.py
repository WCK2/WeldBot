import math


#~ Speeds (linear_velocity, angular_velocity, linear_acceleration, angular_acceleration)
#? CALE
s_mig = 15, 15, 200, 5

# f_mig = 75, 25, 100, 10 # for testing (344 seconds)
f_mig = 250, 60, 125, 40 # for production (280 seconds w/ RelOffset(1) for linear_sleep welds) (293 previously)






FAST = 0
SLOW = 1
FASTAF = 2
SLOWAF = 3


#~ Other
SQRT2 = math.sqrt(2) # for right triangle w/ 45 degree angle, then both sides length = sqrt(2) would make hypotenuse length = 2
SQRT2_2 = math.sqrt(2) / 2 # for right triangle w/ 45 degree angle, then both sides length = sqrt(2)/2 would make hypotenuse length = 1



