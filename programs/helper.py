from setup import *
import numpy as np
import copy


#~ RoboDK Stuff
def isClass(c):
    """Returns true if argument is a class"""
    class C():pass
    return type(c)==type(C)

def findChild(self,name,recursive=True):
    for child in self.Childs():
        if child.Name() == name:
            return child
        if recursive:
            if len(child.Childs())>0:
                r = child.findChild(name, recursive)
                if r: return r
Item.findChild = findChild

def GetTargetItems(frame):
    return [t for t in frame.Childs() if t.Type()==6]

def GetTargetMats(frame):
    return [t.Pose() for t in frame.Childs() if t.Type()==6]

def GetTargetNames(frame):
    return [t.Name() for t in frame.Childs() if t.Type()==6]

def GetIK(target_pose, ref_joints=None, tool=None, frame=None):
    if ref_joints is None:
        ref_joints = robot.Joints()
    if tool is None:
        tool = robot.PoseTool()
    if frame is None:
        frame = robot.PoseFrame()
    return robot.SolveIK(target_pose, ref_joints, tool, frame)

def AddJoints(joints, addition:list):
    if isinstance(joints, Mat):
        joints=joints.tolist()
    if len(joints)!=len(addition):
        print(f'Warning: AddJoints({joints, addition}) mst be of same len')
        return joints
    out=[j+a for j,a in zip(joints, addition)]
    return out

def SetTool(toolframe):
    robot.setPoseTool(toolframe)
    pose=pose_2_xyzrpw(robot.PoseTool())
    rounded_pose=[round(val,5) for val in pose]
    robot.AddCode(f'robot.set_tool({rounded_pose})')

def SetFrame(refframe):
    robot.setPoseFrame(refframe)
    pose=pose_2_xyzrpw(robot.PoseFrame())
    rounded_pose=[round(val,5) for val in pose]
    robot.AddCode(f'robot.set_frame({rounded_pose})')

def SetSpeed(s:str):
    print(f'SetSpeed({s})')
    if s=='Laser_CALE':
        robot.setSlowSpeeds(*s_mig)
        robot.setFastSpeeds(*f_mig)
    elif s=='Laser_Elite':
        robot.setSlowSpeeds(*s_mig)
        robot.setFastSpeeds(*f_mig)
    else:
        print(f'!!Warning!! No speed set for "{s}"')

def GetToolNameFromTarFrame(tar_frame):
    name=tar_frame.Name()
    if name.endswith('leftx2'):     return 'leftx2'
    elif name.endswith('left'):     return 'left'
    elif name.endswith('mid'):      return 'mid'
    elif name.endswith('right'):    return 'right'
    elif name.endswith('rightx2'):  return 'rightx2'
    else:                           return 'mid'


#~ Tool I/O
def Laser(b, t_delay=None):
    if b:
        if t_delay is None: robot.AddCode('Laser(1)')
        else: robot.AddCode(f'Laser(1, {t_delay})')
        if not MAKE: rdk.Command('Trace', 'On')
    else:
        robot.AddCode('Laser(0)')
        if not MAKE: rdk.Command('Trace', 'Off')

def AddSleep(t):
    if MAKE: robot.AddCode("time.sleep(%s)" % t)
    else: time.sleep(t)

def Post(pn,qty):
    if MAKE: robot.AddCode("PostInc(\"%s\",%s)" % (pn, qty))


#~ Math
def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(np.array(point1) - np.array(point2))


#~ Movement helpers
def __EaseOn(tar, zdistances:list, speeds:list, autoblend=True):
    blend = 5 if autoblend else 0
    ilast = len(zdistances) - 1
    for i, (dist,sp) in enumerate(zip(zdistances,speeds)):
        if i == ilast:
            robot.nos_MoveL(sp, tar.Offset(z=dist))
        else:
            robot.nos_MoveL(sp, tar.Offset(z=dist), blend=blend)

def EaseOn(tar, zdistances: list, speeds: list, autoblend=True):
    blend_ratio = 0.2
    ilast = len(zdistances) - 1
    current_position = robot.Pose()

    for i, (dist, sp) in enumerate(zip(zdistances, speeds)):
        target_position = tar.Offset(z=dist)

        if i == ilast:
            robot.nos_MoveL(sp, target_position, blend=0)
        else:
            next_position = tar.Offset(z=zdistances[i + 1])
            
            dist_to_target = calculate_distance(current_position, target_position)
            dist_to_next = calculate_distance(target_position, next_position)
            min_distance = min(dist_to_target, dist_to_next)
            
            blend = blend_ratio * min_distance if autoblend else 0
            # print(f'blend: {blend}')
            
            robot.nos_MoveL(sp, target_position, blend=blend)
            
            current_position = target_position

def RelativeEaseOff(zdistances:list, speeds:list, autoblend=True):
    blend = 1 if autoblend else 0
    ilast = len(zdistances) - 1
    tar = robot.Pose()
    for i, (dist, sp) in enumerate(zip(zdistances, speeds)):
        if i==ilast:
            robot.nos_MoveL(sp, tar.Offset(z=dist))
        else:
            robot.nos_MoveL(sp, tar.Offset(z=dist), blend=blend)

def get_easeoffon_targets(z_easeoff, t, z_easeon):
    targets = []

    # Ease off wrt robot pose
    targets.append(robot.Pose().Offset(z=z_easeoff))

    # Ease on wrt target
    if not isinstance(z_easeon, list):
        targets.append(t.Offset(z=z_easeon))
    else:
        for z in z_easeon:
            targets.append(t.Offset(z=z))
    
    return targets

def autoblend_moves(targets, speeds=[FAST], blend_ratio=0.2):
    if len(targets) != len(speeds):
        # Extend speeds with speeds[0] until it matches the length of targets
        speeds.extend([speeds[0]] * (len(targets) - len(speeds)))
    
    ilast = len(targets) - 1
    current_position = robot.Pose()

    for i, (tar, sp) in enumerate(zip(targets, speeds)):
        if i == ilast:
            robot.nos_MoveL(sp, tar, blend=0)
        else:
            next_position = targets[i + 1]
            
            dist_to_target = calculate_distance(current_position, tar)
            dist_to_next = calculate_distance(tar, next_position)
            min_distance = min(dist_to_target, dist_to_next)
            
            blend = blend_ratio * min_distance
            # print(f'blend: {blend}')
            
            robot.nos_MoveL(sp, tar, blend=blend)
            
            current_position = tar




#~ Target runs
def generate_zigzag_path(t_start, t_end, step_size, x_amp=0, y_amp=0, z_amp=0):
    """
    Generate a zig-zag path from t_start to t_end with specified amplitudes for each axis, starting at the maximum displacement.

    Args:
        t_start (robomath.Mat): Starting transformation matrix.
        t_end (robomath.Mat): Ending transformation matrix.
        step_size (float): Distance between each step along the main path.
        x_amp (float): Amplitude of the zig-zag along the x-axis.
        y_amp (float): Amplitude of the zig-zag along the y-axis.
        z_amp (float): Amplitude of the zig-zag along the z-axis.

    Returns:
        list: List of zig-zag transformation matrices (robomath.Mat).
    """
    # Calculate start and end positions as numpy arrays
    start_pos = np.array(t_start.Pos())
    finish_pos = np.array(t_end.Pos())

    # Calculate the direction vector and the number of steps
    direction_vector = finish_pos - start_pos
    total_distance = np.linalg.norm(direction_vector)
    unit_vector = direction_vector / total_distance  # Normalize to unit vector
    num_steps = int(total_distance / step_size)  # Calculate number of steps based on step_size

    # List to hold the zig-zag target points
    targets = []

    # Set up zig-zag amplitudes for each axis
    amplitudes = np.array([x_amp, y_amp, z_amp])

    # Generate zig-zag points
    for i in range(num_steps + 1):
        # Interpolation factor
        t = i / num_steps
        interp_pos = start_pos + t * direction_vector

        # Apply zig-zag offsets, starting with a maximum displacement on the first point
        zig_offset = amplitudes * (-1) ** i  # Alternating sign, starting with max
        interp_pos_with_zigzag = interp_pos + zig_offset

        # Create a new transformation matrix with the zig-zag position
        tar = copy.deepcopy(t_start)
        tar.setPos(interp_pos_with_zigzag)
        targets.append(tar)
        # print(tar)

    return targets

def run_zigzag_weld(t_start, t_end, step_size, x_amp=0, y_amp=0, z_amp=0, speed=SLOW, myblend=0.5):
    """
    Generate a zig-zag path from t_start to t_end with blends applied to smooth out movements.

    Args:
        t_start (robomath.Mat): Starting transformation matrix.
        t_end (robomath.Mat): Ending transformation matrix.
        step_size (float): Distance between each step along the main path.
        x_amp (float): Amplitude of the zig-zag along the x-axis.
        y_amp (float): Amplitude of the zig-zag along the y-axis.
        z_amp (float): Amplitude of the zig-zag along the z-axis.
        speed: Movement speed for the robot.
        autoblend (bool): If True, add blending between zig-zag points.
    """
    zigzag_targets = generate_zigzag_path(
        t_start, t_end, step_size, x_amp, y_amp, z_amp
    )

    total_targets = len(zigzag_targets)

    for i, t in enumerate(zigzag_targets):
        if i == 0:
            robot.nos_MoveL(speed, t, blend=0)
            Laser(1)
        elif i == total_targets - 1:
            robot.nos_MoveL(speed, t, blend=0)
        else:
            robot.nos_MoveL(speed, t, blend=myblend)

    Laser(0)

def run_spot_weld(t, t_delay=1, sp=SLOW):
    robot.nos_MoveL(sp, t, blend=0)
    Laser(1)
    AddSleep(t_delay)
    Laser(0)

def generate_circular_path(center, point1, point2, num_circles=1):
    """
    Generate targets for concentric circles around a center point based on the first two points on the circle.

    Args:
        center (robomath.Mat): Center transformation matrix of the circle.
        point1 (robomath.Mat): First point on the circle, used to define radius and plane.
        point2 (robomath.Mat): Second point on the circle, used to define plane orientation.
        num_circles (int): Number of concentric circles to generate.

    Returns:
        list: List of transformation matrices for the targets around the custom-oriented circles.
    """
    # Convert center, point1, and point2 positions to numpy arrays for easy calculations
    center_pos = np.array(center.Pos())
    point1_pos = np.array(point1.Pos())
    point2_pos = np.array(point2.Pos())

    # Calculate the radius as the distance between the center and the first point
    radius = np.linalg.norm(point1_pos - center_pos)

    # Define two vectors in the plane of the circle
    vec1 = (point1_pos - center_pos) / radius  # Unit vector from center to first point
    vec2 = (point2_pos - center_pos)           # Vector from center to second point
    vec2 = vec2 - np.dot(vec2, vec1) * vec1    # Remove any component along vec1 to make vec2 orthogonal
    vec2 = vec2 / np.linalg.norm(vec2)         # Normalize vec2 to make it a unit vector

    # List to store all target points for all circles
    all_targets = [center]

    # Generate concentric circles
    for i in range(num_circles):
        current_radius = (i + 1) * radius
        circle_targets = []

        # Generate the 4 points around the circle
        angles = [0, np.pi / 2, np.pi, 3 * np.pi / 2]  # 0°, 90°, 180°, 270°
        for angle in angles:
            offset = current_radius * (np.cos(angle) * vec1 + np.sin(angle) * vec2)
            new_point = copy.deepcopy(center)
            new_point.setPos(center_pos + offset)
            circle_targets.append(new_point)

        # Close the circle by adding the first point at the end
        circle_targets.append(circle_targets[0])
        
        # Add the current circle's targets to the overall list
        all_targets.extend(circle_targets)

    return all_targets

def run_circular_weld(center, point1, point2, num_circles=1, speed=SLOW, myblend=0.0):
    """
    Generate and run a circular weld path around a center point.

    Args:
        center (robomath.Mat): Center transformation matrix for the circular path.
        point1 (robomath.Mat): First point on the circle, used to define radius and plane.
        point2 (robomath.Mat): Second point on the circle, used to define plane orientation.
        num_circles (int): Number of concentric circles to generate.
        speed: Movement speed for the robot.
        myblend (float): blend value between targets.
    """
    # Generate circular targets using the provided center, point1, and point2
    circular_targets = generate_circular_path(
        center, point1, point2, num_circles=num_circles
    )

    total_targets = len(circular_targets)

    # Run through the generated circular targets
    for i, t in enumerate(circular_targets):
        if i == 0:
            robot.nos_MoveL(speed, t, blend=0)
            Laser(1)  # Start welding
        elif i == total_targets - 1:
            robot.nos_MoveL(speed, t, blend=0)
        else:
            robot.nos_MoveL(speed, t, blend=myblend)

    # Stop welding after the circular path is completed
    Laser(0)

def run_linear_sleep_weld(point1, point2, delay=0.33, speed=SLOWAF):
    """ Simple weld from point1 to point2 with a sleep after turning on the laser """
    robot.nos_MoveL(speed, point1)
    Laser(1)
    AddSleep(delay)
    robot.nos_MoveL(speed, point2)
    Laser(0)








