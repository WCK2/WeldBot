from jaka.nos.jakabus import *
import math
import keyboard
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px


#~ Init
ip_jaka = '192.168.69.50'
jbus = JAKABUS(ip_jaka)
jbus.connect()


#~ Log
def log():
    x_positions = []
    y_positions = []
    z_positions = []
    total_velocities = []

    while True:
        vlist = jbus.get(jbus.reg_tcp_speed)
        vtotal = math.sqrt(vlist[0]**2 + vlist[1]**2 + vlist[2]**2)
        print(f'loop 1: {vtotal}')
        if vtotal > 0.001: break
        if keyboard.is_pressed('q'): break

    while True:
        plist = jbus.get(jbus.reg_tcp_position)
        vlist = jbus.get(jbus.reg_tcp_speed)
        vtotal = math.sqrt(vlist[0]**2 + vlist[1]**2 + vlist[2]**2)

        x_positions.append(plist[0])
        y_positions.append(plist[1])
        z_positions.append(plist[2])
        total_velocities.append(vtotal)
        # print(plist)
        # print(vlist)
        # print(vtotal)

        if vtotal < 0.001: break
        if keyboard.is_pressed('q'): break
        time.sleep(0.001)

    fig = px.scatter_3d(x=x_positions, y=y_positions, z=total_velocities,
                        labels={'x': 'X Position', 'y': 'Y Position', 'z': 'vtotal Speed'},
                        title='Robot Path and vtotal Speed')
    fig.show()




if __name__=="__main__":
    
    log()



