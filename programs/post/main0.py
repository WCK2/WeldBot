from rdkgen0 import *


#~ main
def main():
    mem.log = 'idle'
    mem.status = 'idle'
    while True:
        time.sleep(1)
        print('waiting for start button press')
        while True:
            if mem.start:
                print('start button pressed!')
                p = mem.program
                break
            else:
                CheckRobotFlags(wait = False)
                time.sleep(0.75)
        
        CheckRobotFlags(wait=True)

        # start of run
        mem.log = f'running program: {p}'
        mem.status = f'running:{p}'
        if robot.is_in_drag_mode()[1]:
            robot.drag_mode_enable(False)
        
        # run prog
        ProgSel(p)

        # end of run
        robot.waitmove()
        mem.log = 'program finished'
        mem.status = 'idle'
        time.sleep(1)


#~ setup
def setup():
    # start server
    server.run_server()
    mem.status = 'booting'
    print('> server running')

    robot.init()
    robot.servo_move_enable(False)
    robot.set_collision_val(1)
    # CheckForceSensor()
    print('> jaka initialize success')

    plc.init()
    print('> plc initialize success')

#~ crash
def crash():
    mem.log = 'crash'
    mem.status = 'crash'

    try:
        if robot.connected:
            # robot.set_DO(0,0)
            robot.disable()
        elif plc.connected:
            plc.write_coil(addr.laser_trigger, False)

    except:
        print(exc_info())
        print(' ^^ crash crashed :o')



#~ main thread
if __name__ == "__main__":
    while True:
        try:
            print('PROGRAM START')
            setup()
            main()
            print('should never reach here')
        except KeyboardInterrupt:
            exc_info()
            break
        except Exception:
            exc_info()
            crash()

            try:
                print("\033[1;31;43m !! Restarting in 10 ", end="")
                for i in range(10):
                    time.sleep(1)
                    print(end=". ")
                print("\033[0;0m")
            except KeyboardInterrupt:
                print("kb interrupt \033[0;0m")
                sys.exit()
        except:
            exc_info()
            print("rip prog")
            crash()




