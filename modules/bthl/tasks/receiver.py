import bpy
from bthl.tasks.task import Task
import socket
import struct
import random

sock = None

def receive() -> float:
    global sock

    receivebuffer_size = 64

    #receive via udp socket
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #make the receive buffer small
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, receivebuffer_size)
        #bind localhost on port 7001
        sock.bind(("localhost", 7001))
        sock.setblocking(False)
    
    update_rate = 0.001

    try:
        data, addr = sock.recvfrom(receivebuffer_size)
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
        frame += int((milliseconds / 1000) * fps)
        #set the current frame of the scene
        #check if we are still on this frame, if so do nothing
        if scene.frame_current == frame:
            return update_rate
        scene.frame_set(frame)
        return update_rate
    except BlockingIOError:
        #no data received
        return update_rate
