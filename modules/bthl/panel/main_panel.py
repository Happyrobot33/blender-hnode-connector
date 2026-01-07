import bpy
import bthl.modal.sender_modal as sender_modal

class MainPanel(bpy.types.Panel):
    bl_label = "HNode Connector"
    bl_idname = "BTHL_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HNode Connector'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        #render udp client
        layout.operator(sender_modal.UDPClientToggleModal.bl_idname, text=sender_modal.UDPClientToggleModal.dynamic_text(context))
