from bpy.types import Panel, Camera
from bpy.utils import register_class, unregister_class
from ...utility import prop_split
from ...panels import MM_Panel
from ..mm_utility import drawEnumWithCustom
from .properties import MMCollisionExportSettings, MMCameraPositionProperty, MMMaterialCollisionProperty
from .operators import MM_ExportCollision


class MM_CameraPosPanel(Panel):
    bl_label = "Camera Position Inspector"
    bl_idname = "OBJECT_PT_MM_Camera_Position_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM" and isinstance(context.object.data, Camera)

    def draw(self, context):
        box = self.layout.box().column()
        obj = context.object

        box.box().label(text="Camera Data")
        camPosProps: MMCameraPositionProperty = obj.mmCameraPositionProperty
        camPosProps.draw_props(box, obj)


class MM_CollisionPanel(Panel):
    bl_label = "Collision Inspector"
    bl_idname = "MATERIAL_PT_MM_Collision_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM" and context.material is not None

    def draw(self, context):
        box = self.layout.box().column()

        collisionProp: MMMaterialCollisionProperty = context.material.mmCollisionProperty
        collisionProp.draw_props(box)


class MM_ExportCollisionPanel(MM_Panel):
    bl_idname = "MM_PT_export_collision"
    bl_label = "MM Collision Exporter"

    # called every frame
    def draw(self, context):
        col = self.layout.column()
        col.operator(MM_ExportCollision.bl_idname)

        exportSettings: MMCollisionExportSettings = context.scene.fast64.mm.collisionExportSettings
        exportSettings.draw_props(col)


mm_col_panel_classes = (
    MM_CameraPosPanel,
    MM_CollisionPanel,
    MM_ExportCollisionPanel,
)


def mm_collision_panels_register():
    for cls in mm_col_panel_classes:
        register_class(cls)


def mm_collision_panels_unregister():
    for cls in mm_col_panel_classes:
        unregister_class(cls)
