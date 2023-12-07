import bpy, os, mathutils
from bpy.types import Operator, Mesh
from bpy.ops import object
from bpy.path import abspath
from bpy.utils import register_class, unregister_class
from mathutils import Matrix
from ...utility import CData, PluginError, raisePluginError, writeCData, toAlnum
from ...f3d.f3d_parser import importMeshC, getImportData
from ...f3d.f3d_gbi import DLFormat, F3D, TextureExportSettings, ScrollMethod, get_F3D_GBI
from ...f3d.f3d_writer import TriangleConverterInfo, removeDL, saveStaticModel, getInfoDict
from ..mm_utility import mmGetObjectPath, getMMScale
from ..mm_model_classes import MMF3DContext, mmGetIncludedAssetData
from ..mm_texture_array import mmReadTextureArrays
from ..mm_model_classes import MMModel, MMGfxFormatter
from ..mm_f3d_writer import mmReadActorScale, writeTextureArraysNew, writeTextureArraysExisting
from .properties import MMDLImportSettings, MMDLExportSettings

from ..mm_utility import (
    MMObjectCategorizer,
    mmDuplicateHierarchy,
    mmCleanupScene,
    mmGetPath,
    addIncludeFiles,
    getMMScale,
)


def mmConvertMeshToC(
    originalObj: bpy.types.Object,
    finalTransform: mathutils.Matrix,
    DLFormat: DLFormat,
    saveTextures: bool,
    settings: MMDLExportSettings,
):
    folderName = settings.folder
    exportPath = bpy.path.abspath(settings.customPath)
    isCustomExport = settings.isCustom
    drawLayer = settings.drawLayer
    removeVanillaData = settings.removeVanillaData
    name = toAlnum(originalObj.name)
    overlayName = settings.actorOverlayName
    flipbookUses2DArray = settings.flipbookUses2DArray
    flipbookArrayIndex2D = settings.flipbookArrayIndex2D if flipbookUses2DArray else None

    try:
        obj, allObjs = mmDuplicateHierarchy(originalObj, None, False, MMObjectCategorizer())

        fModel = MMModel(name, DLFormat, drawLayer)
        triConverterInfo = TriangleConverterInfo(obj, None, fModel.f3d, finalTransform, getInfoDict(obj))
        fMeshes = saveStaticModel(
            triConverterInfo, fModel, obj, finalTransform, fModel.name, not saveTextures, False, "mm"
        )

        # Since we provide a draw layer override, there should only be one fMesh.
        for drawLayer, fMesh in fMeshes.items():
            fMesh.draw.name = name

        mmCleanupScene(originalObj, allObjs)

    except Exception as e:
        mmCleanupScene(originalObj, allObjs)
        raise Exception(str(e))

    data = CData()
    data.source += '#include "ultra64.h"\n#include "global.h"\n'
    if not isCustomExport:
        data.source += '#include "' + folderName + '.h"\n\n'
    else:
        data.source += "\n"

    path = mmGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    includeDir = settings.customAssetIncludeDir if settings.isCustom else f"assets/objects/{folderName}"
    exportData = fModel.to_c(
        TextureExportSettings(False, saveTextures, includeDir, path), MMGfxFormatter(ScrollMethod.Vertex)
    )

    data.append(exportData.all())

    if isCustomExport:
        textureArrayData = writeTextureArraysNew(fModel, flipbookArrayIndex2D)
        data.append(textureArrayData)

    filename = settings.filename if settings.isCustomFilename else name
    writeCData(data, os.path.join(path, filename + ".h"), os.path.join(path, filename + ".c"))

    if not isCustomExport:
        writeTextureArraysExisting(bpy.context.scene.mmDecompPath, overlayName, False, flipbookArrayIndex2D, fModel)
        addIncludeFiles(folderName, path, name)
        if removeVanillaData:
            headerPath = os.path.join(path, folderName + ".h")
            sourcePath = os.path.join(path, folderName + ".c")
            removeDL(sourcePath, headerPath, name)


class MM_ImportDL(Operator):
    # set bl_ properties
    bl_idname = "object.mm_import_dl"
    bl_label = "Import DL"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        obj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")

        try:
            settings: MMDLImportSettings = context.scene.fast64.mm.DLImportSettings
            name = settings.name
            folderName = settings.folder
            importPath = abspath(settings.customPath)
            isCustomImport = settings.isCustom
            basePath = abspath(context.scene.mmDecompPath) if not isCustomImport else importPath
            removeDoubles = settings.removeDoubles
            importNormals = settings.importNormals
            drawLayer = settings.drawLayer
            overlayName = settings.actorOverlayName
            flipbookUses2DArray = settings.flipbookUses2DArray
            flipbookArrayIndex2D = settings.flipbookArrayIndex2D if flipbookUses2DArray else None

            paths = [mmGetObjectPath(isCustomImport, importPath, folderName)]
            data = getImportData(paths)
            f3dContext = MMF3DContext(get_F3D_GBI(), [name], basePath)

            scale = getMMScale(settings.actorScale)
            if not isCustomImport:
                data = mmGetIncludedAssetData(basePath, paths, data) + data

                if overlayName is not None:
                    mmReadTextureArrays(basePath, overlayName, name, f3dContext, False, flipbookArrayIndex2D)
                if settings.autoDetectActorScale:
                    scale = mmReadActorScale(basePath, overlayName, False)

            obj = importMeshC(
                data,
                name,
                scale,
                removeDoubles,
                importNormals,
                drawLayer,
                f3dContext,
            )
            obj.mmActorScale = scale / context.scene.mmBlenderScale

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


class MM_ExportDL(Operator):
    # set bl_ properties
    bl_idname = "object.mm_export_dl"
    bl_label = "Export DL"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        obj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")
        if len(context.selected_objects) == 0:
            raise PluginError("Mesh not selected.")
        obj = context.active_object
        if type(obj.data) is not Mesh:
            raise PluginError("Mesh not selected.")

        finalTransform = Matrix.Scale(getMMScale(obj.mmActorScale), 4)

        try:
            # exportPath, levelName = getPathAndLevel(context.scene.geoCustomExport,
            # 	context.scene.geoExportPath, context.scene.geoLevelName,
            # 	context.scene.geoLevelOption)

            saveTextures = context.scene.saveTextures
            exportSettings = context.scene.fast64.mm.DLExportSettings

            mmConvertMeshToC(
                obj,
                finalTransform,
                DLFormat.Static,
                saveTextures,
                exportSettings,
            )

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


mm_dl_writer_classes = (
    MM_ImportDL,
    MM_ExportDL,
)


def mm_f3d_ops_register():
    for cls in mm_dl_writer_classes:
        register_class(cls)


def mm_f3d_ops_unregister():
    for cls in reversed(mm_dl_writer_classes):
        unregister_class(cls)
