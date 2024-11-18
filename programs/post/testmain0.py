from rdkgen0 import *


#~ Setup
def setup():
    robot.init()
    robot.set_collision_val(1)

    plc.init()


#~ Main Program
def main():
    Laser_CALE()




#~ Main Thread
if __name__ == "__main__":
    setup()
    main()

    Laser(0)
    plc.close()



    
