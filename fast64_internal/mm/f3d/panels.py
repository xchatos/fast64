from bpy.types import Panel, Mesh, Armature
from bpy.utils import register_class, unregister_class
from ...panels import MM_Panel
from ...utility import prop_split
from .operators import MM_ImportDL, MM_ExportDL
from .properties import (
    MMDLExportSettings,
    MMDLImportSettings,
    MMDynamicMaterialProperty,
    MMDefaultRenderModesProperty,
)


class MM_DisplayListPanel(Panel):
    bl_label = "Display List Inspector"
    bl_idname = "OBJECT_PT_MM_DL_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM" and (
            context.object is not None and isinstance(context.object.data, Mesh)
        )

    def draw(self, context):
        box = self.layout.box().column()
        box.box().label(text="MM DL Inspector")
        obj = context.object

        # prop_split(box, obj, "mmDrawLayer", "Draw Layer")
        box.prop(obj, "ignore_render")
        box.prop(obj, "ignore_collision")

        if not (obj.parent is not None and isinstance(obj.parent.data, Armature)):
            actorScaleBox = box.box().column()
            prop_split(actorScaleBox, obj, "mmActorScale", "Actor Scale")
            actorScaleBox.label(text="This applies to actor exports only.", icon="INFO")

        # Doesn't work since all static meshes are pre-transformed
        # box.prop(obj.mmDynamicTransform, "billboard")


class MM_MaterialPanel(Panel):
    bl_label = "MM Material"
    bl_idname = "MATERIAL_PT_MM_Material_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.material is not None and context.scene.gameEditorMode == "MM"

    def draw(self, context):
        layout = self.layout
        mat = context.material
        col = layout.column()

        if (
            hasattr(context, "object")
            and context.object is not None
            and context.object.parent is not None
            and isinstance(context.object.parent.data, Armature)
        ):
            drawLayer = context.object.parent.mmDrawLayer
            if drawLayer != mat.f3d_mat.draw_layer.mm:
                col.label(text="Draw layer is being overriden by skeleton.", icon="OUTLINER_DATA_ARMATURE")
        else:
            drawLayer = mat.f3d_mat.draw_layer.mm

        dynMatProps: MMDynamicMaterialProperty = mat.mmMaterial
        dynMatProps.draw_props(col.box().column(), mat, drawLayer)


class MM_DrawLayersPanel(Panel):
    bl_label = "MM Draw Layers"
    bl_idname = "WORLD_PT_MM_Draw_Layers_Panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM"

    def draw(self, context):
        mmDefaultRenderModeProp: MMDefaultRenderModesProperty = context.scene.world.mmDefaultRenderModes
        mmDefaultRenderModeProp.draw_props(self.layout)


class MM_ExportDLPanel(MM_Panel):
    bl_idname = "MM_PT_export_dl"
    bl_label = "MM DL Exporter"

    # called every frame
    def draw(self, context):
        col = self.layout.column()

        col.operator(MM_ExportDL.bl_idname)
        exportSettings: MMDLExportSettings = context.scene.fast64.mm.DLExportSettings
        exportSettings.draw_props(col)

        col.operator(MM_ImportDL.bl_idname)
        importSettings: MMDLImportSettings = context.scene.fast64.mm.DLImportSettings
        importSettings.draw_props(col)


mm_dl_writer_panel_classes = (
    MM_DisplayListPanel,
    MM_MaterialPanel,
    MM_DrawLayersPanel,
    MM_ExportDLPanel,
)


def mm_f3d_panels_register():
    for cls in mm_dl_writer_panel_classes:
        register_class(cls)


def mm_f3d_panels_unregister():
    for cls in mm_dl_writer_panel_classes:
        unregister_class(cls)
