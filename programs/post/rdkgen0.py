#!/usr/bin/python
# Generated: December 19, 2024 -- 10:59:53 

from header0 import *


#=================================================
# Laser_Elite
#=================================================
def Laser_Elite():
    print("running Laser_Elite")
    # INITIALIZATION
    robot.set_tool([3.21601, -15.09436, 355.59596, -179.97628, -0.43837, 1.44147])
    robot.set_frame([-705.9324, 25.69165, 175.53272, 1.31001, 0.54002, 87.72001])
    # LockTab
    robot.set_frame([-705.9324, 25.69165, 175.53272, 1.31001, 0.54002, 87.72001])
    robot.set_tool([3.21601, -15.09436, 355.59596, -179.97628, -0.43837, 1.44147])
    # LockTab - loop 0
    robot.set_frame([-705.932,25.6917,175.533,1.31001,0.540021,87.72])
    robot.set_tool([3.21601,-15.0944,355.596,-179.976,-0.43837399999999993,1.44147])
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    robot.movel_joints(joints=[-143.292,65.2429,-71.1352,55.6152,65.8504,52.1579],speed=250.0,accel=125.0,blend=14.0)
    robot.movel_joints(joints=[-145.177,68.9255,-81.4254,62.8891,64.6404,50.5669],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-145.462,69.385,-82.7979,63.9066,64.4592,50.3239],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-145.38,69.3171,-82.5437,63.6904,64.5107,50.3932],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-145.547,69.2468,-82.6075,63.8858,64.405,50.2511],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-145.543,69.4522,-83.0512,64.1227,64.4075,50.2544],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-145.376,69.5228,-82.9875,63.9269,64.5135,50.397],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-145.38,69.3171,-82.5437,63.6904,64.5107,50.3932],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-143.218,65.1462,-70.8395,55.3909,65.8985,52.22],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-153.019,57.8672,-59.2621,47.5031,76.567,63.6844],speed=250.0,accel=125.0,blend=7.475)
    robot.movel_joints(joints=[-154.017,62.5971,-71.4539,55.1415,75.8764,62.943],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-154.168,63.1824,-73.0423,56.1723,75.7721,62.8304],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-154.085,63.121,-72.7955,55.9716,75.8295,62.8923],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-154.23,63.013,-72.7888,56.0995,75.7289,62.7837],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-154.251,63.243,-73.2881,56.3728,75.7146,62.7683],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-154.105,63.3513,-73.2948,56.2443,75.8154,62.8772],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-154.085,63.121,-72.7955,55.9716,75.8295,62.8923],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-152.942,57.7708,-58.9586,47.2827,76.6207,63.7417],speed=250.0,accel=125.0,blend=0.0)
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    # LockTab - loop 1
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    robot.movel_joints(joints=[-154.103,78.2813,-89.3546,65.2398,59.1695,42.5654],speed=250.0,accel=125.0,blend=14.0)
    robot.movel_joints(joints=[-156.866,81.0215,-97.9357,72.4725,57.5789,39.9117],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-157.283,81.359,-99.1047,73.524,57.3434,39.5026],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-157.176,81.3223,-98.8928,73.2923,57.4035,39.6076],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-157.354,81.199,-98.9196,73.5362,57.3038,39.4336],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-157.39,81.395,-99.316,73.7562,57.2832,39.3974],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-157.213,81.5189,-99.2892,73.5112,57.3831,39.572],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-157.176,81.3223,-98.8928,73.2923,57.4035,39.6076],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-154.005,78.2204,-89.1181,65.0168,59.2269,42.6578],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-164.218,69.1672,-76.3862,55.8919,68.9701,55.0601],speed=250.0,accel=125.0,blend=7.961)
    robot.movel_joints(joints=[-165.955,72.8012,-86.3963,62.7866,67.8291,53.6518],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-166.219,73.2613,-87.7433,63.7552,67.657,53.4361],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-166.117,73.2377,-87.5508,63.5547,67.7232,53.5191],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-166.26,73.0822,-87.5055,63.7093,67.63,53.4022],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-166.32,73.2842,-87.935,63.9557,67.5908,53.3529],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-166.177,73.4402,-87.9803,63.8004,67.6841,53.4701],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-166.117,73.2377,-87.5508,63.5547,67.7232,53.5191],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-164.124,69.1193,-76.1633,55.6898,69.0324,55.1358],speed=250.0,accel=125.0,blend=0.0)
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    # LockTab - loop 2
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    robot.movel_joints(joints=[-168.074,88.3315,-102.276,76.335,51.7779,28.1379],speed=250.0,accel=125.0,blend=14.0)
    robot.movel_joints(joints=[-171.889,90.1368,-109.777,84.8098,50.0914,23.7296],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-172.461,90.3297,-110.803,86.0797,49.8531,23.0504],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-172.329,90.3318,-110.623,85.7965,49.9078,23.2078],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-172.494,90.1374,-110.611,86.1052,49.8397,23.0117],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-172.594,90.3266,-110.982,86.3635,49.7986,22.8926],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-172.429,90.5221,-110.994,86.0532,49.8666,23.0894],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-172.329,90.3318,-110.623,85.7965,49.9078,23.2078],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-167.951,88.3043,-102.076,76.0764,51.8351,28.2766],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-177.007,76.1424,-86.4704,63.6707,60.8966,44.0931],speed=250.0,accel=125.0,blend=7.961)
    robot.movel_joints(joints=[-179.556,79.0149,-95.2979,70.8085,59.3957,41.7173],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-179.941,79.3708,-96.4977,71.839,59.1726,41.3519],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-179.828,79.3837,-96.345,71.6182,59.2382,41.4597],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-179.948,79.1776,-96.2607,71.7985,59.1687,41.3456],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-180.055,79.3572,-96.6497,72.0601,59.107,41.2438],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-179.934,79.5641,-96.734,71.8788,59.1764,41.3582],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-179.828,79.3837,-96.345,71.6182,59.2382,41.4597],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-176.9,76.1312,-86.2944,63.4583,60.9603,44.1909],speed=250.0,accel=125.0,blend=0.0)
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    # LockTab - loop 3
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    robot.movel_joints(joints=[-184.933,94.196,-110.908,93.0659,45.7562,7.11507],speed=250.0,accel=125.0,blend=14.0)
    robot.movel_joints(joints=[-189.563,94.3357,-117.214,103.727,44.8401,0.728457],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-190.243,94.2601,-118.057,105.323,44.7359,-0.224891],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-190.101,94.3258,-117.921,104.979,44.757,-0.0256094],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-190.214,94.0479,-117.851,105.301,44.7401,-0.185173],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-190.384,94.1933,-118.193,105.667,44.7152,-0.424268],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-190.271,94.4728,-118.263,105.344,44.7318,-0.264902],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-190.101,94.3258,-117.921,104.979,44.757,-0.0256094],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-184.795,94.2207,-110.745,92.7485,45.7889,7.30214],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-190.924,79.1445,-91.6488,73.4533,53.3036,30.1688],speed=250.0,accel=125.0,blend=7.961)
    robot.movel_joints(joints=[-194.133,81.0683,-99.4755,81.5278,51.7981,26.5984],speed=250.0,accel=125.0,blend=0.0)
    robot.movel_joints(joints=[-194.612,81.2811,-100.537,82.7144,51.5827,26.0528],speed=10.0,accel=133.333,blend=0.0)
    Laser(1)
    robot.movel_joints(joints=[-194.499,81.3361,-100.425,82.4675,51.6333,26.1817],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-194.577,81.083,-100.295,82.6459,51.5985,26.0931],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-194.725,81.2253,-100.648,82.9614,51.5323,25.9238],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-194.648,81.4793,-100.778,82.7823,51.5669,26.0123],speed=10.0,accel=133.333,blend=0.375)
    robot.movel_joints(joints=[-194.499,81.3361,-100.425,82.4675,51.6333,26.1817],speed=10.0,accel=133.333,blend=0.0)
    Laser(0)
    robot.movel_joints(joints=[-190.815,79.1725,-91.5143,73.2199,53.3565,30.2874],speed=250.0,accel=125.0,blend=0.0)
    robot.movej(joints=[-194.568,99.6468,-95.7787,96.6791,92.0729,-13.2886],speed=90.0,accel=60.0,blend=0.0)
    # DONE


#=================================================
# Main program select
#=================================================
def ProgSel(p):
    if type(p)==str: p=p.strip()
    if p==999: pass
    elif p==2: Laser_Elite()
    else: return prog_ext(p)

#====================== END ======================
# Generated: December 19, 2024 -- 10:59:56 