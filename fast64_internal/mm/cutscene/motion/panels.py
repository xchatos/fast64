from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from .properties import MMCSMotionCameraShotProperty, MMCSMotionCameraShotPointProperty


class MM_CSMotionCameraShotPanel(Panel):
    bl_label = "Cutscene Motion Camera Shot Controls"
    bl_idname = "MM_PT_camera_shot_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        obj = context.view_layer.objects.active
        layout = self.layout

        if obj.type == "ARMATURE":
            camShotProp: MMCSMotionCameraShotProperty = obj.data.mmCamShotProp
            camShotPointProp: MMCSMotionCameraShotPointProperty = None
            activeBone = editBone = None

            box = layout.box()
            camShotProp.draw_props(box, self.bl_label)

            if obj.mode == "POSE":
                box.label(text="Warning: You can't be in 'Pose' mode to edit camera bones!")
            elif obj.mode == "OBJECT":
                activeBone = obj.data.bones.active
                if activeBone is not None:
                    camShotPointProp = activeBone.mmCamShotPointProp
                    camShotPointProp.draw_props(box)
            elif obj.mode == "EDIT":
                editBone = obj.data.edit_bones.active
                if editBone is not None:
                    camShotPointProp = editBone.mmCamShotPointProp
                    camShotPointProp.draw_props(box)


classes = (MM_CSMotionCameraShotPanel,)


def mm_csMotion_panels_register():
    for cls in classes:
        register_class(cls)


def mm_csMotion_panels_unregister():
    for cls in reversed(classes):
        unregister_class(cls)
