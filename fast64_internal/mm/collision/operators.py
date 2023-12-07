import bpy, os, mathutils
from bpy.types import Operator, Mesh
from bpy.utils import register_class, unregister_class
from bpy.ops import object
from mathutils import Matrix
from ..mm_collision import exportCollisionCommon, mmCollisionToC
from ..mm_collision_classes import MMCollision, MMCameraData
from .properties import MMCollisionExportSettings

from ...utility import (
    PluginError,
    CData,
    unhideAllAndGetHiddenState,
    restoreHiddenState,
    writeCData,
    toAlnum,
    raisePluginError,
)

from ..mm_utility import (
    MMObjectCategorizer,
    addIncludeFiles,
    getMMScale,
    mmDuplicateHierarchy,
    mmCleanupScene,
    mmGetPath,
    mmGetObjectPath,
)


def exportCollisionToC(
    originalObj: bpy.types.Object, transformMatrix: mathutils.Matrix, exportSettings: MMCollisionExportSettings
):
    includeChildren = exportSettings.includeChildren
    name = toAlnum(originalObj.name)
    isCustomExport = exportSettings.customExport
    folderName = exportSettings.folder
    exportPath = mmGetObjectPath(isCustomExport, bpy.path.abspath(exportSettings.exportPath), folderName)

    collision = MMCollision(name)
    collision.cameraData = MMCameraData(name)

    if bpy.context.scene.exportHiddenGeometry:
        hiddenState = unhideAllAndGetHiddenState(bpy.context.scene)

    # Don't remove ignore_render, as we want to resuse this for collision
    obj, allObjs = mmDuplicateHierarchy(originalObj, None, True, MMObjectCategorizer())

    if bpy.context.scene.exportHiddenGeometry:
        restoreHiddenState(hiddenState)

    try:
        exportCollisionCommon(collision, obj, transformMatrix, includeChildren, name)
        mmCleanupScene(originalObj, allObjs)
    except Exception as e:
        mmCleanupScene(originalObj, allObjs)
        raise Exception(str(e))

    collisionC = mmCollisionToC(collision)

    data = CData()
    data.source += '#include "ultra64.h"\n#include "z64.h"\n#include "macros.h"\n'
    if not isCustomExport:
        data.source += '#include "' + folderName + '.h"\n\n'
    else:
        data.source += "\n"

    data.append(collisionC)

    path = mmGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    filename = exportSettings.filename if exportSettings.isCustomFilename else f"{name}_collision"
    writeCData(data, os.path.join(path, f"{filename}.h"), os.path.join(path, f"{filename}.c"))

    if not isCustomExport:
        addIncludeFiles(folderName, path, name)


class MM_ExportCollision(Operator):
    # set bl_ properties
    bl_idname = "object.mm_export_collision"
    bl_label = "Export Collision"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        obj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")
        if len(context.selected_objects) == 0:
            raise PluginError("No object selected.")
        obj = context.active_object
        if type(obj.data) is not Mesh:
            raise PluginError("No mesh object selected.")

        finalTransform = Matrix.Scale(getMMScale(obj.mmActorScale), 4)

        try:
            exportSettings: MMCollisionExportSettings = context.scene.fast64.mm.collisionExportSettings
            exportCollisionToC(obj, finalTransform, exportSettings)

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


mm_col_classes = (MM_ExportCollision,)


def mm_collision_ops_register():
    for cls in mm_col_classes:
        register_class(cls)


def mm_collision_ops_unregister():
    for cls in reversed(mm_col_classes):
        unregister_class(cls)
