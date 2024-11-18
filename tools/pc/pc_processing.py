import os
import copy
import time
import cv2
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.backend_bases import PickEvent
from matplotlib.widgets import Button, TextBox
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d


#~ 
def pointcloud_from_rgbd(vertices, colors, compute_normals=False, show=False):
    vertices = vertices.reshape(-1, 3)
    colors = colors / 255
    colors = colors.reshape(-1, 3)

    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(vertices)
    pc.colors = o3d.utility.Vector3dVector(colors)
    pc.normals = o3d.utility.Vector3dVector(np.zeros(np.asarray(pc.points).shape))
    # pc.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    # pc.transform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    pc.orient_normals_towards_camera_location(camera_location = np.array([0,0,0]))
    if compute_normals:
        pc.estimate_normals(fast_normal_computation = True) # time consuming
        # pc.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=15, max_nn=30))

    if show: o3d.visualization.draw_geometries([pc], point_show_normal = False)
    return pc


#~ filters
def rgbd_depth_filter(rgbd_data, min=None, max=None):
    if min is None: min = np.min(rgbd_data.depth)
    if max is None: max = np.max(rgbd_data.depth)

    filtered_image = np.full(rgbd_data.depth.shape, 127, dtype=np.uint8)

    filtered_image[rgbd_data.depth < min] = 0
    filtered_image[rgbd_data.depth > max] = 255

    rgbd_data.depth[rgbd_data.depth < min] = 0
    rgbd_data.depth[rgbd_data.depth > max] = 0

    rgbd_data.vertices[rgbd_data.vertices[:, :, 2] < min] = [0, 0, 0]
    rgbd_data.vertices[rgbd_data.vertices[:, :, 2] > max] = [0, 0, 0]

    return rgbd_data, filtered_image

def rgbd_bounding_box_filter(rgbd_data, x1, y1, x2, y2):
    """
    Filters vertices and depth data in rgbd_data based on a bounding box.

    Parameters:
    - rgbd_data: The class containing depth and vertices data.
    - x1, y1: Coordinates of the top-left corner of the bounding box.
    - x2, y2: Coordinates of the bottom-right corner of the bounding box.

    Returns:
    - rgbd_data: Filtered rgbd_data with vertices and depth outside the bounding box set to 0.
    """
    # Initialize a mask for the bounding box
    mask = np.zeros_like(rgbd_data.depth, dtype=bool)
    mask[y1:y2, x1:x2] = True  # Set mask to true inside bounding box

    # Zero out vertices outside the bounding box
    rgbd_data.vertices[~mask] = [0, 0, 0]

    # Zero out depth values outside the bounding box
    rgbd_data.depth[~mask] = 0

    return rgbd_data


#~ visualizations
def visualization_view(pcs:list, point_show_normal=False):
    o3d.visualization.draw_geometries(pcs, point_show_normal=point_show_normal)

def visualization_interactive(pc, log=False):
    print(f' - Add points using [shift + left click]')
    print(f' - Remove points using [shift + right click]')
    print(f' - press "Q" to close the window')
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pc)
    vis.run()
    vis.destroy_window()

    indices = vis.get_picked_points()
    if log:
        print(f'locations clicked: {indices}')
        for i in indices:
            print(f'  index: {i}')
            print(f'    points: {pc.points[i]}')
            print(f'    normals: {pc.normals[i]}')

    return indices












