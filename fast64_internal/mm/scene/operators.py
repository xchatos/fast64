import bpy, os
from bpy.path import abspath
from bpy.types import Operator, UILayout
from bpy.props import EnumProperty, IntProperty, StringProperty
from bpy.utils import register_class, unregister_class
from bpy.ops import object
from mathutils import Matrix, Vector
from ...f3d.f3d_gbi import DLFormat
from ...utility import PluginError, raisePluginError, mmGetSceneOrRoomHeader
from ..mm_utility import ExportInfo, sceneNameFromID, getEnumName
from ..mm_level_writer import mmExportSceneToC
from ..mm_constants import mmEnumMusicSeq, mmEnumSceneID
from ..mm_level_parser import parseScene
from .exporter.to_c import clearBootupScene, modifySceneTable, editSpecFile, deleteSceneFiles


def mmRemoveSceneC(exportInfo):
    modifySceneTable(None, exportInfo)
    editSpecFile(None, exportInfo, None)
    deleteSceneFiles(exportInfo)


def run_ops_without_view_layer_update(func):
    from bpy.ops import _BPyOpsSubModOp

    view_layer_update = _BPyOpsSubModOp._view_layer_update

    def dummy_view_layer_update(context):
        pass

    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update
        func()

    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update


def parseSceneFunc():
    settings = bpy.context.scene.mmSceneImportSettings
    parseScene(settings, settings.option)


class MM_SearchSceneEnumOperator(Operator):
    bl_idname = "object.mm_search_scene_enum_operator"
    bl_label = "Choose Scene"
    bl_property = "mmSceneID"
    bl_options = {"REGISTER", "UNDO"}

    mmSceneID: EnumProperty(items=mmEnumSceneID, default="SCENE_DEKU_TREE")
    opName: StringProperty(default="Export")

    def execute(self, context):
        if self.opName == "Export":
            context.scene.mmSceneExportSettings.option = self.mmSceneID
        elif self.opName == "Import":
            context.scene.mmSceneImportSettings.option = self.mmSceneID
        elif self.opName == "Remove":
            context.scene.mmSceneRemoveSettings.option = self.mmSceneID
        else:
            raise Exception(f'Invalid MM scene search operator name: "{self.opName}"')

        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.mmSceneID)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class MM_SearchMusicSeqEnumOperator(Operator):
    bl_idname = "object.mm_search_music_seq_enum_operator"
    bl_label = "Search Music Sequence"
    bl_property = "mmMusicSeq"
    bl_options = {"REGISTER", "UNDO"}

    mmMusicSeq: EnumProperty(items=mmEnumMusicSeq, default="0x02")
    headerIndex: IntProperty(default=0, min=0)
    objName: StringProperty()

    def execute(self, context):
        sceneHeader = mmGetSceneOrRoomHeader(bpy.data.objects[self.objName], self.headerIndex, False)
        sceneHeader.musicSeq = self.mmMusicSeq
        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.mmMusicSeq)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


class MM_ClearBootupScene(Operator):
    bl_idname = "object.mm_clear_bootup_scene"
    bl_label = "Undo Boot To Scene"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        clearBootupScene(os.path.join(abspath(context.scene.mmDecompPath), "include/config/config_debug.h"))
        self.report({"INFO"}, "Success!")
        return {"FINISHED"}


class MM_ImportScene(Operator):
    """Import an MM scene from C."""

    bl_idname = "object.mm_import_level"
    bl_label = "Import Scene"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        try:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            object.select_all(action="DESELECT")

            run_ops_without_view_layer_update(parseSceneFunc)

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}


class MM_ExportScene(Operator):
    """Export an MM scene."""

    bl_idname = "object.mm_export_level"
    bl_label = "Export Scene"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        activeObj = None
        try:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            activeObj = context.view_layer.objects.active

            obj = context.scene.mmSceneExportObj
            if obj is None:
                raise PluginError("Scene object input not set.")
            elif obj.data is not None or obj.mmEmptyType != "Scene":
                raise PluginError("The input object is not an empty with the Scene type.")

            scaleValue = context.scene.mmBlenderScale
            finalTransform = Matrix.Diagonal(Vector((scaleValue, scaleValue, scaleValue))).to_4x4()

        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}
        try:
            settings = context.scene.mmSceneExportSettings
            levelName = settings.name
            option = settings.option
            if settings.customExport:
                exportInfo = ExportInfo(True, bpy.path.abspath(settings.exportPath), None, levelName)
            else:
                if option == "Custom":
                    subfolder = "assets/scenes/" + settings.subFolder + "/"
                else:
                    levelName = sceneNameFromID(option)
                    subfolder = None
                exportInfo = ExportInfo(False, bpy.path.abspath(context.scene.mmDecompPath), subfolder, levelName)

            bootOptions = context.scene.fast64.mm.bootupSceneOptions
            hackerFeaturesEnabled = context.scene.fast64.mm.hackerFeaturesEnabled
            mmExportSceneToC(
                obj,
                finalTransform,
                levelName,
                DLFormat.Static,
                context.scene.saveTextures,
                exportInfo,
                bootOptions if hackerFeaturesEnabled else None,
            )

            self.report({"INFO"}, "Success!")

            # don't select the scene
            for elem in context.selectable_objects:
                elem.select_set(False)

            context.view_layer.objects.active = activeObj
            if activeObj is not None:
                activeObj.select_set(True)

            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            # don't select the scene
            for elem in context.selectable_objects:
                elem.select_set(False)
            context.view_layer.objects.active = activeObj
            if activeObj is not None:
                activeObj.select_set(True)
            raisePluginError(self, e)
            return {"CANCELLED"}


class MM_RemoveScene(Operator):
    """Remove an MM scene from an existing decomp directory."""

    bl_idname = "object.mm_remove_level"
    bl_label = "MM Remove Scene"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.mmSceneRemoveSettings  # Type: MMRemoveSceneSettingsProperty
        levelName = settings.name
        option = settings.option

        if settings.customExport:
            self.report({"ERROR"}, "You can only remove scenes from your decomp path.")
            return {"FINISHED"}

        if option == "Custom":
            subfolder = "assets/scenes/" + settings.subFolder + "/"
        else:
            levelName = sceneNameFromID(option)
            subfolder = None
        exportInfo = ExportInfo(False, abspath(context.scene.mmDecompPath), subfolder, levelName)

        mmRemoveSceneC(exportInfo)

        self.report({"INFO"}, "Success!")
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to remove this scene?")


classes = (
    MM_SearchMusicSeqEnumOperator,
    MM_SearchSceneEnumOperator,
    MM_ClearBootupScene,
    MM_ImportScene,
    MM_ExportScene,
    MM_RemoveScene,
)


def mm_scene_ops_register():
    for cls in classes:
        register_class(cls)


def mm_scene_ops_unregister():
    for cls in reversed(classes):
        unregister_class(cls)
