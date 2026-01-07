import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class UDPClientToggleModal(Operator):
    """Simple toggle operator for UDP client on/off"""
    bl_idname = "bthl.udp_client_toggle"
    bl_label = "UDP Client Toggle"
    bl_description = "Toggle UDP client connection on/off"
    bl_options = {'REGISTER', 'UNDO'}

    udp_client_active_prop_name = "udp_client_active"

    @staticmethod
    def get_udp_client_state(context):
        return getattr(context.scene, UDPClientToggleModal.udp_client_active_prop_name, False)
    
    def execute(self, context):
        """Toggle UDP client state and exit"""
        
        # Get current state or default to False
        current_state = getattr(context.scene, UDPClientToggleModal.udp_client_active_prop_name, False)
        
        # Toggle the state
        new_state = not current_state
        setattr(context.scene, UDPClientToggleModal.udp_client_active_prop_name, new_state)
        
        # Report the new state
        status = "ON" if new_state else "OFF"
        self.report({'INFO'}, f"UDP Client: {status}")
        
        return {'FINISHED'}

    def dynamic_text(context):
        """Dynamically change button text based on state"""
        current_state = getattr(context.scene, UDPClientToggleModal.udp_client_active_prop_name, False)
        return "Stop UDP Client" if current_state else "Start UDP Client"

    def register():
        """Register the operator"""
        # Add scene property to store UDP client state globally
        bpy.types.Scene.udp_client_active = BoolProperty(
            name="UDP Client Active",
            description="Global UDP client active state",
            default=False
        )


    def unregister():
        """Unregister the operator"""
        # Remove scene property
        if hasattr(bpy.types.Scene, UDPClientToggleModal.udp_client_active_prop_name):
            del bpy.types.Scene.udp_client_active
