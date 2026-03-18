from rdkgen0 import *
import time


#~ Setup
def setup():
    # server.run_server()

    robot.init()
    robot.set_collision_val(2)

    plc.init()


#~ Main Program
def main():
    # Laser_MS3_10in()
    # Laser_Vault_Chassis_x4()
    # TEST_Laser_Vault_Chassis_x4()

    # TEST_Laser_101_108_x100()
    # Laser_101_108_x10()
    # Laser_101_108_x100()

    # Laser_871_025B_x1()
    # Laser_871_025B_x2()

    # TEST_Laser_767_2205_B_x7()
    # Laser_767_2205_B_x7()

    # TEST_Laser_1881_1015_x1()
    # Laser_1881_1015_x1()
    # Laser_1881_1015_x2()

    # TEST_Laser_767_119_FixtureA()
    # TEST_Laser_767_119_FixtureB()
    # Laser_767_119_FixtureA()
    Laser_767_119_FixtureB()



#~ Main Thread
if __name__ == "__main__":
    setup()
    start_time = time.time()
    print(f'Start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))}')

    main()

    end_time = time.time()
    print(f'End time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))}')
    print(f'Duration: {(end_time - start_time):.2f} seconds')

    Laser(0)
    plc.close()



    
