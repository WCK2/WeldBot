import os
import numpy as np
from rdk.nos.willrdk import *


SAVE_DIR = os.getcwd() + '/tools/charuco/'
SLOW = 1
GEN = 1
output_lines = []

# 11/1 210pm: ['C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-33/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-39/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-44/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-47/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-51/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-06-57/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-03/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-18/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-26/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-32/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-37/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-42/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-47/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-07-53/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-05/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-10/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-20/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-28/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-34/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-40/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-44/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-49/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-08-54/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-06/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-09/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-17/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-23/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-29/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-36/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-42/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-46/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-52/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-09-58/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-02/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-15/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-22/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-29/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-35/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-41/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-45/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-50/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-53/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-10-58/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-11-04/']
# 11/1 240pm: ['C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-05/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-10/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-15/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-21/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-23/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-28/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-30/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-35/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-40/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-48/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-52/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-34-58/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-04/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-11/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-16/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-20/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-24/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-30/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-37/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-42/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-46/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-52/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-35-59/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-03/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-10/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-14/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-19/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-27/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-33/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-38/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-44/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-50/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-36-56/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-03/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-08/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-14/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-19/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-26/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-32/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-38/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-44/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-51/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-37-58/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-38-05/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-38-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-38-21/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-01_14-38-28/']
#   camera tcp results: [-30.3775588, -104.34399427, 75.91455461, -16.94425204, -0.24361381, 1.30819848]

# 11/12 840am: ['C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-19/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-24/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-30/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-36/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-44/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-48/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-44-54/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-06/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-22/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-29/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-34/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-39/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-45/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-49/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-45-55/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-01/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-21/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-24/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-30/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-37/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-42/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-48/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-46-52/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-14/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-16/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-29/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-41/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-47/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-47-55/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-48-03/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-48-06/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-48-13/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-48-19/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_08-48-27/']
#   camera tcp results: [-30.2533408, -108.52412805, 74.69251914, -17.35379716, -0.39418238, 1.26704269]
# 11/12 930am: ['C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-05/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-06/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-09/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-12/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-17/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-19/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-23/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-25/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-28/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-31/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-35/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-38/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-41/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-43/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-45/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-49/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-53/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-55/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-28-57/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-00/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-05/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-09/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-11/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-15/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-20/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-24/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-28/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-31/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-35/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-39/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-43/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-47/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-51/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-53/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-56/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-29-59/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-02/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-07/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-12/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-17/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-21/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-24/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-28/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-31/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-34/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-38/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-43/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-46/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-50/', 'C:\\Users\\william.cowles\\Desktop\\repos\\PickPlaceWeldBot/assets/data/d435_2024-11-12_09-30-53/']
#   camera tcp results: [-30.10168841, -105.53584827, 73.95309177, -16.93603562, -0.17750193, 1.40414367]


#~ gen helpers
def add(line):
    output_lines.append(line)

def add_multiple(*lines):
    for line in lines:
        if "\n" in line:
            # Split multiline strings into individual lines
            output_lines.extend(line.strip().splitlines())
        else:
            output_lines.append(line)

def save_script(filepath:str = SAVE_DIR, filename:str = 'run_targets.py'):
    with open(filepath + filename, 'w') as file:
        # Write all lines with newline characters
        file.write("# Generated RoboDK interaction script\n\n")
        file.write("\n".join(output_lines))

def add_header():
    add_multiple(
"""
import os
import time
import json
import numpy as np
import pickle
from tools.devices.D435 import D435
from jaka.nos.jakabot import *

#~ Initialization
robot_ip = "192.168.69.50"
robot = jakabot(robot_ip)
robot.init()

camera = D435()

robot.set_frame([0,0,0,0,0,0])
robot.set_tool([0,0,0,0,0,0])
"""
    )

def add_move_through_targets():
    pass



#~ gen
def test_wout_manual_tool():
    #? try to clean last
    old_tool = rdk.Item('temp_rdk_gen_tool')
    if old_tool.Valid(): old_tool.Delete()

    #? setup
    z_offset = -400

    robot = rdk.Item('jaka12_0')
    workpiece_frame = rdk.Item('Workpiece CALE')
    retracted_holder = workpiece_frame.findChild('Retracted Holder')
    retracted_frame = retracted_holder.findChild('Retracted Frame')
    _tool = rdk.Item('camera tcp')
    robot.setSlowSpeeds(20, 50, 25, 10)
    # robot.nos_MoveJ(SLOW, rdk.Item('joints_1').Joints())

    _tool.Copy(False)
    tool_copy = _tool.Parent().Paste()
    tool_copy.setName('temp_rdk_gen_tool')
    tool_copy.setVisible(False)
    tool_pose = tool_copy.PoseTool()

    tool_pose = tool_pose * rotx(np.deg2rad(180))
    tool_pose = tool_pose * transl(0, 0, z_offset)
    tool_copy.setPoseTool(tool_pose)

    robot.setPoseFrame(retracted_frame)
    pose = pose_2_xyzrpw(robot.PoseFrame())
    rounded_pose = [round(val,5) for val in pose]
    # if GEN: add(f'robot.set_frame({rounded_pose})')

    robot.setPoseTool(tool_copy)
    tcp = pose_2_xyzrpw(robot.PoseTool())
    rounded_tcp = [round(val,5) for val in tcp]
    # if GEN: add(f'robot.set_tool({rounded_tcp})')

    #? moves
    # rx_offset = 30
    rx_min = -35
    rx_max = 20

    ry_offset = 25
    
    rz_min = -45
    rz_max = 35
    
    rows = 5
    cols = 5

    # rx_values = np.linspace(-rx_offset, rx_offset, rows).reshape(rows, 1)
    rx_values = np.linspace(rx_min, rx_max, rows).reshape(rows, 1)
    ry_values = np.linspace(-ry_offset, ry_offset, cols).reshape(1, cols)
    # rz_values = np.zeros((rows, cols))
    rz_values = np.random.randint(rz_min, rz_max+1, size=(rows, cols))

    angles = np.zeros((rows, cols, 3))
    angles[:, :, 0] = rx_values
    angles[:, :, 1] = ry_values
    angles[:, :, 2] = rz_values

    t = Pose()
    joint_targets = []
    for i in range(angles.shape[0]):
        for j in range(angles.shape[1]):
            rx, ry, rz = angles[i, j]
            robot.nos_MoveL(SLOW, RelFrame(RelFrame(RelFrame(t, rx=rx), ry=ry), rz=0))
            joints = list(robot.Joints())[0]
            joint_targets.append([round(num, 4) for num in joints])
            
            robot.nos_MoveL(SLOW, RelFrame(RelFrame(RelFrame(t, rx=rx), ry=ry), rz=rz))
            joints = list(robot.Joints())[0]
            joint_targets.append([round(num, 4) for num in joints])

    add(f'\n\njoint_targets = {joint_targets}\n')

    add_multiple(
"""
folders = []
for c, jtar in enumerate(joint_targets):
    robot.movej(joints=jtar, speed=35.0, accel=15)
    robot.waitmove()

    joints = robot.get_joints()
    pose = robot.get_tcp_pose()
    rgbd_data = camera.get_data(save=True)
    path_with_timestamp = rgbd_data.path_with_timestamp
    folders.append(path_with_timestamp)
    
    data_to_save = {
        'joints': joints,
        'pose': pose,
        'path_with_timestamp': path_with_timestamp
    }
    print(f'data_to_save: {data_to_save}')

    filepath = path_with_timestamp + 'handeye_1.pkl'
    with open(filepath, 'wb') as f:
        pickle.dump(data_to_save, f)

    time.sleep(0.5)

print(f'folders: {folders}')
"""
    )








if __name__ == '__main__':
    add_header()
    test_wout_manual_tool()
    save_script()




