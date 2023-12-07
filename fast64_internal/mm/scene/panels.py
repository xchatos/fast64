import os
from bpy.types import UILayout
from bpy.utils import register_class, unregister_class
from ...utility import customExportWarning, prop_split
from ...panels import MM_Panel
from ..mm_constants import mmEnumSceneID
from ..mm_utility import getEnumName
from .properties import (
    MMExportSceneSettingsProperty,
    MMImportSceneSettingsProperty,
    MMRemoveSceneSettingsProperty,
    MMBootupSceneOptions,
    MMSceneCommon,
)

from .operators import (
    MM_ImportScene,
    MM_ExportScene,
    MM_RemoveScene,
    MM_ClearBootupScene,
    MM_SearchSceneEnumOperator,
)


class MM_ExportScenePanel(MM_Panel):
    bl_idname = "MM_PT_export_level"
    bl_label = "MM Scene Exporter"

    def drawSceneSearchOp(self, layout: UILayout, enumValue: str, opName: str):
        searchBox = layout.box().row()
        searchBox.operator(MM_SearchSceneEnumOperator.bl_idname, icon="VIEWZOOM", text="").opName = opName
        searchBox.label(text=getEnumName(mmEnumSceneID, enumValue))

    def draw(self, context):
        col = self.layout.column()

        # Scene Exporter
        exportBox = col.box().column()
        exportBox.label(text="Scene Exporter")

        settings: MMExportSceneSettingsProperty = context.scene.mmSceneExportSettings
        if not settings.customExport:
            self.drawSceneSearchOp(exportBox, settings.option, "Export")
        settings.draw_props(exportBox)

        if context.scene.fast64.mm.hackerFeaturesEnabled:
            hackerMmBox = exportBox.box().column()
            hackerMmBox.label(text="HackerMm Options")

            bootOptions: MMBootupSceneOptions = context.scene.fast64.mm.bootupSceneOptions
            bootOptions.draw_props(hackerMmBox)

            hackerMmBox.label(
                text="Note: Scene boot config changes aren't detected by the make process.", icon="ERROR"
            )
            hackerMmBox.operator(MM_ClearBootupScene.bl_idname, text="Undo Boot To Scene (HackerMM Repo)")

        exportBox.operator(MM_ExportScene.bl_idname)

        # Scene Importer
        importBox = col.box().column()
        importBox.label(text="Scene Importer")

        importSettings: MMImportSceneSettingsProperty = context.scene.mmSceneImportSettings

        if not importSettings.isCustomDest:
            self.drawSceneSearchOp(importBox, importSettings.option, "Import")

        importSettings.draw_props(importBox, importSettings.option)
        importBox.operator(MM_ImportScene.bl_idname)

        # Remove Scene
        removeBox = col.box().column()
        removeBox.label(text="Remove Scene")

        removeSettings: MMRemoveSceneSettingsProperty = context.scene.mmSceneRemoveSettings
        self.drawSceneSearchOp(removeBox, removeSettings.option, "Remove")
        removeSettings.draw_props(removeBox)

        removeRow = removeBox.row()
        removeRow.operator(MM_RemoveScene.bl_idname, text="Remove Scene")

        if removeSettings.option == "Custom":
            exportPath = (
                context.scene.mmDecompPath + f"assets/scenes/{removeSettings.subFolder}/{removeSettings.name}/"
            )

            if not os.path.exists(exportPath):
                removeRow.enabled = False
                removeBox.label(text="This path doesn't exist.")
            else:
                removeRow.enabled = True


classes = (MM_ExportScenePanel,)


def mm_scene_panels_register():
    for cls in classes:
        register_class(cls)


def mm_scene_panels_unregister():
    for cls in classes:
        unregister_class(cls)
