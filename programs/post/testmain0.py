from rdkgen0 import *
import time


#~ Setup
def setup():
    server.run_server()

    robot.init()
    robot.set_collision_val(1)

    plc.init()


#~ Main Program
def main():
    Laser_CALE()




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



    
