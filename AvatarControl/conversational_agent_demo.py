# This script expects object available in UE environment of type
# AAirSimCharater
# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode
from __future__ import print_function
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path
import setup_path 
import airsim
import random
import pprint
import os
import time
import pyaudio  
import argparse

parser = argparse.ArgumentParser(description='agent_phoneme_style.py')
parser.add_argument('-audio', type=str, default='',
                      help='Audio path')
parser.add_argument('-level', type=int, default=1,
                      help='Loudness level')

opt = parser.parse_args()

client = airsim.VehicleClient()
client.confirmConnection()

phoneme_dict = {}
phoneme_dict = {
         'AA' : 'Phoneme_a-e',
         'AE' : 'Phoneme_a-e',
         'AY': 'Phoneme_a-e',
         'EY' : 'Phoneme_a-e',
         'AH' : 'Phoneme_a-e',
         'B' : 'Phoneme_b',
         'D' : 'Phoneme_d',
         'DH' :'Phoneme_d',
         'S' :'Phoneme_d',
         'IY' : 'Phoneme_ee',
         'JH' : 'Phoneme_ngnk',
         'Y'  : 'Phoneme_ee',
         'EH' : 'Phoneme_eh',
         'ER' : 'Phoneme_ar',
         'R' : 'Phoneme_ar',
         'F' : 'Phoneme_f',
         'V' : 'Phoneme_f',
         'W' : 'Phoneme_f',
         'G' : 'Phoneme_g',
         'HH' : 'Phoneme_h',
         'IH' : 'Phoneme_i',
         'K' : 'Phoneme_k',
         'L' : 'Phoneme_l',
         'M' : 'Phoneme_m',
         'P' : 'Phoneme_m',
         'N' : 'Phoneme_n',
         'CH' : 'Phoneme_ngnk',
         'SH' : 'Phoneme_ngnk',
         'NG' : 'Phoneme_ngnk',
         'T' : 'Phoneme_ngnk',
         'TH' : 'Phoneme_ngnk',
         'Z' : 'Phoneme_d',
         'ZH' : 'Phoneme_d',
         'AO' : 'Phoneme_oh',
         'AW' : 'Phoneme_oh',
         'OW' : 'Phoneme_ooo',
         'UH' : 'Phoneme_ooo',
         'UW' : 'Phoneme_ooo',
         'OY' : 'Phoneme_or',
         'SIL' : 'Phoneme_m',
        
    }


def reset_pose():
    presets = { 'FACS_10': facs_value[7], 'FACS_11': facs_value[8],
               'FACS_12' : facs_value[9],  'FACS_13': facs_value[10], 'FACS_14': facs_value[11],
               'FACS_15' : facs_value[12],  'FACS_16': facs_value[13], 'FACS_17': facs_value[14],
               'FACS_18' : facs_value[15],  'FACS_20': facs_value[16], 'FACS_22': facs_value[17],
               'FACS_23' : facs_value[18],  'FACS_24': facs_value[19], 'FACS_25': facs_value[20],
               'FACS_26' : facs_value[21],  'FACS_27': facs_value[22], 'FACS_28': facs_value[23],
                'Phoneme_a-e' :0, 'Phoneme_ar':0, 'Phoneme_b' :0, 'Phoneme_d' :0, 'Phoneme_ee' :0, 'Phoneme_eh' :0, 'Phoneme_er' :0, ' Phoneme_f' : 0,
                'Phoneme_g' :0, 'Phoneme_h' :0, 'Phoneme_i' : 0, 'Phoneme_k' :0, 'Phoneme_l' :0, 'Phoneme_m' :0, 'Phoneme_n' :0, 'Phoneme_ngnk' : 0,
                'Phoneme_oh' :0, 'Phoneme_oo' :0, 'Phoneme_ooo' :0, 'Phoneme_or' :0}
    client.simCharSetFacePresets(presets)

# predict phoneme from audio
model_path = get_model_path()
data_path = get_data_path()

AUDIO=os.path.join(data_path, opt.audio)

config = {
    'samprate' : 16000,
    'allphone' :  os.path.join(model_path, 'en-us-phone.lm.bin'),
    'remove_silence':False
}


ps = Pocketsphinx(**config)
ps.decode(
    audio_file=AUDIO,
    buffer_size=1024,
    no_search=False,
    full_utt=False
)

#define stream chunk   
chunk = 1024

#open the audio files (bytes)  
f = open(opt.audio,"rb")  


#instantiate PyAudio  
p = pyaudio.PyAudio()  

#open stream  
stream = p.open(format = 8,  
                channels = 1,  
                rate = 16000,  
                output = True)


#read data  
data = f.read(chunk*2)

frames = []
phones = {}
phoneme_pred = ps.segments(detailed=True)

fps = 100 
for idx,s in enumerate(phoneme_pred):
    if (idx < len(phoneme_pred)-1):
        phones[phoneme_pred[idx+1][2]/fps] = phoneme_pred[idx][0]
    else:
        phones[phoneme_pred[idx][3]/fps] = phoneme_pred[idx][0]

mouth_list = []
pre_mouth_shape = 'M'

#lip sync style intensity variation
if (opt.level == 0):
    intensity = 0.2
elif (opt.level == 1):
    intensity = 0.3
elif (opt.level == 2):
    intensity = 0.4
elif (opt.level == 3):
    intensity = 0.5
else:
    intensity = 0.6


facs_value = [0]*24

reset_pose()

#play stream  
while data:

    if (len(frames)==0):
        stream.write(data[30:])
    else:
        stream.write(data)

    data = f.read(chunk*2)
    frames.append(data)

    checkpoint = round(len(frames)*chunk/16000, 2)

    nearest = min(phones.keys(), key=lambda k: abs(k-checkpoint))
    nearest_idx = sorted(list(phones)).index(nearest)
    next_index = nearest_idx

    if (nearest < checkpoint and nearest_idx < len(phones)-1):
        nearest_idx = nearest_idx + 1
    if (next_index < len(phones)-2):
            next_index = nearest_idx + 1   
        
        
    mouth_shape = phones[sorted(list(phones))[nearest_idx]]
    idx = len(frames)*2 + len(frames)
    

    if (mouth_shape not in phoneme_dict.keys()):
        mouth_shape = pre_mouth_shape
        
        
    if (len(frames)%2 ==0):
        mouth_shape = pre_mouth_shape
    
    next_mouth_shape = phones[sorted(list(phones))[next_index]]

    if (next_mouth_shape not in phoneme_dict.keys()):
        next_mouth_shape = pre_mouth_shape
        
    mouth_list.append(pre_mouth_shape)
    mouth_list.append(mouth_shape)
    mouth_list.append(next_mouth_shape)

    if (len(frames) ==1):
        presets = {phoneme_dict[mouth_list[1]]:intensity}
    elif (len(frames)%2 !=0):
        presets = {phoneme_dict[mouth_list[idx-3]]:0.1, phoneme_dict[mouth_list[idx-2]]:intensity}
    elif (mouth_shape == pre_mouth_shape):
        presets = {phoneme_dict[mouth_list[idx-6]]:0, phoneme_dict[mouth_list[idx-1]]:0.1, phoneme_dict[mouth_list[idx-2]]:intensity}

   
    client.simCharSetFacePresets(presets)

    pre_mouth_shape = mouth_shape

reset_pose()  

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()   


