from bpy.types import Armature, Panel
from bpy.utils import register_class, unregister_class
from ...utility import prop_split
from ...panels import MM_Panel
from .properties import MMSkeletonImportSettings, MMSkeletonExportSettings
from .operators import MM_ImportSkeleton, MM_ExportSkeleton


class MM_SkeletonPanel(Panel):
    bl_idname = "MM_PT_skeleton"
    bl_label = "MM Skeleton Properties"
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
        col.box().label(text="MM Skeleton Inspector")
        prop_split(col, context.object, "mmDrawLayer", "Draw Layer")
        context.object.mmSkeleton.draw_props(col)

        prop_split(col, context.object, "mmActorScale", "Actor Scale")


class MM_BonePanel(Panel):
    bl_idname = "MM_PT_bone"
    bl_label = "MM Bone Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM" and context.bone is not None

    # called every frame
    def draw(self, context):
        col = self.layout.box().column()
        col.box().label(text="MM Bone Inspector")
        context.bone.mmBone.draw_props(col)


class MM_ExportSkeletonPanel(MM_Panel):
    bl_idname = "MM_PT_export_skeleton"
    bl_label = "MM Skeleton Exporter"

    # called every frame
    def draw(self, context):
        col = self.layout.column()
        col.operator(MM_ExportSkeleton.bl_idname)
        exportSettings: MMSkeletonExportSettings = context.scene.fast64.mm.skeletonExportSettings
        exportSettings.draw_props(col)

        col.operator(MM_ImportSkeleton.bl_idname)
        importSettings: MMSkeletonImportSettings = context.scene.fast64.mm.skeletonImportSettings
        importSettings.draw_props(col)


mm_skeleton_panels = (
    MM_SkeletonPanel,
    MM_BonePanel,
    MM_ExportSkeletonPanel,
)


def mm_skeleton_panels_register():
    for cls in mm_skeleton_panels:
        register_class(cls)


def mm_skeleton_panels_unregister():
    for cls in mm_skeleton_panels:
        unregister_class(cls)
