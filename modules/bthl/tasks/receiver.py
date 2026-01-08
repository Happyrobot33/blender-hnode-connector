import bpy
from bthl.tasks.task import Task
import socket
import struct
import random

sock = None

def receive() -> float:
    global sock

    #receive via udp socket
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #bind localhost on port 7001
        sock.bind(("localhost", 7001))
        sock.setblocking(False)
    
    try:
        data, addr = sock.recvfrom(10)  # buffer size is 65535 bytes
        print(f"Received message from {addr}: {data}")
        #the data coming in is a signed long long in bytes, big endian
        milliseconds = int.from_bytes(data[0:4], byteorder='big', signed=True)
        frames = data[4]
        # val = random.randint(0, 20)
        scene = bpy.context.scene
        # scene.frame_set(milliseconds)
        # return 0.01
        # scene = bpy.context.scene
        # scene.frame_set(int(value / 1000))
        # return 0.001
        #get the scene
        fps = scene.render.fps / scene.render.fps_base
        #convert the value to frames
        frame = frames
        if milliseconds > 0:
            frame += int((milliseconds / 1000) * fps)
        #set the current frame of the scene
        scene.frame_set(frame)
        return 0.001
    except BlockingIOError:
        #no data received
        return 0.001

    return 0.001  # Call again after 1.0 seconds
