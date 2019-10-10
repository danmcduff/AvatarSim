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

q = airsim.to_quaternion(0, 0, 0)
client.simCharSetHeadRotation(q)


def get_new_time_to_perform_action():
  delay_minutes = (1 + random.random() * 1) 
  return time.time() + delay_minutes * 1

next_time_to_run = get_new_time_to_perform_action()

while True:
  if (time.time() >= next_time_to_run):
    up_eyes_blink = airsim.Pose()
    up_eyes_blink.position = airsim.Vector3r(0, 0, 0)
    up_eyes_blink.orientation = airsim.to_quaternion(-1.5, 0, 0)

    bone_setting = {'LUpperEyelid' : up_eyes_blink,  'RUpperEyelid': up_eyes_blink}
    client.simCharSetBonePoses(bone_setting)
    client.simCharResetBonePose('LUpperEyelid')
    client.simCharResetBonePose('RUpperEyelid')
    
    next_time_to_run = get_new_time_to_perform_action()


