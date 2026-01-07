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
def send_udp_packet(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message, (ip, port))
        print(f"Sent message to {ip}:{port}")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        sock.close()
def generateMessage(data_dict):
    #standard is
    #short,byte for each channel
    bmessage = []
    #iterate over each channel in order
    for channel in sorted(data_dict.keys()):
        value = data_dict[channel]
        #now encode the channel as short
        bmessage += channel.to_bytes(2, byteorder='big')
        #now encode the value as byte
        bmessage += value.to_bytes(1, byteorder='big')
    return bytes(bmessage)
def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min
#dmx data dict
#key: channel number
#value: channel value
data_dict = {}

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
        
def send():
    target_ip = "127.0.0.1"
    target_port = 7000
    #generate X arbitrary channel data
    # for i in range(11800):
    #     if i not in data_dict:
    #         data_dict[i] = random.randint(0, 255)
    fragments = []
    fragmentation_size = 3070 #max size of a udp packet roughly
    #loop over every dict object, fragmenting if necessary
    #all we need to do is split the dictionary into smaller dictionaries
    for i in range(0, len(data_dict), fragmentation_size):
        fragment = dict(list(data_dict.items())[i:i+fragmentation_size])
        fragments.append(fragment)
    for fragment in fragments:
        message = generateMessage(fragment)
        #print first channel
        #print(message)
        send_udp_packet(target_ip, target_port, message)
        time.sleep(0.001)  # brief pause to avoid overwhelming the network
        
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
    
def register():
    append_function_unique(bpy.app.handlers.frame_change_post, dostuff)
    append_function_unique(bpy.app.handlers.depsgraph_update_post, dostuff)
    
if __name__ == "__main__":
    register()
    dostuff(None)
