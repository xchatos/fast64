import mathutils, bpy, os
from ....f3d.f3d_gbi import DLFormat, FMesh, TextureExportSettings, ScrollMethod
from ....f3d.f3d_writer import getInfoDict
from ...mm_f3d_writer import mmProcessVertexGroup, writeTextureArraysNew, writeTextureArraysExisting
from ...mm_model_classes import MMModel, MMGfxFormatter
from ..constants import mmSkeletonImportDict
from ..properties import MMSkeletonExportSettings
from ..utility import mmDuplicateArmatureAndRemoveRotations, getGroupIndices, mmRemoveSkeleton
from .classes import MMLimb, MMSkeleton

from ....utility import (
    PluginError,
    CData,
    getGroupIndexFromname,
    writeCData,
    toAlnum,
    cleanupDuplicatedObjects,
)

from ...mm_utility import (
    checkEmptyName,
    checkForStartBone,
    getStartBone,
    getSortedChildren,
    mmGetPath,
    addIncludeFiles,
)


def mmProcessBone(
    fModel,
    boneName,
    parentLimb,
    nextIndex,
    meshObj,
    armatureObj,
    convertTransformMatrix,
    meshInfo,
    convertTextureData,
    namePrefix,
    skeletonOnly,
    drawLayer,
    lastMaterialName,
    optimize: bool,
):
    bone = armatureObj.data.bones[boneName]
    if bone.parent is not None:
        transform = convertTransformMatrix @ bone.parent.matrix_local.inverted() @ bone.matrix_local
    else:
        transform = convertTransformMatrix @ bone.matrix_local

    translate, rotate, scale = transform.decompose()

    groupIndex = getGroupIndexFromname(meshObj, boneName)

    meshInfo.vertexGroupInfo.vertexGroupToLimb[groupIndex] = nextIndex

    if skeletonOnly:
        mesh = None
        hasSkinnedFaces = None
    else:
        mesh, hasSkinnedFaces, lastMaterialName = mmProcessVertexGroup(
            fModel,
            meshObj,
            boneName,
            convertTransformMatrix,
            armatureObj,
            namePrefix,
            meshInfo,
            drawLayer,
            convertTextureData,
            lastMaterialName,
            optimize,
        )

    if bone.mmBone.boneType == "Custom DL":
        if mesh is not None:
            raise PluginError(
                bone.name
                + " is set to use a custom DL but still has geometry assigned to it. Remove this geometry from this bone."
            )
        else:
            # Dummy data, only used so that name is set correctly
            mesh = FMesh(bone.mmBone.customDLName, DLFormat.Static)

    DL = None
    if mesh is not None:
        if not bone.use_deform:
            raise PluginError(
                bone.name
                + " has vertices in its vertex group but is not set to deformable. Make sure to enable deform on this bone."
            )
        DL = mesh.draw

    if isinstance(parentLimb, MMSkeleton):
        skeleton = parentLimb
        limb = MMLimb(skeleton.name, boneName, nextIndex, translate, DL, None)
        skeleton.limbRoot = limb
    else:
        limb = MMLimb(parentLimb.skeletonName, boneName, nextIndex, translate, DL, None)
        parentLimb.children.append(limb)

    limb.isFlex = hasSkinnedFaces
    nextIndex += 1

    # This must be in depth-first order to match the Mm SkelAnime draw code, so
    # the bones are listed in the file in the same order as they are drawn. This
    # is needed to enable the programmer to get the limb indices and to enable
    # optimization between limbs.
    childrenNames = getSortedChildren(armatureObj, bone)
    for childName in childrenNames:
        nextIndex, lastMaterialName = mmProcessBone(
            fModel,
            childName,
            limb,
            nextIndex,
            meshObj,
            armatureObj,
            convertTransformMatrix,
            meshInfo,
            convertTextureData,
            namePrefix,
            skeletonOnly,
            drawLayer,
            lastMaterialName,
            optimize,
        )

    return nextIndex, lastMaterialName


def mmConvertArmatureToSkeleton(
    originalArmatureObj,
    convertTransformMatrix,
    fModel,
    name,
    convertTextureData,
    skeletonOnly,
    drawLayer,
    optimize: bool,
):
    checkEmptyName(name)

    armatureObj, meshObjs = mmDuplicateArmatureAndRemoveRotations(originalArmatureObj)

    try:
        skeleton = MMSkeleton(name)

        if len(armatureObj.children) == 0:
            raise PluginError("No mesh parented to armature.")

        # startBoneNames = sorted([bone.name for bone in armatureObj.data.bones if bone.parent is None])
        # startBoneName = startBoneNames[0]
        checkForStartBone(armatureObj)
        startBoneName = getStartBone(armatureObj)
        meshObj = meshObjs[0]

        meshInfo = getInfoDict(meshObj)
        getGroupIndices(meshInfo, armatureObj, meshObj, getGroupIndexFromname(meshObj, startBoneName))

        convertTransformMatrix = convertTransformMatrix @ mathutils.Matrix.Diagonal(armatureObj.scale).to_4x4()

        # for i in range(len(startBoneNames)):
        # 	startBoneName = startBoneNames[i]
        mmProcessBone(
            fModel,
            startBoneName,
            skeleton,
            0,
            meshObj,
            armatureObj,
            convertTransformMatrix,
            meshInfo,
            convertTextureData,
            name,
            skeletonOnly,
            drawLayer,
            None,
            optimize,
        )

        cleanupDuplicatedObjects(meshObjs + [armatureObj])
        originalArmatureObj.select_set(True)
        bpy.context.view_layer.objects.active = originalArmatureObj

        return skeleton, fModel
    except Exception as e:
        cleanupDuplicatedObjects(meshObjs + [armatureObj])
        originalArmatureObj.select_set(True)
        bpy.context.view_layer.objects.active = originalArmatureObj
        raise Exception(str(e))


def mmConvertArmatureToSkeletonWithoutMesh(originalArmatureObj, convertTransformMatrix, name):
    # note: only used to export non-Link animation
    skeleton, fModel = mmConvertArmatureToSkeleton(
        originalArmatureObj, convertTransformMatrix, None, name, False, True, "Opaque", False
    )
    return skeleton


def mmConvertArmatureToSkeletonWithMesh(
    originalArmatureObj, convertTransformMatrix, fModel, name, convertTextureData, drawLayer, optimize
):
    return mmConvertArmatureToSkeleton(
        originalArmatureObj, convertTransformMatrix, fModel, name, convertTextureData, False, drawLayer, optimize
    )


def mmConvertArmatureToC(
    originalArmatureObj: bpy.types.Object,
    convertTransformMatrix: mathutils.Matrix,
    DLFormat: DLFormat,
    savePNG: bool,
    drawLayer: str,
    settings: MMSkeletonExportSettings,
):
    if settings.mode != "Generic" and not settings.isCustom:
        importInfo = mmSkeletonImportDict[settings.mode]
        skeletonName = importInfo.skeletonName
        filename = skeletonName
        folderName = importInfo.folderName
        overlayName = importInfo.actorOverlayName
        flipbookUses2DArray = importInfo.flipbookArrayIndex2D is not None
        flipbookArrayIndex2D = importInfo.flipbookArrayIndex2D
        isLink = importInfo.isLink
    else:
        skeletonName = toAlnum(originalArmatureObj.name)
        filename = settings.filename if settings.isCustomFilename else skeletonName
        folderName = settings.folder
        overlayName = settings.actorOverlayName if not settings.isCustom else None
        flipbookUses2DArray = settings.flipbookUses2DArray
        flipbookArrayIndex2D = settings.flipbookArrayIndex2D if flipbookUses2DArray else None
        isLink = False

    exportPath = bpy.path.abspath(settings.customPath)
    isCustomExport = settings.isCustom
    removeVanillaData = settings.removeVanillaData
    optimize = settings.optimize

    fModel = MMModel(skeletonName, DLFormat, drawLayer)
    skeleton, fModel = mmConvertArmatureToSkeletonWithMesh(
        originalArmatureObj, convertTransformMatrix, fModel, skeletonName, not savePNG, drawLayer, optimize
    )

    if originalArmatureObj.mmSkeleton.LOD is not None:
        lodSkeleton, fModel = mmConvertArmatureToSkeletonWithMesh(
            originalArmatureObj.mmSkeleton.LOD,
            convertTransformMatrix,
            fModel,
            skeletonName + "_lod",
            not savePNG,
            drawLayer,
            optimize,
        )
    else:
        lodSkeleton = None

    if lodSkeleton is not None:
        skeleton.hasLOD = True
        limbList = skeleton.createLimbList()
        lodLimbList = lodSkeleton.createLimbList()

        if len(limbList) != len(lodLimbList):
            raise PluginError(
                originalArmatureObj.name
                + " cannot use "
                + originalArmatureObj.mmSkeleton.LOD.name
                + "as LOD because they do not have the same bone structure."
            )

        for i in range(len(limbList)):
            limbList[i].lodDL = lodLimbList[i].DL
            limbList[i].isFlex |= lodLimbList[i].isFlex

    data = CData()
    data.source += '#include "ultra64.h"\n#include "global.h"\n'
    if not isCustomExport:
        data.source += '#include "' + folderName + '.h"\n\n'
    else:
        data.source += "\n"

    path = mmGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, True)
    includeDir = settings.customAssetIncludeDir if settings.isCustom else f"assets/objects/{folderName}"
    exportData = fModel.to_c(
        TextureExportSettings(False, savePNG, includeDir, path), MMGfxFormatter(ScrollMethod.Vertex)
    )
    skeletonC = skeleton.toC()

    data.append(exportData.all())
    data.append(skeletonC)

    if isCustomExport:
        textureArrayData = writeTextureArraysNew(fModel, flipbookArrayIndex2D)
        data.append(textureArrayData)

    writeCData(data, os.path.join(path, filename + ".h"), os.path.join(path, filename + ".c"))

    if not isCustomExport:
        writeTextureArraysExisting(bpy.context.scene.mmDecompPath, overlayName, isLink, flipbookArrayIndex2D, fModel)
        addIncludeFiles(folderName, path, filename)
        if removeVanillaData:
            mmRemoveSkeleton(path, folderName, skeletonName)
