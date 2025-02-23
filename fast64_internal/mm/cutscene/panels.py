from bpy.utils import register_class, unregister_class
from bpy.types import Scene
from bpy.props import BoolProperty
from ...utility import prop_split
from ...panels import MM_Panel
from .operators import MM_ExportCutscene, MM_ExportAllCutscenes, MM_ImportCutscene


class MM_CutscenePanel(MM_Panel):
    bl_idname = "MM_PT_export_cutscene"
    bl_label = "MM Cutscene Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MM"

    def draw(self, context):
        layout = self.layout

        exportBox = layout.box()
        exportBox.label(text="Cutscene Exporter")

        col = exportBox.column()
        if not context.scene.fast64.mm.hackerFeaturesEnabled:
            col.prop(context.scene, "useDecompFeatures")
        col.prop(context.scene, "exportMotionOnly")

        prop_split(exportBox, context.scene, "mmCutsceneExportPath", "Export To")

        activeObj = context.view_layer.objects.active
        label = None
        col = exportBox.column()
        colcol = col.column()
        if activeObj is None or activeObj.type != "EMPTY" or activeObj.mmEmptyType != "Cutscene":
            label = "Select a cutscene object"

        if activeObj is not None and activeObj.parent is not None:
            label = "Cutscene object must not be parented to anything"

        if label is not None:
            col.label(text=label)
            colcol.enabled = False

        colcol.operator(MM_ExportCutscene.bl_idname)
        col.operator(MM_ExportAllCutscenes.bl_idname)

        importBox = layout.box()
        importBox.label(text="Cutscene Importer")
        prop_split(importBox, context.scene, "mmCutsceneImportPath", "Import From")

        col = importBox.column()
        col.operator(MM_ImportCutscene.bl_idname)


mm_cutscene_panel_classes = (MM_CutscenePanel,)


def mm_cutscene_panels_register():
    Scene.useDecompFeatures = BoolProperty(
        name="Use Decomp for Export", description="Use names and macros from decomp when exporting", default=True
    )
    Scene.exportMotionOnly = BoolProperty(
        name="Export Motion Data Only",
        description=(
            "Export everything or only the camera and actor motion data.\n"
            + "This will insert the data into the cutscene."
        ),
    )

    for cls in mm_cutscene_panel_classes:
        register_class(cls)


def mm_cutscene_panels_unregister():
    del Scene.exportMotionOnly
    del Scene.useDecompFeatures

    for cls in mm_cutscene_panel_classes:
        unregister_class(cls)
