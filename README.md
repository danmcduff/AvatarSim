# AvatarSim

This repository contains an avatar environment that can be programaticly controlled from Python via AirSim (https://github.com/Microsoft/AirSim).

## Executable:

The executable (avatarsim.exe) includes the avatar envrionment.  It is compiles for Windows 10 and runs best Nvidia GTX 1080i GPU or higher.  An AirSim settings file is also included that 

![Alt text](imgs/avatar.png?raw=true "Avatar") <!-- .element height="50%" width="50%" -->

## Avatar Control Scripts:

Python scripts are included in the repository that illustrate how to control the avatar's facial pose and expressions in order to generate face images for testing face detection algorithms. Parameters that can be controlled programmaticly are: skin tone, age, head pose, head position, facial actions based on the Facial Action Coding System (FACS). 

```python
import airsim

client = airsim.VehicleClient()
client.confirmConnection()
```

### Head Pose and Position:
Pitch, yaw and roll of the head can be set in radians.


```python
# Set Head Position:
q = airsim.to_quaternion(0, math.radians(opt.roll), math.radians(opt.yaw))
client.simCharSetHeadRotation(q)                # Set the head rotation.
```




The positions of "bones" can be set
![Alt text](imgs/bone_positions.png?raw=true "Avatar" | width=200)

```python
# Set Bone Position:
EyeLid = airsim.Pose()
EyeLid.position = airsim.Vector3r(0, 0, 0)
EyeLid.orientation = airsim.to_quaternion(-1.5, 0, 0)
bone_setting = {'LUpperEyelid' : EyeLid}    
client.simCharSetBonePoses(bone_setting)
```

Skin Tone and Age:

```python
# Set Skin Tone:
client.simCharSetSkinDarkness(0.2)              # Set skin tone.
```

Facial Coding:

```python
FACS_values = {'FACS_01' : 0.0,  'FACS_02': 1.0, 'FACS_04': 0.0,
               'FACS_05' : 0.0,  'FACS_06': 0.0, 'FACS_07': 0.0,
               'FACS_09' : 0.0,  'FACS_10': 0.0, 'FACS_11': 0.0,
               'FACS_12' : 0.0,  'FACS_13': 0.0, 'FACS_14': 0.0,
               'FACS_15' : 0.0,  'FACS_16': 0.0, 'FACS_17': 0.0,
               'FACS_18' : 0.0,  'FACS_20': 0.0, 'FACS_22': 0.0,
               'FACS_23' : 0.0,  'FACS_24': 0.0, 'FACS_25': 0.0,
               'FACS_26' : 0.0,  'FACS_27': 0.0, 'FACS_28': 0.0}

client.simCharSetFacePresets(FACS_values)
```


## Commerical Face API Scripts:

We include example python scripts for a set of commercial face detection APIs. These scripts show how to interrogate the APIs with images generated from the avatar environment. 
