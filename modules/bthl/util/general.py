import bpy

def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min

# def register_list(cls: list):
#     """Registers a list of class"""
#     for c in cls:
#         bpy.utils.register_class(c)

# def unregister_list(cls: list):
#     """Unregisters a list of class"""
#     for c in cls:
#         bpy.utils.unregister_class(c)
