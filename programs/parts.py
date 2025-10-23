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
        self.parts              = get('parts', None) # weld only the specified part indices (0-based), e.g. [0,1] to weld parts 1 and 2
        self.test               = get('test', False)

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

        autoblend_moves(get_easeoffon_targets(5, tars[1], [5]))
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, z=rr), RelFrame(tars[1], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[2], [5]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[3], [70, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[4], [5]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[5], [5]))
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(70, tars[6], [70, 10]))
        run_circular_weld(tars[6], RelFrame(tars[6], y=rr, z=rr), RelFrame(tars[6], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[7], [5]))
        run_circular_weld(tars[7], RelFrame(tars[7], y=rr, z=rr), RelFrame(tars[7], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[8], [5]))
        run_circular_weld(tars[8], RelFrame(tars[8], y=rr, z=rr), RelFrame(tars[8], x=rr), num_circles=2, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=25), RelFrame(tars[8], z=100)])

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

        autoblend_moves(get_easeoffon_targets(40, tars[1], [10]))
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, z=rr), RelFrame(tars[1], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[2], [10]))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, z=rr), RelFrame(tars[2], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(80, tars[3], [80, 10]))
        run_circular_weld(tars[3], RelFrame(tars[3], y=rr, z=rr), RelFrame(tars[3], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(10, tars[4], [30, 10]))
        run_circular_weld(tars[4], RelFrame(tars[4], y=rr, z=rr), RelFrame(tars[4], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[5], [5]))
        run_circular_weld(tars[5], RelFrame(tars[5], y=rr, z=rr), RelFrame(tars[5], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(100, tars[6], [100, 10]))
        run_circular_weld(tars[6], RelFrame(tars[6], y=rr, z=rr), RelFrame(tars[6], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[7], [5]))
        run_circular_weld(tars[7], RelFrame(tars[7], y=rr, z=rr), RelFrame(tars[7], x=rr), num_circles=2, myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, tars[8], [5]))
        run_circular_weld(tars[8], RelFrame(tars[8], y=rr, z=rr), RelFrame(tars[8], x=rr), num_circles=2, myblend=rr/4)
        RelativeEaseOff([100], [FAST])

        if TEST: robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

    def TicketSpout(self, tar_frame):
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
        autoblend_moves([robot.Pose().Offset(z=10), RelFrame(tars[1], x=-25, z=125)])
        
        robot.nos_MoveJ(FAST, GetIK(Pose(40, 230, 150, 0, 0, 0)), blend=10)
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[2], z=150)), blend=10)
        EaseOn(tars[2], [25, 10], [FAST, FAST])
        run_circular_weld(tars[2], RelFrame(tars[2], x=-rr, z=rr), RelFrame(tars[2], y=rr), num_circles=2, speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=10), RelFrame(tars[2], x=25, z=50)])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[3], x=30, z=50)), blend=10)
        EaseOn(tars[3], [25, 10, 5], [FAST, FAST, SLOW])
        run_circular_weld(tars[3], RelFrame(tars[3], x=-rr, z=rr), RelFrame(tars[3], y=rr), num_circles=2, speed=0.25, myblend=rr/4)

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
        run_circular_weld(tars[0], RelFrame(tars[0], y=-rr, x=-rr/2, z=rr/2), RelFrame(tars[0], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface
        RelativeEaseOff([50], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[1].Offset(z=50)), blend=5)
        EaseOn(tars[1], [10], [FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], y=-rr, x=-rr), RelFrame(tars[1], z=-rr), speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[2].Offset(z=50)), blend=5)
        EaseOn(tars[2], [10], [FAST])
        run_circular_weld(tars[2], RelFrame(tars[2], y=-(rr+0.5)), RelFrame(tars[2], x=-rr/2, z=-rr/2), num_circles=2, speed=SLOWAF, myblend=rr/4)
        autoblend_moves([robot.Pose().Offset(z=50), RelFrame(tars[2], x=-100, z=125).Offset(rx=10)])

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
        run_circular_weld(tars[0], RelFrame(tars[0], x=-rr), RelFrame(tars[0], y=rr+0.5), num_circles=2, speed=SLOWAF, myblend=rr/4)
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FAST, GetIK(tars[1].Offset(z=75)), blend=5)
        EaseOn(tars[1], [10], [FAST])
        run_circular_weld(tars[1], RelFrame(tars[1], y=rr, x=-rr/2, z=rr/2), RelFrame(tars[1], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface

        autoblend_moves(get_easeoffon_targets(5, tars[2], 5))
        run_circular_weld(tars[2], RelFrame(tars[2], y=rr, x=-rr/2, z=rr/2), RelFrame(tars[2], x=-rr, z=-rr), speed=SLOWAF, myblend=rr/4) # 45 deg surface
        RelativeEaseOff([75], [FAST])

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints(), blend=5)
        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())



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





#^=========================
#^ Laser Vault_Chassis
#^=========================
class Laser_Vault_Chassis(GENERIC_LASER):
    def weld_pins(self, tar_frame):
        """
        Weld only the specified part indices.
        - self.parts: list of indices (0-based), e.g. [0,1] to weld parts 1 and 2.
        If None or [], weld all.
        """
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = (5.84 + 2) / 2 # actal diameter = 5.84
        
        if not self.parts:
            self.parts = [0, 1, 2, 3]

        #? right
        robot.nos_MoveJ(FASTAF, AddJoints(self.Tar001.Joints(), [-20,0,0,0,0,0]))
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[0], x=75, y=50, z=75)), blend=5)

        for c, (y_off, z_off) in enumerate([[-98.2, -1.5], [1.4, -0.9], [101.0, -1.15], [201.2, -0.65]]):
            if c not in self.parts:
                continue
            robot.AddCode(f'# right weld, index: {c}')
            t_right = RelFrame(tars[0], y=y_off, z=z_off)

            EaseOn(t_right, [30, 5], [FAST, FAST])
            if self.test:
                run_spot_weld(t_right, t_delay=0.5)
            else:
                run_circular_weld(t_right, RelFrame(t_right, z=rr), RelFrame(t_right, y=rr), speed=SLOWAF, myblend=rr/2)
            RelativeEaseOff([30], [FAST])

        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[0], x=75, y=50, z=75)))
        robot.nos_MoveJ(FAST, AddJoints(self.Tar001.Joints(), [-20,0,0,0,0,0]))

        #? left
        robot.nos_MoveJ(FAST, AddJoints(self.Tar001.Joints(), [20,0,0,0,0,0]))
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[1], x=-75, y=50, z=75)), blend=5)

        for c, (y_off, z_off) in enumerate([[-99.35, -1.55], [1.65, -2.25], [100.8, -1.75], [200.85, -1.5]]):
            if c not in self.parts:
                continue
            robot.AddCode(f'# left weld, index: {c}')
            t_left = RelFrame(tars[1], y=y_off, z=z_off)

            EaseOn(t_left, [30, 5], [FAST, FAST])
            if self.test:
                run_spot_weld(t_left, t_delay=0.5)
            else:
                run_circular_weld(t_left, RelFrame(t_left, z=rr), RelFrame(t_left, y=rr), speed=SLOWAF, myblend=rr/2)
            RelativeEaseOff([30], [FAST])
        
        robot.nos_MoveJ(FAST, GetIK(RelFrame(tars[1], x=-75, y=50, z=75)))
        robot.nos_MoveJ(FAST, AddJoints(self.Tar001.Joints(), [20,0,0,0,0,0]))
        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())


    #~ Run
    def run(self):
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        self.weld_pins(self.Retracted_Frame.findChild('n1_pins'))



#^=========================
#^ Laser SSPM Door Latch Plate (101-108)
#^=========================
class Laser_101_108(GENERIC_LASER):
    def weld_pins(self, tar_frame):
        """
        Weld only the specified part indices.
        - self.parts: list of indices (0-based), e.g. [0,1] to weld parts in block 1 and 2.
        If None or [], weld all.
        """
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        
        if not self.parts:
            self.parts = list(range(10)) # [0, 1, ..., 9]

        #? prep
        origin = tars[0]
        rr = (4.76 + 2) / 2 # actal diameter = 4.76
        C2C_DIST = 19.3
        XOFF = 199.4
        part_offsets = {
            'block_1': [XOFF + 0.4,     162.3 + 0.9],
            'block_2': [-XOFF - 0.55,   162.3 - 0.2],
            'block_3': [XOFF + 0.1,     102.3 + 0.9],
            'block_4': [-XOFF - 0.3,    102.3 - 0.1],
            'block_5': [XOFF + 0.25,    -9.1 + 0.4],
            'block_6': [-XOFF - 0.45,   -9.1 - 0.4],
            'block_7': [XOFF + 0.2,     -69.1 + 0.45],
            'block_8': [-XOFF - 0.6,    -69.1 - 0.5],
            'block_9': [XOFF + 0.3,     -129.1 + 0.55],
            'block_10': [-XOFF - 0.35,  -129.1 - 0.35],
        }

        row_vectors = []
        block_names = list(part_offsets.keys())
        block_values = list(part_offsets.values())
        for i in range(0, len(block_names), 2):
            p1 = np.array(block_values[i])
            p2 = np.array(block_values[i+1])
            vec = p2 - p1
            row_vectors.append(vec)
            # print(f'vector from {block_names[i]} to {block_names[i+1]}: {vec}')

        #? robot controls
        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        for idx, (part, (x_off, y_off)) in enumerate(part_offsets.items()):
            if idx not in self.parts:
                continue

            step_multipliers = list(range(10))
            if self.test:
                step_multipliers = [0]

            # Determine which row this block belongs to
            row_idx = idx // 2 # (0,1)->0, (2,3)->1, etc.
            vec = row_vectors[row_idx]

            # Odd blocks: use vec as is; Even blocks: reverse direction
            if idx % 2 == 1:
                vec = -vec
                step_multipliers.reverse()

            vec_len = np.linalg.norm(vec)
            if vec_len == 0:
                step_x, step_y = 0, 0
            else:
                step_x, step_y = vec / vec_len

            t = RelFrame(origin, x=x_off, y=y_off)

            for cc, m in enumerate(step_multipliers):
                xstep = step_x * C2C_DIST * m
                ystep = step_y * C2C_DIST * m
                tt = RelFrame(t, x=xstep, y=ystep)
                
                if idx == 0 and cc == 0:
                    EaseOn(tt, [40, 10, 1], [FASTAF, FAST, FAST])
                elif cc == 0:
                    EaseOn(tt, [20, 5, 1], [FASTAF, FAST, FAST])
                else:
                    EaseOn(tt, [1], [FASTAF])

                if self.test:
                    run_spot_weld(tt, t_delay=0.5)
                else:
                    run_semi_circular_weld(tt, RelFrame(tt, x=rr), RelFrame(tt, y=rr), [10, 20], rr/4)

                if cc == len(step_multipliers) - 1:
                    RelativeEaseOff([20], [FASTAF])

        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())
        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())

    #~ Run
    def run(self):
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        self.weld_pins(self.Retracted_Frame.findChild('part_ref'))






#^=========================
#^ Laser 871_025B (Tandem Battery Mount)
#^=========================
class Laser_871_025B(GENERIC_LASER):
    def _get_weld_targets(self, part_idx: int, config_tars):
        part_idx_offsets = {
            0: [0, 0, 0],
            1: [-189.88, 0, 0]
        }

        Z_OFF = 2.8
        weld_targets = {
            "left": {
                "0": [[16,  70.7, Z_OFF], [0,0,0], [0,0,0]],
                "1": [[16,  48.2, Z_OFF], [0,0,0], [0,0,0]],
                "2": [[16, -33.6, Z_OFF], [0,0,0], [0,0,0]],
                "3": [[16, -55.7, Z_OFF], [0,0,0], [0,0,0]],
            },
            "mid": {
                "0": [[44, -56.6, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "1": [[68, -56.6, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "2": [[104, -56.6, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "3": [[128, -56.6, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "4": [[44,  61.4, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "5": [[68,  61.4, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "6": [[104,  61.4, Z_OFF], [0, 0, 0], [0, 0, 0]],
                "7": [[128,  61.4, Z_OFF], [0, 0, 0], [0, 0, 0]],
            },
            "right": {
                "0": [[156,  65.0, Z_OFF], [0,0,0], [0,0,0]],
                "1": [[156,  50.0, Z_OFF], [0,0,0], [0,0,0]],
                "2": [[156, -35.0, Z_OFF], [0,0,0], [0,0,0]],
                "3": [[156, -50.0, Z_OFF], [0,0,0], [0,0,0]],
            },
        }

        left_tars, mid_tars, right_tars = [], [], []
        for config in ['left', 'mid', 'right']:
            for k,v in weld_targets[config].items():
                if config == 'left':
                    config_tar = config_tars[0]
                elif config == 'mid':
                    config_tar = config_tars[1]
                elif config == 'right':
                    config_tar = config_tars[2]
                
                t = RelFrame(
                    config_tar,
                    x = v[0][0] + v[1][0] + part_idx_offsets[part_idx][0],
                    y = v[0][1] + v[1][1] + part_idx_offsets[part_idx][1],
                    z = v[0][2] + v[1][2] + part_idx_offsets[part_idx][2],
                )

                if config == 'left':
                    left_tars.append(t)
                elif config == 'mid':
                    mid_tars.append(t)
                elif config == 'right':
                    right_tars.append(t)

        return left_tars, mid_tars, right_tars

    def left(self, rr, p0_left_tars, p1_left_tars):
        t = RelFrame(p0_left_tars[0], z=75)
        vv, aa = custom_speed_movel(robot.Pose(), t, self.fast_ww, self.fast_aa)
        robot.nos_MoveL([vv, aa], t, blend=5)

        EaseOn(p0_left_tars[0], [30, 5], [FAST, FAST])
        run_circular_weld(p0_left_tars[0], RelFrame(p0_left_tars[0], z=rr), RelFrame(p0_left_tars[0], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, p0_left_tars[1], [5]))
        run_circular_weld(p0_left_tars[1], RelFrame(p0_left_tars[1], z=rr), RelFrame(p0_left_tars[1], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(50, p0_left_tars[2], [50, 5]))
        run_circular_weld(p0_left_tars[2], RelFrame(p0_left_tars[2], z=rr), RelFrame(p0_left_tars[2], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, p0_left_tars[3], [5]))
        run_circular_weld(p0_left_tars[3], RelFrame(p0_left_tars[3], z=rr), RelFrame(p0_left_tars[3], y=rr), myblend=rr/4)
        if not p1_left_tars:
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)
        else:
            autoblend_moves([RelFrame(robot.Pose(), z=75), RelFrame(p1_left_tars[0], z=75), p1_left_tars[0].Offset(z=30), p1_left_tars[0].Offset(z=5)])
            run_circular_weld(p1_left_tars[0], RelFrame(p1_left_tars[0], z=rr), RelFrame(p1_left_tars[0], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(5, p1_left_tars[1], [5]))
            run_circular_weld(p1_left_tars[1], RelFrame(p1_left_tars[1], z=rr), RelFrame(p1_left_tars[1], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(50, p1_left_tars[2], [50, 5]))
            run_circular_weld(p1_left_tars[2], RelFrame(p1_left_tars[2], z=rr), RelFrame(p1_left_tars[2], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(5, p1_left_tars[3], [5]))
            run_circular_weld(p1_left_tars[3], RelFrame(p1_left_tars[3], z=rr), RelFrame(p1_left_tars[3], y=rr), myblend=rr/4)
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)

    def __mid_(self, rr, p0_mid_tars, p1_mid_tars):
        t = RelFrame(p0_mid_tars[0], z=75)
        vv, aa = custom_speed_movel(robot.Pose(), t, self.fast_ww, self.fast_aa)
        robot.nos_MoveL([vv, aa], t, blend=5)

        autoblend_moves([RelFrame(p0_mid_tars[0], z=15), RelFrame(p0_mid_tars[0], z=5)])
        run_circular_weld(p0_mid_tars[0], RelFrame(p0_mid_tars[0], y=rr, z=rr), RelFrame(p0_mid_tars[0], x=rr), myblend=rr/4)

        autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p0_mid_tars[1], z=5)])
        run_circular_weld(p0_mid_tars[1], RelFrame(p0_mid_tars[1], y=rr, z=rr), RelFrame(p0_mid_tars[1], x=rr), myblend=rr/4)

        autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p0_mid_tars[2], z=5)])
        run_circular_weld(p0_mid_tars[2], RelFrame(p0_mid_tars[2], y=rr, z=rr), RelFrame(p0_mid_tars[2], x=rr), myblend=rr/4)

        autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p0_mid_tars[3], z=5)])
        run_circular_weld(p0_mid_tars[3], RelFrame(p0_mid_tars[3], y=rr, z=rr), RelFrame(p0_mid_tars[3], x=rr), myblend=rr/4)
        if not p1_mid_tars:
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)
        else:
            autoblend_moves([RelFrame(robot.Pose(), z=75), RelFrame(p1_mid_tars[0], z=75), RelFrame(p1_mid_tars[0], z=5)])
            run_circular_weld(p1_mid_tars[0], RelFrame(p1_mid_tars[0], y=rr, z=rr), RelFrame(p1_mid_tars[0], x=rr), myblend=rr/4)

            autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p1_mid_tars[1], z=5)])
            run_circular_weld(p1_mid_tars[1], RelFrame(p1_mid_tars[1], y=rr, z=rr), RelFrame(p1_mid_tars[1], x=rr), myblend=rr/4)

            autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p1_mid_tars[2], z=5)])
            run_circular_weld(p1_mid_tars[2], RelFrame(p1_mid_tars[2], y=rr, z=rr), RelFrame(p1_mid_tars[2], x=rr), myblend=rr/4)

            autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(p1_mid_tars[3], z=5)])
            run_circular_weld(p1_mid_tars[3], RelFrame(p1_mid_tars[3], y=rr, z=rr), RelFrame(p1_mid_tars[3], x=rr), myblend=rr/4)
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)

    def mid(self, rr, p0_mid_tars, p1_mid_tars):
        t = RelFrame(p0_mid_tars[0], z=75)
        vv, aa = custom_speed_movel(robot.Pose(), t, self.fast_ww, self.fast_aa)
        robot.nos_MoveL([vv, aa], t, blend=5)

        for i, t1, t2 in iter_pairs(p0_mid_tars):
            if i == 0:
                autoblend_moves([RelFrame(t1, z=15), RelFrame(t1, z=5)])
            else:
                autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(t1, z=15), RelFrame(t1, z=5)])
            run_seam_weld(t1, t2, speed=SLOW, delay=0.15)

        robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)
        if not p1_mid_tars:
            return
        
        for i, t1, t2 in iter_pairs(p1_mid_tars):
            if i == 0:
                autoblend_moves([RelFrame(t1, z=75), RelFrame(t1, z=15), RelFrame(t1, z=5)])
            else:
                autoblend_moves([RelFrame(robot.Pose(), z=15), RelFrame(t1, z=15), RelFrame(t1, z=5)])
            run_seam_weld(t1, t2, speed=SLOW, delay=0.15)
        
        robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)

    def right(self, rr, p0_right_tars, p1_right_tars):
        t = RelFrame(p0_right_tars[0], z=75)
        vv, aa = custom_speed_movel(robot.Pose(), t, self.fast_ww, self.fast_aa)
        robot.nos_MoveL([vv, aa], t, blend=5)

        EaseOn(p0_right_tars[0], [30, 5], [FAST, FAST])
        run_circular_weld(p0_right_tars[0], RelFrame(p0_right_tars[0], z=rr), RelFrame(p0_right_tars[0], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, p0_right_tars[1], [5]))
        run_circular_weld(p0_right_tars[1], RelFrame(p0_right_tars[1], z=rr), RelFrame(p0_right_tars[1], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(50, p0_right_tars[2], [50, 5]))
        run_circular_weld(p0_right_tars[2], RelFrame(p0_right_tars[2], z=rr), RelFrame(p0_right_tars[2], y=rr), myblend=rr/4)

        autoblend_moves(get_easeoffon_targets(5, p0_right_tars[3], [5]))
        run_circular_weld(p0_right_tars[3], RelFrame(p0_right_tars[3], z=rr), RelFrame(p0_right_tars[3], y=rr), myblend=rr/4)
        if not p1_right_tars:
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)
        else:
            autoblend_moves([RelFrame(robot.Pose(), z=75), RelFrame(p1_right_tars[0], z=75), p1_right_tars[0].Offset(z=30), p1_right_tars[0].Offset(z=5)])
            run_circular_weld(p1_right_tars[0], RelFrame(p1_right_tars[0], z=rr), RelFrame(p1_right_tars[0], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(5, p1_right_tars[1], [5]))
            run_circular_weld(p1_right_tars[1], RelFrame(p1_right_tars[1], z=rr), RelFrame(p1_right_tars[1], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(50, p1_right_tars[2], [50, 5]))
            run_circular_weld(p1_right_tars[2], RelFrame(p1_right_tars[2], z=rr), RelFrame(p1_right_tars[2], y=rr), myblend=rr/4)

            autoblend_moves(get_easeoffon_targets(5, p1_right_tars[3], [5]))
            run_circular_weld(p1_right_tars[3], RelFrame(p1_right_tars[3], z=rr), RelFrame(p1_right_tars[3], y=rr), myblend=rr/4)
            robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=100), blend=5)

    def prep_run(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        config_tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))
        rr = 1.5

        if not self.parts:
            self.parts = list(range(2)) # [0, 1]

        if self.parts == [0]:
            p0_left_tars, p0_mid_tars, p0_right_tars = self._get_weld_targets(part_idx=0, config_tars=config_tars)
            p1_left_tars, p1_mid_tars, p1_right_tars = [], [], []
        else:
            p0_left_tars, p0_mid_tars, p0_right_tars = self._get_weld_targets(part_idx=0, config_tars=config_tars)
            p1_left_tars, p1_mid_tars, p1_right_tars = self._get_weld_targets(part_idx=1, config_tars=config_tars)


        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())

        # self.left(rr, p0_left_tars, p1_left_tars)
        self.mid(rr, p0_mid_tars, p1_mid_tars)
        # self.right(rr, p0_right_tars, p1_right_tars)
        
        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())





    #~ Run
    def run(self):
        self.fast_ww = 37
        self.fast_aa = 30
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        self.prep_run(self.Retracted_Frame.findChild('config'))





#^=========================
#^ Laser Anti Drill Plate (767-2205 B)
#^=========================
class Laser_767_2205_B(GENERIC_LASER):
    def _get_weld_targets(self, config_tars):
        Y_OFF_ROW_1 = 4.12
        Y_OFF_ROW_2 = -85.88
        Z_OFF = 12.5 # 10.125
        
        part_centerpoints = [
            [114.3, 0 + Y_OFF_ROW_1, Z_OFF - 0.1],
            [76.2,  0 + Y_OFF_ROW_1, Z_OFF - 0.2],
            [38.1,  0 + Y_OFF_ROW_1, Z_OFF - 0.4],
            [0,     0 + Y_OFF_ROW_1, Z_OFF - 0.5],
            [-38.1, 0 + Y_OFF_ROW_1, Z_OFF - 0.7],
            [-76.2, 0 + Y_OFF_ROW_1, Z_OFF - 0.9],
            [-114.3, 0 + Y_OFF_ROW_1, Z_OFF - 1.1],

            #! laser welding cable has too much stress against base for row 2 fixture position
            # [114.3, 0 + Y_OFF_ROW_2, Z_OFF],
            # [76.2,  0 + Y_OFF_ROW_2, Z_OFF],
            # [38.1,  0 + Y_OFF_ROW_2, Z_OFF],
            # [0,     0 + Y_OFF_ROW_2, Z_OFF],
            # [-38.1, 0 + Y_OFF_ROW_2, Z_OFF],
            # [-76.2, 0 + Y_OFF_ROW_2, Z_OFF],
            # [-114.3, 0 + Y_OFF_ROW_2, Z_OFF],
        ]

        R = 3.832 / 2 # ACTUAL radius of the through-hole we are welding inside of
        X_OFF = 7.56 # ACTUAL Center of part to center of through-hole we are welding inside of
        center_tars, rx_tars, positive_ry_tars, negative_ry_tars = [], [], [], []
        for n in self.parts:
            for x_offset in [X_OFF, -X_OFF]:
                # center - for testing
                t_center = RelFrame(
                    config_tars[0],
                    x = part_centerpoints[n][0] + x_offset,
                    y = part_centerpoints[n][1],
                    z = part_centerpoints[n][2]
                )
                center_tars.append(t_center)

                # rx
                t_rx = RelFrame(
                    config_tars[1],
                    x = part_centerpoints[n][0] + x_offset,
                    y = part_centerpoints[n][1] + R,
                    z = part_centerpoints[n][2]
                )
                rx_tars.append(t_rx)

            # +/- ry
            t_pos_ry = RelFrame(
                config_tars[3],
                x = part_centerpoints[n][0] - X_OFF,
                y = part_centerpoints[n][1],
                z = part_centerpoints[n][2]
            )
            positive_ry_tars.append(t_pos_ry)

            t_neg_ry = RelFrame(
                config_tars[4],
                x = part_centerpoints[n][0] + X_OFF,
                y = part_centerpoints[n][1],
                z = part_centerpoints[n][2]
            )
            negative_ry_tars.append(t_neg_ry)

        return center_tars, rx_tars, positive_ry_tars, negative_ry_tars

    def rx_welds(self, tar_frame):
        robot.AddCode(f'# {inspect.currentframe().f_code.co_name}')
        config_tars = GetTargetMats(tar_frame)
        SetFrame(tar_frame)
        SetTool(self.TCP_Holder.findChild(GetToolNameFromTarFrame(tar_frame)))

        #? prep        
        if not self.parts:
            self.parts = list(range(7)) # [0, 1, ..., 6]
            # self.parts = list(range(14)) # [0, 1, ..., 13] #! laser welding cable has too much stress against base for row 2 fixture position

        center_tars, rx_tars, positive_ry_tars, negative_ry_tars = self._get_weld_targets(config_tars)
        negative_ry_tars.reverse()

        #? robot controls
        robot.nos_MoveJ(FASTAF, self.Tar001.Joints())

        last_tar = None
        tars = center_tars if self.test else rx_tars
        for c, tar in enumerate(tars):
            extra_easeon = []
            if c == 0:
                t_approach = RelFrame(tar, z=75)
                vv, aa = custom_speed_movel(robot.Pose(), t_approach, self.fast_ww, self.fast_aa)
                robot.nos_MoveL([vv, aa], t_approach, blend=10)

            elif last_tar is not None:
                last_pos = last_tar.Pos()
                curr_pos = tar.Pos()
                dist = calculate_distance(last_pos, curr_pos)
                if dist > 100:
                    print(f"Large jump detected ({dist:.1f} mm) between targets {c-1} and {c}")
                    extra_easeon = [RelFrame(tar, z=50)]
                if dist > 50:
                    print(f"Large jump detected ({dist:.1f} mm) between targets {c-1} and {c}")
                    extra_easeon = [RelFrame(tar, z=25)]

            easeon_tars = extra_easeon + [RelFrame(tar, z=15), RelFrame(tar, z=5), RelFrame(tar, z=1)]
            autoblend_moves(easeon_tars)
            run_spot_weld(tar, t_delay=1.5, sp=SLOWAF)
            
            if c == len(tars) - 1:
                robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=75))
            else:
                robot.nos_MoveL(FAST, RelFrame(robot.Pose(), z=15), blend=1)

            last_tar = tar

        robot.nos_MoveJ(FASTAF, self.Tar000.Joints())


    #~ Run
    def run(self):
        self.fast_ww = 37
        self.fast_aa = 30
        SetSpeed(self.__class__.__name__)
        SetTool(self.TCP_Holder.findChild('mid'))
        SetFrame(self.Retracted_Frame)

        self.rx_welds(self.Retracted_Frame.findChild('config'))






