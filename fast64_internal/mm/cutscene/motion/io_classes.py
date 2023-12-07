import bpy

from dataclasses import dataclass, field
from bpy.types import Object
from ...mm_constants import mmData
from .utility import getBlenderPosition, getBlenderRotation


# NOTE: ``paramNumber`` is the expected number of parameters inside the parsed commands,
# this account for the unused parameters. Every classes are based on the commands arguments from ``z64cutscene_commands.h``


@dataclass
class MMCSMotionBase:
    """This class contains common Cutscene data"""

    startFrame: int
    endFrame: int


@dataclass
class MMCSMotionCamPoint:
    """This class contains a single Camera Point command data"""

    continueFlag: str
    camRoll: int
    frame: int
    viewAngle: float
    pos: list[int, int, int]
    paramNumber: int = 8


@dataclass
class MMCSMotionActorCue(MMCSMotionBase):
    """This class contains a single Actor Cue command data"""

    actionID: int
    rot: list[str, str, str]
    startPos: list[int, int, int]
    endPos: list[int, int, int]
    paramNumber: int = 15


@dataclass
class MMCSMotionActorCueList:
    """This class contains the Actor Cue List command data"""

    commandType: str
    entryTotal: int
    entries: list[MMCSMotionActorCue] = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamEyeSpline(MMCSMotionBase):
    """This class contains the Camera Eye Spline data"""

    entries: list[MMCSMotionCamPoint] = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamATSpline(MMCSMotionBase):
    """This class contains the Camera AT (look-at) Spline data"""

    entries: list[MMCSMotionCamPoint] = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamEyeSplineRelToPlayer(MMCSMotionBase):
    """This class contains the Camera Eye Spline Relative to the Player data"""

    entries: list[MMCSMotionCamPoint] = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamATSplineRelToPlayer(MMCSMotionBase):
    """This class contains the Camera AT Spline Relative to the Player data"""

    entries: list[MMCSMotionCamPoint] = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamEye(MMCSMotionBase):
    """This class contains a single Camera Eye point"""

    # This feature is not used in the final game and lacks polish, it is recommended to use splines in all cases.
    entries: list = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionCamAT(MMCSMotionBase):
    """This class contains a single Camera AT point"""

    # This feature is not used in the final game and lacks polish, it is recommended to use splines in all cases.
    entries: list = field(default_factory=list)
    paramNumber: int = 2


@dataclass
class MMCSMotionMisc(MMCSMotionBase):
    """This class contains a single misc command entry"""

    type: str  # see ``CutsceneMiscType`` in decomp
    paramNumber: int = 14


@dataclass
class MMCSMotionMiscList:
    """This class contains Misc command data"""

    entryTotal: int
    entries: list[MMCSMotionMisc] = field(default_factory=list)
    paramNumber: int = 1


@dataclass
class MMCSMotionTransition(MMCSMotionBase):
    """This class contains Transition command data"""

    type: str
    paramNumber: int = 3


@dataclass
class MMCSMotionCutscene:
    """This class contains a Cutscene's data, including every commands' data"""

    name: str
    totalEntries: int
    frameCount: int
    paramNumber: int = 2

    actorCueList: list[MMCSMotionActorCueList] = field(default_factory=list)
    playerCueList: list[MMCSMotionActorCueList] = field(default_factory=list)
    camEyeSplineList: list[MMCSMotionCamEyeSpline] = field(default_factory=list)
    camATSplineList: list[MMCSMotionCamATSpline] = field(default_factory=list)
    camEyeSplineRelPlayerList: list[MMCSMotionCamEyeSplineRelToPlayer] = field(default_factory=list)
    camATSplineRelPlayerList: list[MMCSMotionCamATSplineRelToPlayer] = field(default_factory=list)
    camEyeList: list[MMCSMotionCamEye] = field(default_factory=list)
    camATList: list[MMCSMotionCamAT] = field(default_factory=list)
    miscList: list[MMCSMotionMiscList] = field(default_factory=list)
    transitionList: list[MMCSMotionTransition] = field(default_factory=list)


class MMCSMotionObjectFactory:
    """This class contains functions to create new Blender objects"""

    def getNewObject(self, name: str, data, selectObject: bool, parentObj: Object) -> Object:
        newObj = bpy.data.objects.new(name=name, object_data=data)
        bpy.context.view_layer.active_layer_collection.collection.objects.link(newObj)
        if selectObject:
            newObj.select_set(True)
            bpy.context.view_layer.objects.active = newObj
        newObj.parent = parentObj
        newObj.location = [0.0, 0.0, 0.0]
        newObj.rotation_euler = [0.0, 0.0, 0.0]
        newObj.scale = [1.0, 1.0, 1.0]
        return newObj

    def getNewEmptyObject(self, name: str, selectObject: bool, parentObj: Object):
        return self.getNewObject(name, None, selectObject, parentObj)

    def getNewArmatureObject(self, name: str, selectObject: bool, parentObj: Object):
        newArmatureData = bpy.data.armatures.new(name)
        newArmatureData.display_type = "STICK"
        newArmatureData.show_names = True
        newArmatureObject = self.getNewObject(name, newArmatureData, selectObject, parentObj)
        return newArmatureObject

    def getNewCutsceneObject(self, name: str, frameCount: int, parentObj: Object):
        newCSObj = self.getNewEmptyObject(name, True, parentObj)
        newCSObj.mmEmptyType = "Cutscene"
        newCSObj.mmCutsceneProperty.csEndFrame = frameCount
        return newCSObj

    def getNewActorCueListObject(self, name: str, commandType: str, parentObj: Object):
        newActorCueListObj = self.getNewEmptyObject(name, False, parentObj)
        newActorCueListObj.mmEmptyType = f"CS {'Player' if 'Player' in name else 'Actor'} Cue List"
        cmdEnum = mmData.enumData.enumByKey["csCmd"]

        if commandType == "Player":
            commandType = "player_cue"

        index = cmdEnum.itemByKey[commandType].index if commandType in cmdEnum.itemByKey else int(commandType, base=16)
        item = cmdEnum.itemByIndex.get(index)

        if item is not None:
            newActorCueListObj.mmCSMotionProperty.actorCueListProp.commandType = item.key
        else:
            newActorCueListObj.mmCSMotionProperty.actorCueListProp.commandType = "Custom"
            newActorCueListObj.mmCSMotionProperty.actorCueListProp.commandTypeCustom = commandType

        return newActorCueListObj

    def getNewActorCueObject(
        self,
        name: str,
        startFrame: int,
        actionID: int | str,
        location: list[int],
        rot: list[str],
        parentObj: Object,
    ):
        isDummy = "(D)" in name
        isPlayer = not isDummy and not "Actor" in name

        newActorCueObj = self.getNewEmptyObject(name, False, parentObj)
        newActorCueObj.location = getBlenderPosition(location, bpy.context.scene.mmBlenderScale)
        newActorCueObj.empty_display_type = "ARROWS"
        newActorCueObj.rotation_mode = "XZY"
        newActorCueObj.rotation_euler = getBlenderRotation(rot)
        emptyType = "Dummy" if isDummy else "Player" if isPlayer else "Actor"
        newActorCueObj.mmEmptyType = f"CS {emptyType} Cue"
        newActorCueObj.mmCSMotionProperty.actorCueProp.cueStartFrame = startFrame

        item = None
        if isPlayer:
            playerEnum = mmData.enumData.enumByKey["csPlayerCueId"]
            if isinstance(actionID, int):
                item = playerEnum.itemByIndex.get(actionID)
            else:
                item = playerEnum.itemByKey.get(actionID)

        if item is not None:
            newActorCueObj.mmCSMotionProperty.actorCueProp.playerCueID = item.key
        elif not isDummy:
            if isPlayer:
                newActorCueObj.mmCSMotionProperty.actorCueProp.playerCueID = "Custom"

            if isinstance(actionID, int):
                cueActionID = f"0x{actionID:04X}"
            else:
                cueActionID = actionID

            newActorCueObj.mmCSMotionProperty.actorCueProp.cueActionID = cueActionID

        return newActorCueObj

    def getNewCameraObject(
        self, name: str, displaySize: float, clipStart: float, clipEnd: float, alpha: float, parentObj: Object
    ):
        newCamera = bpy.data.cameras.new(name)
        newCameraObj = self.getNewObject(name, newCamera, False, parentObj)
        newCameraObj.data.display_size = displaySize
        newCameraObj.data.clip_start = clipStart
        newCameraObj.data.clip_end = clipEnd
        newCameraObj.data.passepartout_alpha = alpha
        return newCameraObj

    def getNewActorCuePreviewObject(self, name: str, selectObject, parentObj: Object):
        newPreviewObj = self.getNewEmptyObject(name, selectObject, parentObj)
        newPreviewObj.mmEmptyType = f"CS {'Actor' if 'Actor' in name else 'Player'} Cue Preview"
        return newPreviewObj
