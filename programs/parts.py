from helper import *
from collections import defaultdict
import inspect



#^=======================================================================================================================
#^ Generic Laser Class
#^=======================================================================================================================
class GENERIC_LASER():
    def __init__(self, **kwargs):
        self.kw = kwargs
        self.auto_calls=[]

        def get(n,d):
            out = kwargs.get(n,None)
            if out != None: return out
            elif hasattr(self, n): return getattr(self,n)
            else: return d

        self.fn                 = get('fn', self.__class__.__name__)
        self.tool_holder_name   = get('tool', 'MIG 00 Holder')
        self.workpiece          = get('workpiece', 'EliteDoor')
        self.workpiece_name     = 'Workpiece '+self.workpiece
        self.retracted          = get('retracted', True)
        self.extended           = get('extended', False)
        self.add_auto           = get('add_auto', False)

        if bool(get("auto", True)): self.main()

    def init(self):
        robot.AddCode("# INITIALIZATION")
        self.Robot_Frame        = rdk.Item(ROBOT)
        self.TCP_Holder         = self.Robot_Frame.findChild(self.tool_holder_name)

        self.Workpiece_Frame    = self.Robot_Frame.findChild(self.workpiece_name)
        self.Retracted_Frame    = self.Workpiece_Frame.findChild('Retracted Holder').findChild('Retracted Frame')
        if self.extended: self.Extended_Frame = self.Workpiece_Frame.findChild('Extended Holder').findChild('Extended Frame')

        self.Joint_Folder       = self.Workpiece_Frame.findChild('Joint Targets')
        self.Tar000             = self.Joint_Folder.findChild('000')
        self.Tar001             = self.Joint_Folder.findChild('001')

        self.Target_Frames      = self.__get_target_frames()

    def __get_target_frames(self):
        new_children,frames=[],[]
        if self.retracted: frames.append(self.Retracted_Frame)
        if self.extended: frames.append(self.Extended_Frame)
        for f in frames:
            children=f.Childs()
            for i in children:
                if i.Type()!=3: continue
                elif i.Name().startswith('_'): continue
                i.Wname=i.Name().split(' - ')[0]
                new_children.append(i)
        return new_children

    def generate_auto(self):
        robot.AddCode('if part=="auto":')
        robot.AddTab(1)

        # req_list=[[self.workpiece]+sublist for sublist in self.auto_calls if sublist[1] is not None]
        req_list=[]
        for sublist in self.auto_calls:
            if sublist[2]: req_list.append([self.workpiece]+sublist[:2])
        # robot.AddCode(f'SendPartRequest({req_list})')

        for s in self.auto_calls:
            p1=s[0]
            p2=s[1] if len(s)>1 else None
            robot.AddCode(f'{self.fn}("{p1}", {p2}, False)')
            # print(f'{self.fn}("{p1}", {p2})')
        robot.AddTab(0)

    def run(self):
        pass

    def main(self):
        print(self.fn)
        robot.AddHeader(self.fn)
        robot.AddCode(f'def {self.fn}():')
        robot.AddTab(True)
        robot.AddCode(f'print("running {self.fn}")')
        rdk.setCollisionActive(0)

        self.init()
        self.run()
        if self.add_auto: self.generate_auto()

        robot.AddCode("# DONE")
        robot.AddTab(False)



#^=========================
#^ Laser CALE
#^=========================
class Laser_CALE(GENERIC_LASER):
    #~ Spot Welds
    def SideBracketTop(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        EaseOn(tars[6], [80, 10], [FAST, FAST])
        run_circular_weld(tars[6], RelFrame(tars[6], x=-rr, z=rr), RelFrame(tars[6], y=rr), speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=20), RelFrame(tars[6], z=100)])

        robot.nos_MoveJ(FAST, RelFrame(tars[7], z=100))
        EaseOn(tars[7], [20, 10], [FAST, FAST])
        run_circular_weld(tars[7], RelFrame(tars[7], x=rr, z=rr), RelFrame(tars[7], y=-rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([50], [FAST])

        t = RelFrame(tars[0], x = -3)
        robot.nos_MoveJ(FAST, t.Offset(z=50))
        EaseOn(t, [20, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[0], x = 3)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = -4)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = 4)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        autoblend_moves(get_easeoffon_targets(50, tars[2], [20, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[3], [10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[4], [70, 10]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), myblend=rr/4)
        
        autoblend_moves(get_easeoffon_targets(10, tars[5], [10]))
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([100], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def SideBracketMiddle(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        t = RelFrame(tars[0], x = -4)
        EaseOn(t, [50, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[0], x = 4)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[0], x = -4 + 25)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[0], x = 4 + 25)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = -4)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = 4)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = -4 + 25)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[1], x = 4 + 25)
        EaseOn(t, [1], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        autoblend_moves(get_easeoffon_targets(50, tars[2], [50, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(40, tars[3], [40, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[4], [70, 10]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), myblend=rr/4)

        autoblend_moves([RelFrame(robot.Pose(), z=10), RelFrame(tars[5], z=10)])
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([80], [FAST])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[6], z=80)))
        EaseOn(tars[6], [20, 10], [FAST])
        run_circular_weld(tars[6], RelFrame(tars[6], x=-rr, z=rr), RelFrame(tars[6], y=rr), myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=20), RelFrame(tars[6], z=80)])

        robot.nos_MoveJ(FAST, GetIK(tars[5].Offset(z=80))) # move back to previous joint config

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def SideBracketBottom(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5
        
        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        t = RelFrame(tars[0], x = -4)
        EaseOn(t, [50, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))

        t = RelFrame(tars[0], x = 2)
        EaseOn(t, [10], [FAST])
        run_linear_sleep_weld(RelFrame(t, y=-2), RelFrame(t, y=1))
        RelativeEaseOff([80], [FAST])

        t = RelFrame(tars[1], x = 0)
        robot.nos_MoveJ(FAST, t.Offset(z=75))
        EaseOn(t, [20, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(t, x=-2, y=-2), RelFrame(t, x=1, y=1))

        t = RelFrame(tars[1], x = 4)
        EaseOn(t, [10], [FAST])
        run_linear_sleep_weld(RelFrame(t, x=-2, y=-2), RelFrame(t, x=1, y=1))
        RelativeEaseOff([50], [FAST])

        EaseOn(tars[2], [20, 10], [FAST, FAST])
        run_circular_weld(tars[2], RelFrame(tars[2], x=rr, z=rr), RelFrame(tars[2], y=-rr), myblend=rr/4)
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[3], z=100)))
        EaseOn(tars[3], [30, 10], [FAST, FAST])
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), myblend=rr/4)
        RelativeEaseOff([50], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[4].Offset(z=50)))
        EaseOn(tars[4], [10], [FAST])
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([100], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def StiffenerTop(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveL(FAST, RelFrame(tars[0], z=100))
        EaseOn(tars[0], [25, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], y=rr, z=rr), RelFrame(tars[0], x=rr), myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=50), RelFrame(tars[0], z=100)])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[1], z=100)))
        EaseOn(tars[1], [50, 10], [FAST, FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], x=rr, z=rr), RelFrame(tars[1], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[2], [10]))
        run_circular_weld(tars[2], RelFrame(tars[2], x=rr, z=rr), RelFrame(tars[2], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[3], [70, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], x=rr, z=rr), RelFrame(tars[3], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[4], [10]))
        run_circular_weld(tars[4], RelFrame(tars[4], x=rr, z=rr), RelFrame(tars[4], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[5], [10]))
        run_circular_weld(tars[5], RelFrame(tars[5], x=rr, z=rr), RelFrame(tars[5], y=-rr), myblend=rr/4)
        RelativeEaseOff([80], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def StiffenerBot(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        EaseOn(tars[0], [80, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], x=rr, z=rr), RelFrame(tars[0], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[1], [10]))
        run_circular_weld(tars[1], RelFrame(tars[1], x=rr, z=rr), RelFrame(tars[1], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(80, tars[2], [80, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], x=rr, z=rr), RelFrame(tars[2], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[3], [10]))
        run_circular_weld(tars[3], RelFrame(tars[3], x=rr, z=rr), RelFrame(tars[3], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(50, tars[4], [20, 10]))
        run_circular_weld(tars[4], RelFrame(tars[4], x=rr, z=rr), RelFrame(tars[4], y=-rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(80, tars[5], [80, 10]))
        run_circular_weld(tars[5], RelFrame(tars[5], x=rr, z=rr), RelFrame(tars[5], y=-rr), myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=20), RelFrame(tars[5], z=150)])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[6], z=150)))
        EaseOn(tars[6], [50, 10], [FAST, FAST])
        run_circular_weld(tars[6], RelFrame(tars[6], y=rr, z=rr), RelFrame(tars[6], x=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(50, tars[7], [20, 10]))
        run_circular_weld(tars[7], RelFrame(tars[7], y=rr, z=rr), RelFrame(tars[7], x=rr), myblend=rr/4)
        RelativeEaseOff([80], [FAST])
        
        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def TicketSpout(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5
        
        # if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())
        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        #? first set of tars
        SetTool(self.TCP_Holder.findChild('right'))
        EaseOn(tars[0], [50, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], x=-rr, z=rr), RelFrame(tars[0], y=rr), speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(50, tars[1], [10]))
        run_circular_weld(tars[1], RelFrame(tars[1], x=-rr, z=rr), RelFrame(tars[1], y=rr), speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(20, tars[2], [20, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], x=-rr, z=rr), RelFrame(tars[2], y=rr), speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[3], [50, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], x=-rr, z=rr), RelFrame(tars[3], y=rr), speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=20), RelFrame(tars[3], z=100)])

        #? second set of tars
        SetTool(self.TCP_Holder.findChild('mid'))
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[4], z=100)))
        EaseOn(tars[4], [50, 10], [FAST, FAST])
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([50], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[5].Offset(z=75)))
        EaseOn(tars[5], [50, 10], [FAST, FAST])
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=25), RelFrame(tars[5], z=100)])

        SetTool(self.TCP_Holder.findChild('right'))
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[6], z=100)))
        EaseOn(tars[6], [25, 10], [FAST, FAST])
        run_circular_weld(tars[6], RelFrame(tars[6], y=-rr, z=rr), RelFrame(tars[6], x=rr), speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=25), RelFrame(tars[6], z=50)])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[7], z=50)))
        EaseOn(tars[7], [25, 10], [FAST, FAST])
        run_circular_weld(tars[7], RelFrame(tars[7], y=-rr, z=rr), RelFrame(tars[7], x=rr), speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=25), RelFrame(tars[7], z=50)])

        SetTool(self.TCP_Holder.findChild('mid'))
        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())



    #~ testing
    def test_ScrapSurface_(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.setSlowSpeeds(15, 15, 200, 5)
        r = 1.0 # 1.5
        _x = 40*0
        _y = -10

        robot.AddCode('#* t relative 0')
        t = RelFrame(tars[5], x=0+_x, y=_y)
        EaseOn(t, [100, 10], [FAST, FAST])
        run_circular_weld(t, RelFrame(t, y=r, z=r), RelFrame(t, x=r), myblend=r/4)
        RelativeEaseOff([10], [FAST])
        robot.AddCode('robot.waitmove()')
        robot.AddCode('time.sleep(1)')

        robot.AddCode('#* t relative 1')
        t = RelFrame(tars[5], x=10+_x, y=_y)
        EaseOn(t, [10], [FAST])
        run_circular_weld(t, RelFrame(t, y=r, z=r), RelFrame(t, x=r), myblend=r/4)
        RelativeEaseOff([10], [FAST])
        robot.AddCode('robot.waitmove()')
        robot.AddCode('time.sleep(1)')

        # robot.AddCode('#* t relative 2')
        # t = RelFrame(tars[5], x=20+_x, y=_y)
        # EaseOn(t, [10], [FAST])
        # run_circular_weld(t, RelFrame(t, y=r, z=r), RelFrame(t, x=r), myblend=r/4)
        # RelativeEaseOff([10], [FAST])
        # robot.AddCode('robot.waitmove()')
        # robot.AddCode('time.sleep(1)')

        # robot.AddCode('#* t relative 3')
        # t = RelFrame(tars[5], x=30+_x, y=_y)
        # EaseOn(t, [10], [FAST])
        # run_circular_weld(t, RelFrame(t, y=r, z=r), RelFrame(t, x=r), myblend=r/4)
        # RelativeEaseOff([10], [FAST])

        
        #* end
        RelativeEaseOff([50], [FAST])
        robot.nos_MoveL(FAST, RelFrame(t, z=100))
        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def test_SideBrackets_(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        # robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        #? tars[0]
        # EaseOn(tars[0], [80, 10], [FAST, FAST])
        # run_linear_sleep_weld(RelFrame(tars[0], x=2), RelFrame(tars[0], x=-1))
        # RelativeEaseOff([80], [FAST])

        EaseOn(tars[0], [80, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], x=rr, z=rr), RelFrame(tars[0], y=-rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([80], [FAST])

        #? tars[1]
        # EaseOn(tars[1], [80, 10], [FAST, FAST])
        # run_linear_sleep_weld(RelFrame(tars[1], x=-2), RelFrame(tars[1], x=1))
        # RelativeEaseOff([80], [FAST])

        #? best run for tars[1]
        # EaseOn(tars[1], [80, 10], [FAST, FAST])
        # run_circular_weld(tars[1], RelFrame(tars[1], x=-rr, z=rr), RelFrame(tars[1], y=rr), speed=SLOWAF, myblend=rr/4)
        # RelativeEaseOff([80], [FAST])


        # EaseOn(tars[3], [80, 10], [FAST, FAST])
        # run_circular_weld(tars[3], RelFrame(tars[3], x=-rr, z=rr), RelFrame(tars[3], y=rr), myblend=rr/4)
        # RelativeEaseOff([80], [FAST])


        # EaseOn(tars[5], [80, 10], [FAST, FAST])
        # run_linear_sleep_weld(RelFrame(tars[5], x=-2, y=-2), RelFrame(tars[5], x=1, y=1))
        # RelativeEaseOff([80], [FAST])

        # EaseOn(tars[6], [80, 10], [FAST, FAST])
        # run_linear_sleep_weld(RelFrame(tars[6], x=-2, y=-2), RelFrame(tars[6], x=1, y=1))
        # RelativeEaseOff([80], [FAST])


    #~ Run
    def run(self):
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        #? Loop through target frames
        for c, tar_frame in enumerate(self.Target_Frames):

            if False: pass            
            # elif tar_frame.Wname=='test_ScrapSurface_': self.test_ScrapSurface_(tar_frame)
            # elif tar_frame.Wname=='test_SideBrackets_': self.test_SideBrackets_(tar_frame)

            elif tar_frame.Wname=='SideBracketTop': self.SideBracketTop(tar_frame)
            elif tar_frame.Wname=='SideBracketMiddle': self.SideBracketMiddle(tar_frame)
            elif tar_frame.Wname=='SideBracketBottom': self.SideBracketBottom(tar_frame)
            elif tar_frame.Wname=='StiffenerTop': self.StiffenerTop(tar_frame)
            elif tar_frame.Wname=='StiffenerBot': self.StiffenerBot(tar_frame)
            elif tar_frame.Wname=='TicketSpout': self.TicketSpout(tar_frame)


            else:
                # robot.AddCode('pass')
                print(f'no function call for "{tar_frame.Name()}" (aka: {tar_frame.Wname})')
            




#^=========================
#^ Laser MS3_10in
#^=========================
class Laser_MS3_10in(GENERIC_LASER):
    #~ Spot Welds
    def UpperStiffener(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveL(FAST, RelFrame(tars[0], z=100))
        EaseOn(tars[0], [25, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], y=rr, z=rr), RelFrame(tars[0], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[1], [10]))
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, z=rr), RelFrame(tars[1], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[2], [10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[3], [70, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[4], [10]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[5], [10]))
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), num_circles=2, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=25), RelFrame(tars[5], z=100)])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def LowerStiffener(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        autoblend_moves([RelFrame(tars[0], z=100), tars[0].Offset(z=25), tars[0].Offset(z=10)])
        run_circular_weld(tars[0], RelFrame(tars[0], y=rr, z=rr), RelFrame(tars[0], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(30, tars[1], [10]))
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, z=rr), RelFrame(tars[1], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[2], [10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[3], [10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(80, tars[4], [80, 10]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[5], [10]))
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[6], [10]))
        run_circular_weld(tars[6], RelFrame(tars[6], y=rr, z=rr), RelFrame(tars[6], x=rr), num_circles=2, myblend=rr/4)
        RelativeEaseOff([100], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def TicketSpout(self, tar_frame):
        """ Running into some difficulty welding tar[2] (The coin slot side of the bottom ticket spout bracket). It looks like the first weld on it is causing this side to raise about 1mm before it can get welded. """
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5
        
        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[0], x=-50, z=125)), blend=5)
        EaseOn(tars[0], [30, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], x=rr, z=rr), RelFrame(tars[0], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(25, tars[1], [30, 10]))
        run_circular_weld(tars[1], RelFrame(tars[1], x=rr, z=rr), RelFrame(tars[1], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=10), RelFrame(tars[1], z=100)])
        
        robot.nos_MoveJ(FAST, GetIK(Pose(40, 230, 150, 0, 0, 0)), blend=5)
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[2], z=150)), blend=5)
        EaseOn(tars[2], [25, 10], [FAST, FAST])
        run_circular_weld(tars[2], RelFrame(tars[2], x=-rr, z=rr), RelFrame(tars[2], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)

        tars_to_next = [
            robot.Pose().Offset(z=10),
            RelFrame(tars[2], x=50, z=50),
            RelFrame(tars[3], x=30, z=50),
            tars[3].Offset(z=25),
            tars[3].Offset(z=10),
            tars[3].Offset(z=1)
        ]
        autoblend_moves(tars_to_next)
        run_linear_sleep_weld(RelFrame(tars[3], x=1), RelFrame(tars[3], x=-1.5), delay=0.66)
        autoblend_moves([robot.Pose().Offset(z=10), RelFrame(tars[3], z=100)])
        robot.nos_MoveJ(FAST, GetIK(Pose(-50, 100, 150, 20, -10, 0)))

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def LHBracket(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[0], x=-100, z=75)), blend=5)
        EaseOn(tars[0], [50, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], y=-rr, x=-rr), RelFrame(tars[0], z=-rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[1].Offset(z=50)), blend=5)
        EaseOn(tars[1], [10], [FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], y=-rr, x=-rr/2, z=rr/2), RelFrame(tars[1], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface

        autoblend_moves(get_easeoffon_targets(30, tars[2], [20, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=-rr, x=-rr/2, z=rr/2), RelFrame(tars[2], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[3].Offset(z=50)), blend=5)
        EaseOn(tars[3], [10], [FAST])
        run_linear_sleep_weld(RelFrame(tars[3], x=-2), RelFrame(tars[3], x=1.5))
        RelativeEaseOff([100], [FAST])

        t = RelFrame(tars[4], x = 8)
        robot.nos_MoveJ(FAST, GetIK(t.Offset(z=50)), blend=5)
        EaseOn(t, [20, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(t, y=1.5), RelFrame(t, y=-1))
        RelativeEaseOff([125], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())
        
    def SwitchMount(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveJ(FAST, GetIK(tars[0].Offset(z=150)), blend=5)
        EaseOn(tars[0], [50, 10], [FAST, FAST])
        run_circular_weld(tars[0], RelFrame(tars[0], y=rr, x=-rr), RelFrame(tars[0], z=-rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[1].Offset(z=50)), blend=5)
        EaseOn(tars[1], [10], [FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, x=-rr/2, z=rr/2), RelFrame(tars[1], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface

        autoblend_moves(get_easeoffon_targets(30, tars[2], [20, 10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, x=-rr/2, z=rr/2), RelFrame(tars[2], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[3].Offset(z=75)), blend=5)
        EaseOn(tars[3], [20, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(tars[3], z=2), RelFrame(tars[3], z=-0.5))
        RelativeEaseOff([40], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[4].Offset(z=30)), blend=5)
        EaseOn(tars[4], [20, 10], [FAST, FAST])
        run_linear_sleep_weld(RelFrame(tars[4], z=2), RelFrame(tars[4], z=-0.5))
        RelativeEaseOff([100], [FAST])

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints(), blend=5)
        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())


    def _TicketSpout_og(self, tar_frame):
        """ Running into some difficulty welding tar[2] (The coin slot side of the bottom ticket spout bracket). It looks like the first weld on it is causing this side to raise about 1mm before it can get welded. """
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5
        
        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[0], z=125)))
        EaseOn(tars[0], [50, 10, 0], [FAST, FAST, SLOW])
        run_linear_sleep_weld(RelFrame(tars[0], x=1), RelFrame(tars[0], x=-1.5), delay=0.5)
        RelativeEaseOff([25], [FAST])
        robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=50))

        robot.nos_MoveL(FAST, RelFrame(tars[1], z=50))
        EaseOn(tars[1], [30, 10], [FAST, FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], x=-rr, z=rr), RelFrame(tars[1], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([50], [FAST])
        robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100))
        
        robot.nos_MoveJ(FAST, GetIK(Pose(40, 230, 200, 0, 0, 0)))
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[2], z=150)))
        EaseOn(tars[2], [25, 10], [FAST, FAST])
        run_circular_weld(tars[2], RelFrame(tars[2], x=rr, z=rr), RelFrame(tars[2], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(25, tars[3], [25, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], x=rr, z=rr), RelFrame(tars[3], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([75], [FAST])
        robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=50))

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())


    #~ Run
    def run(self):
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        #? Loop through target frames
        for c, tar_frame in enumerate(self.Target_Frames):

            if False: pass
            elif tar_frame.Wname=='UpperStiffener': self.UpperStiffener(tar_frame)
            elif tar_frame.Wname=='LowerStiffener': self.LowerStiffener(tar_frame)
            elif tar_frame.Wname=='TicketSpout': self.TicketSpout(tar_frame)
            elif tar_frame.Wname=='LHBracket': self.LHBracket(tar_frame)
            elif tar_frame.Wname=='SwitchMount': self.SwitchMount(tar_frame)

            else:
                print(f'no function call for "{tar_frame.Name()}" (aka: {tar_frame.Wname})')









