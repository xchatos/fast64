import bpy, math, os, re
from ast import parse, Expression, Num, UnaryOp, USub, Invert, BinOp
from bpy.types import Object
from bpy.utils import register_class, unregister_class
from typing import Callable
from .mm_constants import mmSceneIDToName

from ..utility import (
    PluginError,
    prop_split,
    getDataFromFile,
    saveDataToFile,
    attemptModifierApply,
    setOrigin,
    applyRotation,
    cleanupDuplicatedObjects,
    mmGetSceneOrRoomHeader,
    hexOrDecInt,
    binOps,
)


def isPathObject(obj: bpy.types.Object) -> bool:
    return obj.data is not None and isinstance(obj.data, bpy.types.Curve) and obj.mmSplineProperty.splineType == "Path"


mmSceneDungeons = [
    "bdan",
    "bdan_boss",
    "Bmori1",
    "ddan",
    "ddan_boss",
    "FIRE_bs",
    "ganon",
    "ganontika",
    "ganontikasonogo",
    "ganon_boss",
    "ganon_demo",
    "ganon_final",
    "ganon_sonogo",
    "ganon_tou",
    "gerudoway",
    "HAKAdan",
    "HAKAdanCH",
    "HAKAdan_bs",
    "HIDAN",
    "ice_doukutu",
    "jyasinboss",
    "jyasinzou",
    "men",
    "MIZUsin",
    "MIZUsin_bs",
    "moribossroom",
    "ydan",
    "ydan_boss",
]

mmSceneIndoors = [
    "bowling",
    "daiyousei_izumi",
    "hairal_niwa",
    "hairal_niwa2",
    "hairal_niwa_n",
    "hakasitarelay",
    "hut",
    "hylia_labo",
    "impa",
    "kakariko",
    "kenjyanoma",
    "kokiri_home",
    "kokiri_home3",
    "kokiri_home4",
    "kokiri_home5",
    "labo",
    "link_home",
    "mahouya",
    "malon_stable",
    "miharigoya",
    "nakaniwa",
    "syatekijyou",
    "takaraya",
    "tent",
    "tokinoma",
    "yousei_izumi_tate",
    "yousei_izumi_yoko",
]

mmSceneMisc = [
    "enrui",
    "entra_n",
    "hakaana",
    "hakaana2",
    "hakaana_ouke",
    "hiral_demo",
    "kakariko3",
    "kakusiana",
    "kinsuta",
    "market_alley",
    "market_alley_n",
    "market_day",
    "market_night",
    "market_ruins",
    "shrine",
    "shrine_n",
    "shrine_r",
    "turibori",
]

mmSceneOverworld = [
    "entra",
    "souko",
    "spot00",
    "spot01",
    "spot02",
    "spot03",
    "spot04",
    "spot05",
    "spot06",
    "spot07",
    "spot08",
    "spot09",
    "spot10",
    "spot11",
    "spot12",
    "spot13",
    "spot15",
    "spot16",
    "spot17",
    "spot18",
    "spot20",
]

mmSceneShops = [
    "alley_shop",
    "drag",
    "face_shop",
    "golon",
    "kokiri_shop",
    "night_shop",
    "shop1",
    "zoora",
]

mmSceneTest_levels = [
    "besitu",
    "depth_test",
    "sasatest",
    "sutaru",
    "syotes",
    "syotes2",
    "test01",
    "testroom",
]

mmSceneDirs = {
    "assets/scenes/dungeons/": mmSceneDungeons,
    "assets/scenes/indoors/": mmSceneIndoors,
    "assets/scenes/misc/": mmSceneMisc,
    "assets/scenes/overworld/": mmSceneOverworld,
    "assets/scenes/shops/": mmSceneShops,
    "assets/scenes/test_levels/": mmSceneTest_levels,
}


def sceneNameFromID(sceneID):
    if sceneID in mmSceneIDToName:
        return mmSceneIDToName[sceneID]
    else:
        raise PluginError("Cannot find scene ID " + str(sceneID))


def getMMScale(actorScale: float) -> float:
    return bpy.context.scene.mmBlenderScale * actorScale


def replaceMatchContent(data: str, newContent: str, match: re.Match, index: int) -> str:
    return data[: match.start(index)] + newContent + data[match.end(index) :]


def addIncludeFiles(objectName, objectPath, assetName):
    addIncludeFilesExtension(objectName, objectPath, assetName, "h")
    addIncludeFilesExtension(objectName, objectPath, assetName, "c")


def addIncludeFilesExtension(objectName, objectPath, assetName, extension):
    include = '#include "' + assetName + "." + extension + '"\n'
    if not os.path.exists(objectPath):
        raise PluginError(objectPath + " does not exist.")
    path = os.path.join(objectPath, objectName + "." + extension)
    data = getDataFromFile(path)

    if include not in data:
        data += "\n" + include

    # Save this regardless of modification so it will be recompiled.
    saveDataToFile(path, data)


def getSceneDirFromLevelName(name):
    for sceneDir, dirLevels in mmSceneDirs.items():
        if name in dirLevels:
            return sceneDir + name
    return None


class ExportInfo:
    def __init__(self, isCustomExport, exportPath, customSubPath, name):
        self.isCustomExportPath = isCustomExport
        self.exportPath = exportPath
        self.customSubPath = customSubPath
        self.name = name


class MMObjectCategorizer:
    def __init__(self):
        self.sceneObj = None
        self.roomObjs = []
        self.actors = []
        self.transitionActors = []
        self.meshes = []
        self.entrances = []
        self.waterBoxes = []

    def sortObjects(self, allObjs):
        for obj in allObjs:
            if obj.data is None:
                if obj.mmEmptyType == "Actor":
                    self.actors.append(obj)
                elif obj.mmEmptyType == "Transition Actor":
                    self.transitionActors.append(obj)
                elif obj.mmEmptyType == "Entrance":
                    self.entrances.append(obj)
                elif obj.mmEmptyType == "Water Box":
                    self.waterBoxes.append(obj)
                elif obj.mmEmptyType == "Room":
                    self.roomObjs.append(obj)
                elif obj.mmEmptyType == "Scene":
                    self.sceneObj = obj
            elif isinstance(obj.data, bpy.types.Mesh):
                self.meshes.append(obj)


# This also sets all origins relative to the scene object.
def mmDuplicateHierarchy(obj, ignoreAttr, includeEmpties, objectCategorizer):
    # Duplicate objects to apply scale / modifiers / linked data
    bpy.ops.object.select_all(action="DESELECT")
    mmSelectMeshChildrenOnly(obj, includeEmpties)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    try:
        tempObj = bpy.context.view_layer.objects.active
        allObjs = bpy.context.selected_objects
        bpy.ops.object.make_single_user(obdata=True)

        objectCategorizer.sortObjects(allObjs)
        meshObjs = objectCategorizer.meshes
        bpy.ops.object.select_all(action="DESELECT")
        for selectedObj in meshObjs:
            selectedObj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True, properties=False)

        for selectedObj in meshObjs:
            bpy.ops.object.select_all(action="DESELECT")
            selectedObj.select_set(True)
            bpy.context.view_layer.objects.active = selectedObj
            for modifier in selectedObj.modifiers:
                attemptModifierApply(modifier)
        for selectedObj in meshObjs:
            setOrigin(obj, selectedObj)
        if ignoreAttr is not None:
            for selectedObj in meshObjs:
                if getattr(selectedObj, ignoreAttr):
                    for child in selectedObj.children:
                        bpy.ops.object.select_all(action="DESELECT")
                        child.select_set(True)
                        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
                        selectedObj.parent.select_set(True)
                        bpy.ops.object.parent_set(keep_transform=True)
                    selectedObj.parent = None

        # Assume objects with these types of constraints are parented, and are
        # intended to be parented in-game, i.e. rendered as an extra DL alongside
        # a skeletal mesh, e.g. for a character to be wearing or holding it.
        # In this case we purely want the transformation of the object relative
        # to whatever it's parented to. Getting rid of the constraint and then
        # doing transform_apply() sets up this transformation.
        hasConstraint = False
        for constraint in tempObj.constraints:
            if (
                constraint.type
                in {
                    "COPY_LOCATION",
                    "COPY_ROTATION",
                    "COPY_SCALE",
                    "COPY_TRANSFORMS",
                    "TRANSFORM",
                    "CHILD_OF",
                    "CLAMP_TO",
                    "DAMPED_TRACK",
                    "LOCKED_TRACK",
                    "TRACK_TO",
                }
                and not constraint.mute
            ):
                hasConstraint = True
                tempObj.constraints.remove(constraint)
        if not hasConstraint:
            # For normal objects, the game's coordinate system is 90 degrees
            # away from Blender's.
            applyRotation([tempObj], math.radians(90), "X")
        else:
            # This is a relative transform we care about so the 90 degrees
            # doesn't matter (since they're both right-handed).
            print("Applying transform")
            bpy.ops.object.select_all(action="DESELECT")
            tempObj.select_set(True)
            bpy.context.view_layer.objects.active = tempObj
            bpy.ops.object.transform_apply()

        return tempObj, allObjs
    except Exception as e:
        cleanupDuplicatedObjects(allObjs)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        raise Exception(str(e))


def mmSelectMeshChildrenOnly(obj, includeEmpties):
    isMesh = isinstance(obj.data, bpy.types.Mesh)
    isEmpty = (
        obj.data is None or isinstance(obj.data, bpy.types.Camera) or isinstance(obj.data, bpy.types.Curve)
    ) and includeEmpties
    if isMesh or isEmpty:
        obj.select_set(True)
        obj.original_name = obj.name
    for child in obj.children:
        mmSelectMeshChildrenOnly(child, includeEmpties)


def mmCleanupScene(originalSceneObj, allObjs):
    cleanupDuplicatedObjects(allObjs)
    originalSceneObj.select_set(True)
    bpy.context.view_layer.objects.active = originalSceneObj


def getSceneObj(obj):
    while not (obj is None or (obj is not None and obj.data is None and obj.mmEmptyType == "Scene")):
        obj = obj.parent
    if obj is None:
        return None
    else:
        return obj


def getRoomObj(obj):
    while not (obj is None or (obj is not None and obj.data is None and obj.mmEmptyType == "Room")):
        obj = obj.parent
    if obj is None:
        return None
    else:
        return obj


def checkEmptyName(name):
    if name == "":
        raise PluginError("No name entered for the exporter.")


def mmGetObjectPath(isCustomExport, exportPath, folderName):
    if isCustomExport:
        filepath = exportPath
    else:
        filepath = os.path.join(
            mmGetPath(exportPath, isCustomExport, "assets/objects/", folderName, False, False), folderName + ".c"
        )
    return filepath


def mmGetPath(exportPath, isCustomExport, subPath, folderName, makeIfNotExists, useFolderForCustom):
    if isCustomExport:
        path = bpy.path.abspath(os.path.join(exportPath, (folderName if useFolderForCustom else "")))
    else:
        if bpy.context.scene.mmDecompPath == "":
            raise PluginError("Decomp base path is empty.")
        path = bpy.path.abspath(os.path.join(os.path.join(bpy.context.scene.mmDecompPath, subPath), folderName))

    if not os.path.exists(path):
        if isCustomExport or makeIfNotExists:
            os.makedirs(path)
        else:
            raise PluginError(path + " does not exist.")

    return path


def getSortedChildren(armatureObj, bone):
    return sorted(
        [child.name for child in bone.children if child.mmBone.boneType != "Ignore"],
        key=lambda childName: childName.lower(),
    )


def getStartBone(armatureObj):
    startBoneNames = [
        bone.name for bone in armatureObj.data.bones if bone.parent is None and bone.mmBone.boneType != "Ignore"
    ]
    if len(startBoneNames) == 0:
        raise PluginError(armatureObj.name + ' does not have any root bones that are not of the "Ignore" type.')
    startBoneName = startBoneNames[0]
    return startBoneName
    # return 'root'


def getNextBone(boneStack: list[str], armatureObj: bpy.types.Object):
    if len(boneStack) == 0:
        raise PluginError("More bones in animation than on armature.")
    bone = armatureObj.data.bones[boneStack[0]]
    boneStack = boneStack[1:]
    boneStack = getSortedChildren(armatureObj, bone) + boneStack
    return bone, boneStack


def checkForStartBone(armatureObj):
    pass
    # if "root" not in armatureObj.data.bones:
    # 	raise PluginError("Skeleton must have a bone named 'root' where the skeleton starts from.")


class BoxEmpty:
    def __init__(self, position, scale, emptyScale):
        # The scale ordering is due to the fact that scaling happens AFTER rotation.
        # Thus the translation uses Y-up, while the scale uses Z-up.
        self.low = (position[0] - scale[0] * emptyScale, position[2] - scale[1] * emptyScale)
        self.high = (position[0] + scale[0] * emptyScale, position[2] + scale[1] * emptyScale)
        self.height = position[1] + scale[2] * emptyScale

        self.low = [int(round(value)) for value in self.low]
        self.high = [int(round(value)) for value in self.high]
        self.height = int(round(self.height))


def checkUniformScale(scale, obj):
    if abs(scale[0] - scale[1]) > 0.01 or abs(scale[1] - scale[2]) > 0.01 or abs(scale[0] - scale[2]) > 0.01:
        raise PluginError("Cull group " + obj.name + " must have a uniform scale.")


class CullGroup:
    def __init__(self, position, scale, emptyScale):
        self.position = [int(round(field)) for field in position]
        self.cullDepth = abs(int(round(scale[0] * emptyScale)))


def setCustomProperty(data: any, prop: str, value: str, enumList: list[tuple[str, str, str]] | None):
    if enumList is not None:
        if value in [enumItem[0] for enumItem in enumList]:
            setattr(data, prop, value)
            return
        else:
            try:
                numberValue = hexOrDecInt(value)
                hexValue = f'0x{format(numberValue, "02X")}'
                if hexValue in [enumItem[0] for enumItem in enumList]:
                    setattr(data, prop, hexValue)
                    return
            except ValueError:
                pass

    setattr(data, prop, "Custom")
    setattr(data, prop + str("Custom"), value)


def getCustomProperty(data, prop):
    value = getattr(data, prop)
    return value if value != "Custom" else getattr(data, prop + str("Custom"))


def convertIntTo2sComplement(value, length, signed):
    return int.from_bytes(int(round(value)).to_bytes(length, "big", signed=signed), "big")


def drawEnumWithCustom(panel, data, attribute, name, customName):
    prop_split(panel, data, attribute, name)
    if getattr(data, attribute) == "Custom":
        prop_split(panel, data, attribute + "Custom", customName)


def getEnumName(enumItems, value):
    for enumTuple in enumItems:
        if enumTuple[0] == value:
            return enumTuple[1]
    raise PluginError("Could not find enum value " + str(value))


def getEnumIndex(enumItems, value):
    for i, enumTuple in enumerate(enumItems):
        if enumTuple[0] == value or enumTuple[1] == value:
            return i
    return None


def mmConvertTranslation(translation):
    return [int(round(value)) for value in translation]


def mmConvertRotation(rotation):
    # see BINANG_TO_DEGF
    return [int(round((math.degrees(value) % 360) / 360 * (2**16))) % (2**16) for value in rotation.to_euler()]


# parse rotaion in Vec3s format
def mmParseRotation(values: list[int]):
    return [
        math.radians(
            (int.from_bytes(value.to_bytes(2, "big", signed=value < 0x8000), "big", signed=False) / 2**16) * 360
        )
        for value in values
    ]


def getCutsceneName(obj):
    name = obj.name
    if name.startswith("Cutscene."):
        name = name[9:]
    name = name.replace(".", "_")
    return name


def getCollectionFromIndex(obj, prop, subIndex, isRoom):
    header = mmGetSceneOrRoomHeader(obj, subIndex, isRoom)
    return getattr(header, prop)


# Operators cannot store mutable references (?), so to reuse PropertyCollection modification code we do this.
# Save a string identifier in the operator, then choose the member variable based on that.
# subIndex is for a collection within a collection element
def getCollection(objName, collectionType, subIndex):
    obj = bpy.data.objects[objName]
    if collectionType == "Actor":
        collection = obj.mmActorProperty.headerSettings.cutsceneHeaders
    elif collectionType == "Transition Actor":
        collection = obj.mmTransitionActorProperty.actor.headerSettings.cutsceneHeaders
    elif collectionType == "Entrance":
        collection = obj.mmEntranceProperty.actor.headerSettings.cutsceneHeaders
    elif collectionType == "Room":
        collection = obj.mmAlternateRoomHeaders.cutsceneHeaders
    elif collectionType == "Scene":
        collection = obj.mmAlternateSceneHeaders.cutsceneHeaders
    elif collectionType == "Light":
        collection = getCollectionFromIndex(obj, "lightList", subIndex, False)
    elif collectionType == "Exit":
        collection = getCollectionFromIndex(obj, "exitList", subIndex, False)
    elif collectionType == "Object":
        collection = getCollectionFromIndex(obj, "objectList", subIndex, True)
    elif collectionType == "Curve":
        collection = obj.mmSplineProperty.headerSettings.cutsceneHeaders
    elif collectionType.startswith("CSHdr."):
        # CSHdr.HeaderNumber[.ListType]
        # Specifying ListType means uses subIndex
        toks = collectionType.split(".")
        assert len(toks) in [2, 3]
        hdrnum = int(toks[1])
        collection = getCollectionFromIndex(obj, "csLists", hdrnum, False)
        if len(toks) == 3:
            collection = getattr(collection[subIndex], toks[2])
    elif collectionType.startswith("Cutscene."):
        # Cutscene.ListType
        toks = collectionType.split(".")
        assert len(toks) == 2
        collection = obj.mmCutsceneProperty.csLists
        collection = getattr(collection[subIndex], toks[1])
    elif collectionType == "Cutscene":
        collection = obj.mmCutsceneProperty.csLists
    elif collectionType == "extraCutscenes":
        collection = obj.mmSceneHeader.extraCutscenes
    elif collectionType == "BgImage":
        collection = obj.mmRoomHeader.bgImageList
    else:
        raise PluginError("Invalid collection type: " + collectionType)

    return collection


def drawAddButton(layout, index, collectionType, subIndex, objName):
    if subIndex is None:
        subIndex = 0
    addOp = layout.operator(MMCollectionAdd.bl_idname)
    addOp.option = index
    addOp.collectionType = collectionType
    addOp.subIndex = subIndex
    addOp.objName = objName


def drawCollectionOps(layout, index, collectionType, subIndex, objName, allowAdd=True, compact=False):
    if subIndex is None:
        subIndex = 0

    if not compact:
        buttons = layout.row(align=True)
    else:
        buttons = layout

    if allowAdd:
        addOp = buttons.operator(MMCollectionAdd.bl_idname, text="Add" if not compact else "", icon="ADD")
        addOp.option = index + 1
        addOp.collectionType = collectionType
        addOp.subIndex = subIndex
        addOp.objName = objName

    removeOp = buttons.operator(MMCollectionRemove.bl_idname, text="Delete" if not compact else "", icon="REMOVE")
    removeOp.option = index
    removeOp.collectionType = collectionType
    removeOp.subIndex = subIndex
    removeOp.objName = objName

    moveUp = buttons.operator(MMCollectionMove.bl_idname, text="Up" if not compact else "", icon="TRIA_UP")
    moveUp.option = index
    moveUp.offset = -1
    moveUp.collectionType = collectionType
    moveUp.subIndex = subIndex
    moveUp.objName = objName

    moveDown = buttons.operator(MMCollectionMove.bl_idname, text="Down" if not compact else "", icon="TRIA_DOWN")
    moveDown.option = index
    moveDown.offset = 1
    moveDown.collectionType = collectionType
    moveDown.subIndex = subIndex
    moveDown.objName = objName


class MMCollectionAdd(bpy.types.Operator):
    bl_idname = "object.mm_collection_add"
    bl_label = "Add Item"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty()
    collectionType: bpy.props.StringProperty(default="Actor")
    subIndex: bpy.props.IntProperty(default=0)
    objName: bpy.props.StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)

        collection.add()
        collection.move(len(collection) - 1, self.option)
        return {"FINISHED"}


class MMCollectionRemove(bpy.types.Operator):
    bl_idname = "object.mm_collection_remove"
    bl_label = "Remove Item"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty()
    collectionType: bpy.props.StringProperty(default="Actor")
    subIndex: bpy.props.IntProperty(default=0)
    objName: bpy.props.StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)
        collection.remove(self.option)
        return {"FINISHED"}


class MMCollectionMove(bpy.types.Operator):
    bl_idname = "object.mm_collection_move"
    bl_label = "Move Item"
    bl_options = {"REGISTER", "UNDO"}

    option: bpy.props.IntProperty()
    offset: bpy.props.IntProperty()
    subIndex: bpy.props.IntProperty(default=0)
    objName: bpy.props.StringProperty()

    collectionType: bpy.props.StringProperty(default="Actor")

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.subIndex)
        collection.move(self.option, self.option + self.offset)
        return {"FINISHED"}


def getHeaderSettings(actorObj: bpy.types.Object):
    itemType = actorObj.mmEmptyType
    if actorObj.data is None:
        if itemType == "Actor":
            headerSettings = actorObj.mmActorProperty.headerSettings
        elif itemType == "Entrance":
            headerSettings = actorObj.mmEntranceProperty.actor.headerSettings
        elif itemType == "Transition Actor":
            headerSettings = actorObj.mmTransitionActorProperty.actor.headerSettings
        else:
            headerSettings = None
    elif actorObj.data is not None and isPathObject(actorObj):
        headerSettings = actorObj.mmSplineProperty.headerSettings
    else:
        headerSettings = None

    return headerSettings


mm_utility_classes = (
    MMCollectionAdd,
    MMCollectionRemove,
    MMCollectionMove,
)


def mm_utility_register():
    for cls in mm_utility_classes:
        register_class(cls)


def mm_utility_unregister():
    for cls in reversed(mm_utility_classes):
        unregister_class(cls)


def getActiveHeaderIndex() -> int:
    # All scenes/rooms should have synchronized tabs from property callbacks
    headerObjs = [obj for obj in bpy.data.objects if obj.mmEmptyType == "Scene" or obj.mmEmptyType == "Room"]
    if len(headerObjs) == 0:
        return 0

    headerObj = headerObjs[0]
    if headerObj.mmEmptyType == "Scene":
        header = headerObj.mmSceneHeader
        altHeader = headerObj.mmAlternateSceneHeaders
    else:
        header = headerObj.mmRoomHeader
        altHeader = headerObj.mmAlternateRoomHeaders

    if header.menuTab != "Alternate":
        headerIndex = 0
    else:
        if altHeader.headerMenuTab == "Child Night":
            headerIndex = 1
        elif altHeader.headerMenuTab == "Adult Day":
            headerIndex = 2
        elif altHeader.headerMenuTab == "Adult Night":
            headerIndex = 3
        else:
            headerIndex = altHeader.currentCutsceneIndex

    return (
        headerIndex,
        altHeader.childNightHeader.usePreviousHeader,
        altHeader.adultDayHeader.usePreviousHeader,
        altHeader.adultNightHeader.usePreviousHeader,
    )


def setAllActorsVisibility(self, context: bpy.types.Context):
    activeHeaderInfo = getActiveHeaderIndex()

    actorObjs = [
        obj
        for obj in bpy.data.objects
        if obj.mmEmptyType in ["Actor", "Transition Actor", "Entrance"] or isPathObject(obj)
    ]

    for actorObj in actorObjs:
        setActorVisibility(actorObj, activeHeaderInfo)


def setActorVisibility(actorObj: bpy.types.Object, activeHeaderInfo: tuple[int, bool, bool, bool]):
    headerIndex, childNightHeader, adultDayHeader, adultNightHeader = activeHeaderInfo
    usePreviousHeader = [False, childNightHeader, adultDayHeader, adultNightHeader]
    if headerIndex < 4:
        while usePreviousHeader[headerIndex]:
            headerIndex -= 1

    headerSettings = getHeaderSettings(actorObj)
    if headerSettings is None:
        return
    if headerSettings.sceneSetupPreset == "All Scene Setups":
        actorObj.hide_set(False)
    elif headerSettings.sceneSetupPreset == "All Non-Cutscene Scene Setups":
        actorObj.hide_set(headerIndex >= 4)
    elif headerSettings.sceneSetupPreset == "Custom":
        actorObj.hide_set(not headerSettings.checkHeader(headerIndex))
    else:
        print("Error: unhandled header case")


def onMenuTabChange(self, context: bpy.types.Context):
    def callback(thisHeader, otherObj: bpy.types.Object):
        if otherObj.mmEmptyType == "Scene":
            header = otherObj.mmSceneHeader
        else:
            header = otherObj.mmRoomHeader

        if thisHeader.menuTab != "Alternate" and header.menuTab == "Alternate":
            header.menuTab = "General"
        if thisHeader.menuTab == "Alternate" and header.menuTab != "Alternate":
            header.menuTab = "Alternate"

    onHeaderPropertyChange(self, context, callback)


def onHeaderMenuTabChange(self, context: bpy.types.Context):
    def callback(thisHeader, otherObj: bpy.types.Object):
        if otherObj.mmEmptyType == "Scene":
            header = otherObj.mmAlternateSceneHeaders
        else:
            header = otherObj.mmAlternateRoomHeaders

        header.headerMenuTab = thisHeader.headerMenuTab
        header.currentCutsceneIndex = thisHeader.currentCutsceneIndex

    onHeaderPropertyChange(self, context, callback)


def onHeaderPropertyChange(self, context: bpy.types.Context, callback: Callable[[any, bpy.types.Object], None]):
    if not bpy.context.scene.fast64.mm.headerTabAffectsVisibility or bpy.context.scene.mmActiveHeaderLock:
        return
    bpy.context.scene.mmActiveHeaderLock = True

    thisHeader = self
    thisObj = context.object
    otherObjs = [
        obj
        for obj in bpy.data.objects
        if (obj.mmEmptyType == "Scene" or obj.mmEmptyType == "Room") and obj != thisObj
    ]

    for otherObj in otherObjs:
        callback(thisHeader, otherObj)

    setAllActorsVisibility(self, context)

    bpy.context.scene.mmActiveHeaderLock = False


def getEvalParams(input: str):
    """Evaluates a string to an hexadecimal number"""

    # degrees to binary angle conversion
    if "DEG_TO_BINANG(" in input:
        input = input.strip().removeprefix("DEG_TO_BINANG(").removesuffix(")").strip()
        return f"0x{round(float(input) * (0x8000 / 180)):X}"

    if input is None or "None" in input:
        return "0x0"

    # remove spaces
    input = input.strip()

    try:
        node = parse(input, mode="eval")
    except Exception as e:
        raise ValueError(f"Could not parse {input} as an AST.") from e

    def _eval(node):
        if isinstance(node, Expression):
            return _eval(node.body)
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, UnaryOp):
            if isinstance(node.op, USub):
                return -_eval(node.operand)
            elif isinstance(node.op, Invert):
                return ~_eval(node.operand)
            else:
                raise ValueError(f"Unsupported unary operator {node.op}")
        elif isinstance(node, BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise ValueError(f"Unsupported AST node {node}")

    return f"0x{_eval(node.body):X}"
