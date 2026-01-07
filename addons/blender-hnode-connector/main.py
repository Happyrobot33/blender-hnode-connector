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

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min

def getPositionAsDMX(loc, range, bytesPerAxis=1):
    xscale = int(scale_number(loc.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(loc.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(loc.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    return xbytes + ybytes + zbytes

def getRotationAsDMX(rot, range, bytesPerAxis=1):
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    return xbytes + ybytes + zbytes

def getColorAsDMX(color):
    r = int(scale_number(color[0], 0,255,0,1))
    g = int(scale_number(color[1], 0,255,0,1))
    b = int(scale_number(color[2], 0,255,0,1))
    return bytes([r, g, b])

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
    
        
def append_function_unique(fn_list, fn):
    """ Appending 'fn' to 'fn_list',
        Remove any functions from with a matching name & module.
    """
    fn_name = fn.__name__
    fn_module = fn.__module__
    for i in range(len(fn_list) - 1, -1, -1):
        if fn_list[i].__name__ == fn_name and fn_list[i].__module__ == fn_module:
            del fn_list[i]
    fn_list.append(fn)
    
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
