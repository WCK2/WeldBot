from utils.config import *
from tools.devices.D435 import *
from tools.cv.img_processing import *
from tools.pc.pc_processing import *



fname = 'd435_2024-11-04_09-20-40'

rgbd_data = rgbd_read_data(fname, 'data_dict_1.pkl')
rgbd_data, _ = rgbd_depth_filter(rgbd_data, min=150, max=310)
rgbd_imshow(rgb=rgbd_data.colors, z=rgbd_data.vertices[:,:,2])


# pc = pointcloud_from_rgbd(rgbd_data.vertices, rgbd_data.colors, show=False)
# indices = visualization_interactive(pc, log=True)
# print(f'indices: {indices[0]}')
# print(f'positioin: {pc.points[indices[0]]}')



