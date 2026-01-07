# send string UDP packets to a specified IP and port
import socket
import sys
import random
import time
import base64
import bpy
from math import radians
import mathutils
from sbstudio.plugin.constants import Collections
from sbstudio.plugin.colors import get_color_of_drone

#dmx data dict
#key: channel number
#value: channel value
data_dict = {}

def gen_drone_data(start_channel):
    #get all the drones
    drones = Collections.find_drones(create=False).objects
    #do for each drone, keeping a index to offset channels
    for drone_index, drone in enumerate(drones):
        base_channel = drone_index * 9  #each drone gets 6 channels
        base_channel = base_channel + start_channel
        loc = drone.matrix_world.to_translation()
        #flip y
        loc.y *= -1
        loc.x, loc.y = loc.y, loc.x
        combined = getPositionAsDMX(loc, range=800, bytesPerAxis=2)
        #handle color
        color = get_color_of_drone(drone)
        combined += getColorAsDMX(color)
        #write them starting at channel 0
        for i in range(9):
            data_dict[i + base_channel] = combined[i]
            
def gen_truss_data(start_channel, object):
    if object == None:
        return
    base_channel = start_channel
    loc = object.matrix_world.to_translation()
    #loc.z *= -1
    loc.y, loc.x = loc.x, loc.y
    loc.y *= -1
    loc.y, loc.z = loc.z, loc.y
    combined = getPositionAsDMX(loc, range=50, bytesPerAxis=2)
    rot = object.matrix_world.to_quaternion()
    #works but flipped across Y??????
    unityrot = mathutils.Quaternion((rot.w, rot.x, rot.y, rot.z))
    eulrot = unityrot.to_euler("XYZ")
    combined += getRotationAsDMX(eulrot, range=radians(540 / 2), bytesPerAxis=2)
    #write them starting at channel 0
    for i in range(12):
        data_dict[i + base_channel] = combined[i]
    
def dostuff(scene):
    #needs truss position at 255 to work
    data_dict[5] = 255 #custom truss position
    data_dict[4] = 100 #truss speed
    data_dict[2802] = 255
    data_dict[2804] = 255
    for i in range(12 - 1):
        gen_truss_data(6 + (14 * i), bpy.data.objects.get("Truss " + str(1 + i)))
        
    gen_drone_data(2880)
    send()


# def register():
#     append_function_unique(bpy.app.handlers.frame_change_post, dostuff)
#     append_function_unique(bpy.app.handlers.depsgraph_update_post, dostuff)
    
# if __name__ == "__main__":
#     register()
#     dostuff(None
