bl_info = {
    "name": "Blender to HNode link",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from bthl.panel.main_panel import MainPanel
from bthl.modal.sender_modal import UDPClientToggleModal
from bthl.tasks.sender import UDPClientTasks

classes = {
    MainPanel,
    UDPClientToggleModal,
}

tasks = {
    UDPClientTasks,
}

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    for task in tasks:
        task.register(task)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for task in tasks:
        task.unregister(task)
