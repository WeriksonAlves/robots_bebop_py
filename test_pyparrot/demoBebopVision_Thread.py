"""
Demo of the Bebop ffmpeg based vision code (basically flies around and saves out photos as it flies)

Author: Amy McGovern
"""
from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision
from Model import Model
import threading
import cv2
import time
import numpy as np

import torch

from depth_anything_v2.dpt import DepthAnythingV2

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

encoder = 'vits' # or 'vits', 'vitb', 'vitg'

model = DepthAnythingV2(**model_configs[encoder])
model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
model = model.to(DEVICE).eval()






isAlive = False

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision
        self.depth = np.zeros((480, 640), dtype='uint8')
        self.img = None
        self.frame_lock = threading.Lock()
        self._initialize_threads()

    def save_pictures(self, args):
        #print("saving picture")
        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            #cv2.imwrite(filename, img)
            self.index +=1

    def my_imshow(self, args):
        with self.frame_lock:
            img = self.vision.get_latest_valid_picture()
            if img is not None:
                self.img = img.copy()

        if self.img is not None:
            cv2.imshow('Stream_Bebop2', self.img)
            cv2.imshow('Depth_Bebop2', self.depth)
            cv2.waitKey(1)

    def _initialize_threads(self) -> None:
        print('Começou-222222222222222222222222222222222222222222222222222222')
        self.depth_thread = threading.Thread(target=self.process_depth)
        self.depth_thread.daemon = True
        self.depth_thread.start()
    
    def process_depth(self):
        print('Começou-111111111111111111111111111111111111111111111111111111')
        while True:
            with self.frame_lock:
                if self.img is not None:
                    img_copy = self.img.copy()
            if img_copy is not None:
                self.depth = model.infer_image(img_copy)
            print('OI')



# make my bebop object
bebop = Bebop()

# connect to the bebop
success = bebop.connect(100)

if (success):
    # start up the video
    bebopVision = DroneVision(bebop, Model.BEBOP, buffer_size=10)

    userVision = UserVision(bebopVision)
    bebopVision.set_user_callback_function(userVision.my_imshow, user_callback_args=None)
    success = bebopVision.open_video()
    
    if (success):
        
        print("Vision successfully started!")
        #removed the user call to this function (it now happens in open_video())
        #bebopVision.start_video_buffering()

        # skipping actually flying for safety purposes indoors - if you want
        # different pictures, move the bebop around by hand
        print("Fly me around by hand!")
        bebop.smart_sleep(5)
        
        
        
        print("Moving the camera using velocity")
        bebop.pan_tilt_camera_velocity(pan_velocity=0, tilt_velocity=0, duration=4)
        bebop.smart_sleep(25)
        print("Finishing demo and stopping vision")
        bebopVision.close_video()

    # disconnect nicely so we don't need a reboot
    bebop.disconnect()
else:
    print("Error connecting to bebop.  Retry")
