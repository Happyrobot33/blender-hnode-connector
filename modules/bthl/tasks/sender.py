import socket
import time
import bpy
from bthl.tasks.task import Task
import random
from bthl.api.dmxdata import dmx_buffer
from bthl.modal.sender_modal import UDPClientToggleModal

def send_udp_packet(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message, (ip, port))
        print(f"Sent message to {ip}:{port}")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        sock.close()

def generateMessage(dmx_buffer):
    #standard is
    #short,byte for each channel
    bmessage = []
    #iterate over each channel in order
    for channel in sorted(dmx_buffer.keys()):
        value = dmx_buffer[channel]
        #now encode the channel as short
        bmessage += channel.to_bytes(2, byteorder='big')
        #now encode the value as byte
        bmessage += value.to_bytes(1, byteorder='big')
    return bytes(bmessage)

def send(scene, depsgraph):
    #we should only send if the udp client is active
    if not UDPClientToggleModal.get_udp_client_state(bpy.context):
        return
    
    target_ip = "127.0.0.1"
    target_port = 7000
    #generate X arbitrary channel data
    # for i in range(11800):
    #     if i not in data_dict:
    #         data_dict[i] = random.randint(0, 255)
    for i in range(20):
        if i not in dmx_buffer:
            dmx_buffer[i] = random.randint(0, 255)
    fragments = []
    fragmentation_size = 3070 #max size of a udp packet roughly
    #loop over every dict object, fragmenting if necessary
    #all we need to do is split the dictionary into smaller dictionaries
    for i in range(0, len(dmx_buffer), fragmentation_size):
        fragment = dict(list(dmx_buffer.items())[i:i+fragmentation_size])
        fragments.append(fragment)
    for fragment in fragments:
        message = generateMessage(fragment)
        #print first channel
        #print(message)
        send_udp_packet(target_ip, target_port, message)
        time.sleep(0.001)  # brief pause to avoid overwhelming the network
    
class UDPClientTasks(Task):
    functions = {
        "depsgraph_update_post": send,
        "frame_change_post": send,
        "load_post": send,
    }
