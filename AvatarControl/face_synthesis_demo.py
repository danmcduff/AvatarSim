# This script expects object available in UE environment of type AAirSimCharater
# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

import setup_path 
import airsim
import pprint
import os
import time
import sys
import dlib
import cv2
from time import sleep
import numpy as np
import scipy.misc as misc
import scipy.ndimage as ndimage
import random

pp = pprint.PrettyPrinter(indent=4)

client = airsim.VehicleClient()
client.confirmConnection()

image_count = 1

pose = client.simGetVehiclePose()
initial_pose_x = pose.position.x_val
initial_pose_y = pose.position.y_val
initial_pose_z = pose.position.z_val

for imgs in range (1, 100, 1):

    pose.position.x_val = initial_pose_x + random.randrange(0, 10, 1)/40 - 0.15
    pose.position.y_val = initial_pose_y + random.randrange(0, 10, 1)/40 - 0.15
    pose.position.z_val = initial_pose_z + random.randrange(0, 10, 1)/40 - 0.15
    client.simSetVehiclePose(pose, True)

    # For skintone in range (1, 31, 5):
    skintone = random.randrange(1, 31, 5)
    client.simCharSetSkinDarkness(float(skintone)/10)

    # For age in range (1, 22, 10):
    age = random.randrange(1, 21, 5)
    client.simCharSetSkinAgeing(float(age)/10);

    # For pitch and yaw:
    pitch = random.randrange(-8, 8, 2)
    yaw = random.randrange(-12, 12, 2)
    q = airsim.to_quaternion(pitch/10.0, 0, yaw/10.0)
    client.simCharSetHeadRotation(q)

    for x in range(1): 
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene)])
