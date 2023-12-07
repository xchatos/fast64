from bpy.utils import register_class, unregister_class
from ...panels import MM_Panel
from .operators import (
    MM_AddWaterBox,
    MM_AddDoor,
    MM_AddScene,
    MM_AddRoom,
    MM_AddCutscene,
    MM_AddPath,
    MMClearTransformAndLock,
)


class Mm_ToolsPanel(MM_Panel):
    bl_idname = "MM_PT_tools"
    bl_label = "MM Tools"

    def draw(self, context):
        col = self.layout.column()
        col.operator(MM_AddWaterBox.bl_idname)
        col.operator(MM_AddDoor.bl_idname)
        col.operator(MM_AddScene.bl_idname)
        col.operator(MM_AddRoom.bl_idname)
        col.operator(MM_AddCutscene.bl_idname)
        col.operator(MM_AddPath.bl_idname)
        col.operator(MMClearTransformAndLock.bl_idname)


mm_operator_panel_classes = [
    Mm_ToolsPanel,
]

toolOpsToRegister = [
    MM_AddWaterBox,
    MM_AddDoor,
    MM_AddScene,
    MM_AddRoom,
    MM_AddCutscene,
    MM_AddPath,
    MMClearTransformAndLock,
]


def mm_operator_panel_register():
    for cls in mm_operator_panel_classes:
        register_class(cls)


def mm_operator_panel_unregister():
    for cls in mm_operator_panel_classes:
        unregister_class(cls)


def mm_operator_register():
    for cls in toolOpsToRegister:
        register_class(cls)


def mm_operator_unregister():
    for cls in reversed(toolOpsToRegister):
        unregister_class(cls)
