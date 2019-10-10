# This script expects object available in UE environment of type
# AAirSimCharater
# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode
import setup_path 
import airsim
import pprint
import os
import time
import math
import argparse
import random

client = airsim.VehicleClient()
client.confirmConnection()

client.reset()

# reset head to neutral position
resets = airsim.to_quaternion(0, 0, 0)


length = 10000 # sets duration of the head movement

start_time = time.time()
elapsed_time = 0

while True:
    delay = random.uniform(1, 4)
    elapsed_time = time.time() - start_time
    number_of_steps = 20

    client.simCharSetHeadRotation(resets)

    current_pitch = client.simCharGetHeadRotation()['y_val'] # the y_val is definitely the pitch, which is what needs to be moved the most. Although I'm not sure what exactly z, w and x are, it doesn't matter since they need to be set to equally small values...
    current_roll = client.simCharGetHeadRotation()['x_val']
    current_yaw = client.simCharGetHeadRotation()['z_val']

    target_pitch = math.radians(random.random()*4) # pitch = nodding movement
    target_roll = math.radians(random.random()*2) # roll = horizontal movement of the head left and right
    target_yaw = math.radians(random.random()*2) # yaw = oblique movement of the head left and right

    step_pitch = (current_pitch - target_pitch)/number_of_steps
    step_roll = (current_roll - target_roll)/number_of_steps
    step_yaw = (current_yaw - target_yaw)/number_of_steps


    for i in range(number_of_steps):
        q = airsim.to_quaternion(current_pitch + step_pitch, current_roll + step_roll, current_yaw + step_yaw)
        client.simCharSetHeadRotation(q)
        current_pitch = current_pitch + step_pitch
        current_roll = current_roll + step_roll
        current_yaw = current_yaw + step_yaw
        time.sleep(0.05)
        #time.sleep(delay)



    for i in range(number_of_steps):
        q = airsim.to_quaternion(current_pitch - step_pitch, current_roll - step_roll, current_yaw - step_yaw)
        client.simCharSetHeadRotation(q)
        current_pitch = current_pitch - step_pitch
        current_roll = current_roll - step_roll
        current_yaw = current_yaw - step_yaw
        time.sleep(0.05)

    time.sleep(delay)


