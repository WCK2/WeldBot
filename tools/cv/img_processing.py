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


#~ visualizations
def rgbd_imshow(**kwargs):
    num_images = len(kwargs)
    num_rows = (num_images+1)//2
    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5*num_rows))

    for i, (var_name, var_value) in enumerate(kwargs.items()):
        row_idx = i // 2
        col_idx = i % 2
        if num_rows > 1: ax = axes[row_idx, col_idx]
        else: ax = axes[col_idx]
        
        cb = ax.imshow(var_value)
        plt.colorbar(cb, ax = ax)
        ax.set_title(var_name)
        ax.axis('off')
    
    mngr = plt.get_current_fig_manager()
    # mngr.window.wm_geometry('+0+0')
    try:
        mngr.window.setGeometry(0, 0, fig.get_figwidth() * 100, fig.get_figheight() * 100)
    except AttributeError:
        pass  # Ignore if setGeometry isn't available (e.g., on non-GUI backends)

    plt.tight_layout()
    plt.show()

def cv2_show(img, title: str='Image'):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



