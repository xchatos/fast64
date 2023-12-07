import mathutils, bpy, os
from bpy.types import Scene, Operator, Armature
from bpy.props import StringProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from bpy.ops import object
from ...utility import PluginError, toAlnum, writeCData, raisePluginError
from .properties import MMAnimExportSettingsProperty, MMAnimImportSettingsProperty

from ..mm_anim import (
    mmExportLinkAnimation,
    mmExportNonLinkAnimation,
    mmImportLinkAnimationC,
    mmImportNonLinkAnimationC,
)

from ..mm_utility import (
    mmGetPath,
    addIncludeFiles,
    checkEmptyName,
    mmGetObjectPath,
    getMMScale,
)


def exportAnimationC(armatureObj: bpy.types.Object, settings: MMAnimExportSettingsProperty):
    path = bpy.path.abspath(settings.customPath)
    exportPath = mmGetObjectPath(settings.isCustom, path, settings.folderName)

    checkEmptyName(settings.folderName)
    checkEmptyName(armatureObj.name)
    name = toAlnum(armatureObj.name)
    filename = settings.filename if settings.isCustomFilename else name
    convertTransformMatrix = (
        mathutils.Matrix.Scale(getMMScale(armatureObj.mmActorScale), 4)
        @ mathutils.Matrix.Diagonal(armatureObj.scale).to_4x4()
    )

    if settings.isLink:
        mmAnim = mmExportLinkAnimation(armatureObj, convertTransformMatrix, name)
        mmAnimC, mmAnimHeaderC = mmAnim.toC(settings.isCustom)
        path = mmGetPath(
            exportPath,
            settings.isCustom,
            "assets/misc/link_animetion",
            settings.folderName if settings.isCustom else "",
            False,
            False,
        )
        headerPath = mmGetPath(
            exportPath,
            settings.isCustom,
            "assets/objects/gameplay_keep",
            settings.folderName if settings.isCustom else "",
            False,
            False,
        )
        writeCData(
            mmAnimC, os.path.join(path, mmAnim.dataName() + ".h"), os.path.join(path, mmAnim.dataName() + ".c")
        )
        writeCData(
            mmAnimHeaderC,
            os.path.join(headerPath, mmAnim.headerName + ".h"),
            os.path.join(headerPath, mmAnim.headerName + ".c"),
        )

        if not settings.isCustom:
            addIncludeFiles("link_animetion", path, mmAnim.dataName())
            addIncludeFiles("gameplay_keep", headerPath, mmAnim.headerName)

    else:
        mmAnim = mmExportNonLinkAnimation(armatureObj, convertTransformMatrix, name)

        mmAnimC = mmAnim.toC()
        path = mmGetPath(exportPath, settings.isCustom, "assets/objects/", settings.folderName, False, False)
        writeCData(mmAnimC, os.path.join(path, filename + ".h"), os.path.join(path, filename + ".c"))

        if not settings.isCustom:
            addIncludeFiles(settings.folderName, path, filename)


def mmImportAnimationC(
    armatureObj: bpy.types.Object,
    settings: MMAnimImportSettingsProperty,
    actorScale: float,
):
    importPath = bpy.path.abspath(settings.customPath)
    filepath = mmGetObjectPath(settings.isCustom, importPath, settings.folderName)
    if settings.isLink:
        numLimbs = 21
        if not settings.isCustom:
            basePath = bpy.path.abspath(bpy.context.scene.mmDecompPath)
            animFilepath = os.path.join(basePath, "assets/misc/link_animetion/link_animetion.c")
            animHeaderFilepath = os.path.join(basePath, "assets/objects/gameplay_keep/gameplay_keep.c")
        else:
            animFilepath = filepath
            animHeaderFilepath = filepath
        mmImportLinkAnimationC(
            armatureObj,
            animHeaderFilepath,
            animFilepath,
            settings.animName,
            actorScale,
            numLimbs,
            settings.isCustom,
        )
    else:
        mmImportNonLinkAnimationC(armatureObj, filepath, settings.animName, actorScale, settings.isCustom)


class MM_ExportAnim(Operator):
    bl_idname = "object.mm_export_anim"
    bl_label = "Export Animation"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        try:
            if len(context.selected_objects) == 0 or not isinstance(context.selected_objects[0].data, Armature):
                raise PluginError("Armature not selected.")
            if len(context.selected_objects) > 1:
                raise PluginError("Multiple objects selected, make sure to select only one.")
            armatureObj = context.selected_objects[0]
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}

        try:
            settings = context.scene.fast64.mm.animExportSettings
            exportAnimationC(armatureObj, settings)
            self.report({"INFO"}, "Success!")

        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set

        return {"FINISHED"}  # must return a set


class MM_ImportAnim(Operator):
    bl_idname = "object.mm_import_anim"
    bl_label = "Import Animation"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        try:
            if len(context.selected_objects) == 0 or not isinstance(context.selected_objects[0].data, Armature):
                raise PluginError("Armature not selected.")
            if len(context.selected_objects) > 1:
                raise PluginError("Multiple objects selected, make sure to select only one.")
            armatureObj = context.selected_objects[0]
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")

            # We need to apply scale otherwise translation imports won't be correct.
            object.select_all(action="DESELECT")
            armatureObj.select_set(True)
            context.view_layer.objects.active = armatureObj
            object.transform_apply(location=False, rotation=False, scale=True, properties=False)

        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}

        try:
            actorScale = getMMScale(armatureObj.mmActorScale)
            settings = context.scene.fast64.mm.animImportSettings
            mmImportAnimationC(armatureObj, settings, actorScale)
            self.report({"INFO"}, "Success!")

        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set

        return {"FINISHED"}  # must return a set


mm_anim_classes = (
    MM_ExportAnim,
    MM_ImportAnim,
)


def mm_anim_ops_register():
    Scene.mmAnimIsCustomExport = BoolProperty(name="Use Custom Path")
    Scene.mmAnimExportCustomPath = StringProperty(name="Folder", subtype="FILE_PATH")
    Scene.mmAnimExportFolderName = StringProperty(name="Animation Folder", default="object_geldb")

    Scene.mmAnimIsCustomImport = BoolProperty(name="Use Custom Path")
    Scene.mmAnimImportCustomPath = StringProperty(name="Folder", subtype="FILE_PATH")
    Scene.mmAnimImportFolderName = StringProperty(name="Animation Folder", default="object_geldb")

    Scene.mmAnimSkeletonName = StringProperty(name="Skeleton Name", default="gGerudoRedSkel")
    Scene.mmAnimName = StringProperty(name="Anim Name", default="gGerudoRedSpinAttackAnim")
    for cls in mm_anim_classes:
        register_class(cls)


def mm_anim_ops_unregister():
    del Scene.mmAnimIsCustomExport
    del Scene.mmAnimExportCustomPath
    del Scene.mmAnimExportFolderName

    del Scene.mmAnimIsCustomImport
    del Scene.mmAnimImportCustomPath
    del Scene.mmAnimImportFolderName

    del Scene.mmAnimSkeletonName
    del Scene.mmAnimName
    for cls in reversed(mm_anim_classes):
        unregister_class(cls)
