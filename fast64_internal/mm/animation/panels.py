from bpy.types import Panel, Armature
from bpy.utils import register_class, unregister_class
from ...utility import prop_split
from ...panels import MM_Panel
from .operators import MM_ExportAnim, MM_ImportAnim
from .properties import MMAnimExportSettingsProperty, MMAnimImportSettingsProperty, MMLinkTextureAnimProperty


class MM_LinkAnimPanel(Panel):
    bl_idname = "MM_PT_link_anim"
    bl_label = "MM Link Animation Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return (
            context.scene.gameEditorMode == "MM"
            and hasattr(context, "object")
            and context.object is not None
            and isinstance(context.object.data, Armature)
        )

    # called every frame
    def draw(self, context):
        col = self.layout.box().column()
        col.box().label(text="MM Link Animation Inspector")
        linkTextureAnim: MMLinkTextureAnimProperty = context.object.mmLinkTextureAnim
        linkTextureAnim.draw_props(col)
        col.label(text="Index 0 is for auto, flipbook starts at index 1.", icon="INFO")


class MM_ExportAnimPanel(MM_Panel):
    bl_idname = "MM_PT_export_anim"
    bl_label = "MM Animation Exporter"

    # called every frame
    def draw(self, context):
        col = self.layout.column()

        col.operator(MM_ExportAnim.bl_idname)
        exportSettings: MMAnimExportSettingsProperty = context.scene.fast64.mm.animExportSettings
        exportSettings.draw_props(col)

        col.operator(MM_ImportAnim.bl_idname)
        importSettings: MMAnimImportSettingsProperty = context.scene.fast64.mm.animImportSettings
        importSettings.draw_props(col)


panels = (
    MM_LinkAnimPanel,
    MM_ExportAnimPanel,
)


def mm_anim_panels_register():
    for cls in panels:
        register_class(cls)


def mm_anim_panels_unregister():
    for cls in panels:
        unregister_class(cls)
