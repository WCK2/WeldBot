import math


#~ Speeds (linear_velocity, angular_velocity, linear_acceleration, angular_acceleration)
#? CALE
s_mig = 15, 15, 200, 5 #! production

# f_mig = 75, 25, 100, 10 #! testing
# f_mig = 250, 60, 125, 40 #! production
f_mig = 300, 80, 125, 60 #! production
"""
Notes:
Laser MS3 10in:
    - 215 seconds on testing speed (75, 25, 100, 10)
    - 168-170 seconds on production speed (250, 60, 125, 40)
        - Time between start and stops is pretty long. More acceleration could help smooth it out
"""





FAST = 0
SLOW = 1
FASTAF = 2
SLOWAF = 3


#~ Other
SQRT2 = math.sqrt(2) # for right triangle w/ 45 degree angle, then both sides length = sqrt(2) would make hypotenuse length = 2
SQRT2_2 = math.sqrt(2) / 2 # for right triangle w/ 45 degree angle, then both sides length = sqrt(2)/2 would make hypotenuse length = 1



