import mathutils, bpy, math
from ....f3d.f3d_gbi import F3D, get_F3D_GBI
from ....f3d.f3d_parser import getImportData, parseF3D
from ....utility import hexOrDecInt, applyRotation
from ...mm_f3d_writer import mmReadActorScale
from ...mm_model_classes import MMF3DContext, mmGetIncludedAssetData
from ...mm_utility import mmGetObjectPath, getMMScale
from ...mm_texture_array import mmReadTextureArrays
from ..constants import mmSkeletonImportDict
from ..properties import MMSkeletonImportSettings
from ..utility import mmGetLimb, mmGetLimbs, mmGetSkeleton, applySkeletonRestPose


class MMDLEntry:
    def __init__(self, dlName, limbIndex):
        self.dlName = dlName
        self.limbIndex = limbIndex


def mmAddBone(armatureObj, boneName, parentBoneName, currentTransform, loadDL):
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode="EDIT")
    bone = armatureObj.data.edit_bones.new(boneName)
    bone.use_connect = False
    bone.use_deform = loadDL
    if parentBoneName is not None:
        bone.parent = armatureObj.data.edit_bones[parentBoneName]
    bone.head = currentTransform @ mathutils.Vector((0, 0, 0))
    bone.tail = bone.head + (currentTransform.to_quaternion() @ mathutils.Vector((0, 0.3, 0)))

    # Connect bone to parent if it is possible without changing parent direction.

    if parentBoneName is not None:
        nodeOffsetVector = mathutils.Vector(bone.head - bone.parent.head)
        # set fallback to nonzero to avoid creating zero length bones
        if nodeOffsetVector.angle(bone.parent.tail - bone.parent.head, 1) < 0.0001 and loadDL:
            for child in bone.parent.children:
                if child != bone:
                    child.use_connect = False
            bone.parent.tail = bone.head
            bone.use_connect = True
        elif bone.head == bone.parent.head and bone.tail == bone.parent.tail:
            bone.tail += currentTransform.to_quaternion() @ mathutils.Vector((0, 0.2, 0))

    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")


def mmAddLimbRecursively(
    limbIndex: int,
    skeletonData: str,
    obj: bpy.types.Object,
    armatureObj: bpy.types.Object,
    parentTransform: mathutils.Matrix,
    parentBoneName: str,
    f3dContext: MMF3DContext,
    useFarLOD: bool,
):
    limbName = f3dContext.getLimbName(limbIndex)
    boneName = f3dContext.getBoneName(limbIndex)
    matchResult = mmGetLimb(skeletonData, limbName, False)

    isLOD = matchResult.lastindex > 6

    if isLOD and useFarLOD:
        dlName = matchResult.group(7)
    else:
        dlName = matchResult.group(6)

    # Animations override the root translation, so we just ignore importing them as well.
    if limbIndex == 0:
        translation = [0, 0, 0]
    else:
        translation = [
            hexOrDecInt(matchResult.group(1)),
            hexOrDecInt(matchResult.group(2)),
            hexOrDecInt(matchResult.group(3)),
        ]

    LIMB_DONE = 0xFF
    nextChildIndexStr = matchResult.group(4)
    nextChildIndex = LIMB_DONE if nextChildIndexStr == "LIMB_DONE" else hexOrDecInt(nextChildIndexStr)
    nextSiblingIndexStr = matchResult.group(5)
    nextSiblingIndex = LIMB_DONE if nextSiblingIndexStr == "LIMB_DONE" else hexOrDecInt(nextSiblingIndexStr)

    # str(limbIndex) + " " + str(translation) + " " + str(nextChildIndex) + " " + \
    # 	str(nextSiblingIndex) + " " + str(dlName))

    currentTransform = parentTransform @ mathutils.Matrix.Translation(mathutils.Vector(translation))
    f3dContext.matrixData[limbName] = currentTransform
    loadDL = dlName != "NULL"

    mmAddBone(armatureObj, boneName, parentBoneName, currentTransform, loadDL)

    # DLs can access bone transforms not yet processed.
    # Therefore were delay F3D parsing until after skeleton is processed.
    if loadDL:
        f3dContext.dlList.append(MMDLEntry(dlName, limbIndex))

    if nextChildIndex != LIMB_DONE:
        isLOD |= mmAddLimbRecursively(
            nextChildIndex, skeletonData, obj, armatureObj, currentTransform, boneName, f3dContext, useFarLOD
        )

    if nextSiblingIndex != LIMB_DONE:
        isLOD |= mmAddLimbRecursively(
            nextSiblingIndex, skeletonData, obj, armatureObj, parentTransform, parentBoneName, f3dContext, useFarLOD
        )

    return isLOD


def mmBuildSkeleton(
    skeletonName,
    overlayName,
    skeletonData,
    actorScale,
    removeDoubles,
    importNormals,
    useFarLOD,
    basePath,
    drawLayer,
    isLink,
    flipbookArrayIndex2D: int,
    f3dContext: MMF3DContext,
):
    lodString = "_lod" if useFarLOD else ""

    # Create new skinned mesh
    mesh = bpy.data.meshes.new(skeletonName + "_mesh" + lodString)
    obj = bpy.data.objects.new(skeletonName + "_mesh" + lodString, mesh)
    bpy.context.scene.collection.objects.link(obj)

    # Create new armature
    armature = bpy.data.armatures.new(skeletonName + lodString)
    armatureObj = bpy.data.objects.new(skeletonName + lodString, armature)
    armatureObj.show_in_front = True
    armatureObj.mmDrawLayer = drawLayer
    # armature.show_names = True

    bpy.context.scene.collection.objects.link(armatureObj)
    bpy.context.view_layer.objects.active = armatureObj
    # bpy.ops.object.mode_set(mode = 'EDIT')

    f3dContext.mat().draw_layer.mm = armatureObj.mmDrawLayer

    if overlayName is not None:
        mmReadTextureArrays(basePath, overlayName, skeletonName, f3dContext, isLink, flipbookArrayIndex2D)

    transformMatrix = mathutils.Matrix.Scale(1 / actorScale, 4)
    isLOD = mmAddLimbRecursively(0, skeletonData, obj, armatureObj, transformMatrix, None, f3dContext, useFarLOD)
    for dlEntry in f3dContext.dlList:
        limbName = f3dContext.getLimbName(dlEntry.limbIndex)
        boneName = f3dContext.getBoneName(dlEntry.limbIndex)
        parseF3D(
            skeletonData,
            dlEntry.dlName,
            f3dContext.matrixData[limbName],
            limbName,
            boneName,
            "mm",
            drawLayer,
            f3dContext,
            True,
        )
        if f3dContext.isBillboard:
            armatureObj.data.bones[boneName].mmBone.dynamicTransform.billboard = True
    f3dContext.createMesh(obj, removeDoubles, importNormals, False)
    armatureObj.location = bpy.context.scene.cursor.location

    # Set bone rotation mode.
    bpy.ops.object.select_all(action="DESELECT")
    armatureObj.select_set(True)
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode="POSE")
    for bone in armatureObj.pose.bones:
        bone.rotation_mode = "XYZ"

    # Apply mesh to armature.
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    armatureObj.select_set(True)
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.parent_set(type="ARMATURE")

    applyRotation([armatureObj], math.radians(-90), "X")
    armatureObj.mmActorScale = actorScale / bpy.context.scene.mmBlenderScale

    return isLOD, armatureObj


def mmImportSkeletonC(basePath: str, importSettings: MMSkeletonImportSettings):
    importPath = bpy.path.abspath(importSettings.customPath)
    isCustomImport = importSettings.isCustom

    if importSettings.mode != "Generic" and not importSettings.isCustom:
        importInfo = mmSkeletonImportDict[importSettings.mode]
        skeletonName = importInfo.skeletonName
        folderName = importInfo.folderName
        overlayName = importInfo.actorOverlayName
        flipbookUses2DArray = importInfo.flipbookArrayIndex2D is not None
        flipbookArrayIndex2D = importInfo.flipbookArrayIndex2D
        isLink = importInfo.isLink
        restPoseData = importInfo.restPoseData
    else:
        skeletonName = importSettings.name
        folderName = importSettings.folder
        overlayName = importSettings.actorOverlayName if not importSettings.isCustom else None
        flipbookUses2DArray = importSettings.flipbookUses2DArray
        flipbookArrayIndex2D = importSettings.flipbookArrayIndex2D if flipbookUses2DArray else None
        isLink = False
        restPoseData = None

    filepaths = [mmGetObjectPath(isCustomImport, importPath, folderName)]

    removeDoubles = importSettings.removeDoubles
    importNormals = importSettings.importNormals
    drawLayer = importSettings.drawLayer

    skeletonData = getImportData(filepaths)
    if overlayName is not None or isLink:
        skeletonData = mmGetIncludedAssetData(basePath, filepaths, skeletonData) + skeletonData

    matchResult = mmGetSkeleton(skeletonData, skeletonName, False)
    limbsName = matchResult.group(2)

    matchResult = mmGetLimbs(skeletonData, limbsName, False)
    limbsData = matchResult.group(2)
    limbList = [entry.strip()[1:] for entry in limbsData.split(",") if entry.strip() != ""]

    f3dContext = MMF3DContext(get_F3D_GBI(), limbList, basePath)
    f3dContext.mat().draw_layer.mm = drawLayer

    if overlayName is not None and importSettings.autoDetectActorScale:
        actorScale = mmReadActorScale(basePath, overlayName, isLink)
    else:
        actorScale = getMMScale(importSettings.actorScale)

    # print(limbList)
    isLOD, armatureObj = mmBuildSkeleton(
        skeletonName,
        overlayName,
        skeletonData,
        actorScale,
        removeDoubles,
        importNormals,
        False,
        basePath,
        drawLayer,
        isLink,
        flipbookArrayIndex2D,
        f3dContext,
    )
    if isLOD:
        isLOD, LODArmatureObj = mmBuildSkeleton(
            skeletonName,
            overlayName,
            skeletonData,
            actorScale,
            removeDoubles,
            importNormals,
            True,
            basePath,
            drawLayer,
            isLink,
            flipbookArrayIndex2D,
            f3dContext,
        )
        armatureObj.mmSkeleton.LOD = LODArmatureObj
        LODArmatureObj.location += mathutils.Vector((10, 0, 0))

    f3dContext.deleteMaterialContext()

    if importSettings.applyRestPose and restPoseData is not None:
        applySkeletonRestPose(restPoseData, armatureObj)
        if isLOD:
            applySkeletonRestPose(restPoseData, LODArmatureObj)
