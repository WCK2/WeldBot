from parts import *
from nos.exception import *

#=================================================
# Generic Main
#=================================================
class GenericMain:
    progs=[]
    progsel_gen=True
    def __init__(self,progs=[]) -> None:
        self.progs=progs
    def add(self, progsel, p, **kwargs):
        if type(progsel)==type('1t'): progsel="'%s'" % progsel
        self.progs.append((progsel,p,kwargs))
    def generate(self):
        lines = """"""
        for p in self.progs:
            p[1](**p[2])
            if self.progsel_gen: lines+="elif p==%s: %s()\n" % (p[0],p[2].get("fn", p[1].__name__))
        lines+="""else: return prog_ext(p)"""

        lines = """
            \n\n#=================================================
            # Main program select
            #================================================="""+"""
            def ProgSel(p):
                if type(p)==str: p=p.strip()
                if p==999: pass
                %s
            """ % lines.replace("\n","\n"+" "*16)
        return lines
    def main(self):
        pass

#=================================================
# Generic FN
#=================================================
class CARTELMAIN(GenericMain):
    def generate(self):
        robot.AddCode(f'from header{robot.Name()[-1]} import *\n')
        robot.AddCode(super().generate())


if __name__ == "__main__":
    try:
        #~ Generate
        if MAKE:
            print("if make")
            rdk.setRunMode(RUNMODE_MAKE_ROBOTPROG)
            for header in list(robot.HEADER.__dict__.values())[1:-3]: robot.AddCode(header)
            main = CARTELMAIN()

            #? Production Progs
            # main.add(1, MIG_EliteDoor, extended=True, add_auto=True)
            # main.add(2, MIG_MS3CoinReturnCup, workpiece='MS3CoinReturnCup', add_auto=True)

            # main.add(1, Laser_CALE, workpiece='CALE')
            main.add(2, Laser_MS3_10in, workpiece='MS3_10in')
            main.add(3, Laser_Vault_Chassis, workpiece='Vault_Chassis', fn='Laser_Vault_Chassis_x1', parts=[3])
            main.add(4, Laser_Vault_Chassis, workpiece='Vault_Chassis', fn='Laser_Vault_Chassis_x2', parts=[2,3])
            main.add(5, Laser_Vault_Chassis, workpiece='Vault_Chassis', fn='Laser_Vault_Chassis_x4', parts=[0,1,2,3])
            main.add(6, Laser_101_108, workpiece='101_108', fn='Laser_101_108_x10', parts=[0])
            main.add(7, Laser_101_108, workpiece='101_108', fn='Laser_101_108_x50', parts=[0,2,4,6,8])
            main.add(8, Laser_101_108, workpiece='101_108', fn='Laser_101_108_x100', parts=[])
            main.add(9, Laser_871_025B, workpiece='871_025B', tool='TCP 4mm z', fn='Laser_871_025B_x1', parts=[0])
            main.add(10, Laser_871_025B, workpiece='871_025B', tool='TCP 4mm z', fn='Laser_871_025B_x2', parts=[])
            main.add(11, Laser_767_2205_B, workpiece='767-2205 B', tool='TCP 5.5mm z', fn='Laser_767_2205_B_x1', parts=[0])
            main.add(12, Laser_767_2205_B, workpiece='767-2205 B', tool='TCP 5.5mm z', fn='Laser_767_2205_B_x2', parts=[0,1])
            main.add(13, Laser_767_2205_B, workpiece='767-2205 B', tool='TCP 5.5mm z', fn='Laser_767_2205_B_x7', parts=[0,1,2,3,4,5,6])
            main.add(14, Laser_1881_1015, workpiece='1881-1015', fn='Laser_1881_1015_x1', parts=[0])
            main.add(15, Laser_1881_1015, workpiece='1881-1015', fn='Laser_1881_1015_x2', parts=[0,1])
            main.add(16, Laser_767_119, workpiece='767-119', tool='TCP 5.5mm z', fn='Laser_767_119')

            #? Test progs
            # main.add(50, Laser_Vault_Chassis, workpiece='Vault_Chassis', fn='TEST_Laser_Vault_Chassis_x4', parts=[0,1,2,3], test=True)
            # main.add(51, Laser_101_108, workpiece='101_108', fn='TEST_Laser_101_108_x100', parts=[], test=True)
            # main.add(52, Laser_767_2205_B, workpiece='767-2205 B', tool='TCP 5.5mm z', fn='TEST_Laser_767_2205_B_x7', parts=[0,1,2,3,4,5,6], test=True)
            main.add(53, Laser_1881_1015, workpiece='1881-1015', fn='TEST_Laser_1881_1015_x1', parts=[0], test=True)
            main.add(54, Laser_767_119, workpiece='767-119', tool='TCP 5.5mm z', fn='TEST_Laser_767_119_x1', test=True)

            main.generate()

        #~ Simulate
        else:
            rdk.setSimulationSpeed(1.0)

            # Laser_CALE(workpiece='CALE')
            # Laser_MS3_10in(workpiece='MS3_10in')
            # Laser_Vault_Chassis(workpiece='Vault_Chassis', parts=[3])
            # Laser_Vault_Chassis(workpiece='Vault_Chassis', parts=[2,3])
            # Laser_Vault_Chassis(workpiece='Vault_Chassis', parts=[0,1,2,3])

            # Laser_101_108(workpiece='101_108', parts=[0])
            # Laser_101_108(workpiece='101_108', parts=[0,2,4,6,8])
            # Laser_101_108(workpiece='101_108', parts=[])
            # Laser_101_108(workpiece='101_108', parts=[], test=True)
            
            # Laser_871_025B(workpiece='871_025B', tool='TCP 4mm z', parts=[0])
            # Laser_871_025B(workpiece='871_025B', tool_holder_name='TCP 4mm z', parts=[])

            # Laser_767_2205_B(workpiece='767-2205 B', tool='TCP 5.5mm z', parts=[0,1,2,3,4,5,6])
            # Laser_767_2205_B(workpiece='767-2205 B', tool='TCP 5.5mm z', parts=[0,1,2,3,4,5,6], test=True)

            # Laser_1881_1015(workpiece='1881-1015', parts=[0])
            # Laser_1881_1015(workpiece='1881-1015', parts=[])
            # Laser_1881_1015(workpiece='1881-1015', parts=[0], test=True)

            Laser_767_119(workpiece='767-119', tool='TCP 5.5mm z')
            # Laser_767_119(workpiece='767-119', tool='TCP 5.5mm z', test=True)






    except:
        print("error")
        exc_info()
    finally: pass
    print("  >> Generation Complete")


