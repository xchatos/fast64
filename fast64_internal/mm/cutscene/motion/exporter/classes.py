import math
import bpy

from dataclasses import dataclass
from bpy.types import Object
from .....utility import PluginError, indent
from ....mm_constants import mmData

from ..io_classes import (
    MMCSMotionActorCueList,
    MMCSMotionActorCue,
    MMCSMotionCamEyeSpline,
    MMCSMotionCamATSpline,
    MMCSMotionCamEyeSplineRelToPlayer,
    MMCSMotionCamATSplineRelToPlayer,
    MMCSMotionCamEye,
    MMCSMotionCamAT,
    MMCSMotionCamPoint,
)


class MMCSMotionExportCommands:
    """This class contains functions to create the cutscene commands"""

    def getActorCueListCmd(self, actorCueList: MMCSMotionActorCueList, isPlayerActor: bool):
        return indent + (
            f"CS_{'PLAYER' if isPlayerActor else 'ACTOR'}_CUE_LIST("
            + f"{actorCueList.commandType + ', ' if not isPlayerActor else ''}"
            + f"{actorCueList.entryTotal}),\n"
        )

    def getActorCueCmd(self, actorCue: MMCSMotionActorCue, isPlayerActor: bool):
        return indent * 2 + (
            f"CS_{'PLAYER' if isPlayerActor else 'ACTOR'}_CUE("
            + f"{actorCue.actionID}, {actorCue.startFrame}, {actorCue.endFrame}, "
            + "".join(f"{rot}, " for rot in actorCue.rot)
            + "".join(f"{pos}, " for pos in actorCue.startPos)
            + "".join(f"{pos}, " for pos in actorCue.endPos)
            + "0.0f, 0.0f, 0.0f),\n"
        )

    def getCamListCmd(self, cmdName: str, startFrame: int, endFrame: int):
        return indent + f"{cmdName}({startFrame}, {endFrame}),\n"

    def getCamEyeSplineCmd(self, camEyeSpline: MMCSMotionCamEyeSpline):
        return self.getCamListCmd("CS_CAM_EYE_SPLINE", camEyeSpline.startFrame, camEyeSpline.endFrame)

    def getCamATSplineCmd(self, camATSpline: MMCSMotionCamATSpline):
        return self.getCamListCmd("CS_CAM_AT_SPLINE", camATSpline.startFrame, camATSpline.endFrame)

    def getCamEyeSplineRelToPlayerCmd(self, camEyeSplinePlayer: MMCSMotionCamEyeSplineRelToPlayer):
        return self.getCamListCmd(
            "CS_CAM_EYE_SPLINE_REL_TO_PLAYER", camEyeSplinePlayer.startFrame, camEyeSplinePlayer.endFrame
        )

    def getCamATSplineRelToPlayerCmd(self, camATSplinePlayer: MMCSMotionCamATSplineRelToPlayer):
        return self.getCamListCmd(
            "CS_CAM_AT_SPLINE_REL_TO_PLAYER", camATSplinePlayer.startFrame, camATSplinePlayer.endFrame
        )

    def getCamEyeCmd(self, camEye: MMCSMotionCamEye):
        return self.getCamListCmd("CS_CAM_EYE", camEye.startFrame, camEye.endFrame)

    def getCamATCmd(self, camAT: MMCSMotionCamAT):
        return self.getCamListCmd("CS_CAM_AT", camAT.startFrame, camAT.endFrame)

    def getCamPointCmd(self, camPoint: MMCSMotionCamPoint):
        return indent * 2 + (
            f"CS_CAM_POINT("
            + f"{camPoint.continueFlag}, {camPoint.camRoll}, {camPoint.frame}, {camPoint.viewAngle}f, "
            + "".join(f"{pos}, " for pos in camPoint.pos)
            + "0),\n"
        )


@dataclass
class MMCSMotionExport(MMCSMotionExportCommands):
    """This class contains functions to create the new cutscene data"""

    csMotionObjects: dict[str, list[Object]]
    useDecomp: bool
    addBeginEndCmds: bool
    entryTotal: int = 0
    frameCount: int = 0
    camEndFrame: int = 0

    def getMmRotation(self, obj: Object):
        """Returns the converted Blender rotation"""

        def conv(r):
            r /= 2.0 * math.pi
            r -= math.floor(r)
            r = round(r * 0x10000)

            if r >= 0x8000:
                r += 0xFFFF0000

            assert r >= 0 and r <= 0xFFFFFFFF and (r <= 0x7FFF or r >= 0xFFFF8000)

            return hex(r & 0xFFFF)

        rotXYZ = [conv(obj.rotation_euler[0]), conv(obj.rotation_euler[2]), conv(obj.rotation_euler[1])]
        return [f"DEG_TO_BINANG({(int(rot, base=16) * (180 / 0x8000)):.3f})" for rot in rotXYZ]

    def getMmPosition(self, pos):
        """Returns the converted Blender position"""

        scale = bpy.context.scene.mmBlenderScale

        x = round(pos[0] * scale)
        y = round(pos[2] * scale)
        z = round(-pos[1] * scale)

        if any(v < -0x8000 or v >= 0x8000 for v in (x, y, z)):
            raise RuntimeError(f"Position(s) too large, out of range: {x}, {y}, {z}")

        return [x, y, z]

    def getActorCueListData(self, isPlayer: bool):
        """Returns the Actor Cue List commands from the corresponding objects"""

        playerOrActor = f"{'Player' if isPlayer else 'Actor'}"
        actorCueListObjects = self.csMotionObjects[f"CS {playerOrActor} Cue List"]
        actorCueListObjects.sort(key=lambda o: o.mmCSMotionProperty.actorCueProp.cueStartFrame)
        actorCueData = ""

        self.entryTotal += len(actorCueListObjects)
        for obj in actorCueListObjects:
            entryTotal = len(obj.children)

            if entryTotal == 0:
                raise PluginError("ERROR: The Actor Cue List does not contain any child Actor Cue objects")

            if obj.children[-1].mmEmptyType != "CS Dummy Cue":
                # we need an extra point that won't be exported to get the real last cue's
                # end frame and end position
                raise PluginError("ERROR: The Actor Cue List is missing the extra dummy point!")

            commandType = obj.mmCSMotionProperty.actorCueListProp.commandType

            if commandType == "Custom":
                commandType = obj.mmCSMotionProperty.actorCueListProp.commandTypeCustom
            elif self.useDecomp:
                commandType = mmData.enumData.enumByKey["csCmd"].itemByKey[commandType].id

            actorCueList = MMCSMotionActorCueList(commandType, entryTotal - 1)  # ignoring dummy cue
            actorCueData += self.getActorCueListCmd(actorCueList, isPlayer)

            for i, childObj in enumerate(obj.children, 1):
                startFrame = childObj.mmCSMotionProperty.actorCueProp.cueStartFrame
                if i < len(obj.children) and childObj.mmEmptyType != "CS Dummy Cue":
                    endFrame = obj.children[i].mmCSMotionProperty.actorCueProp.cueStartFrame
                    actionID = None

                    if isPlayer:
                        cueID = childObj.mmCSMotionProperty.actorCueProp.playerCueID
                        if cueID != "Custom":
                            actionID = mmData.enumData.enumByKey["csPlayerCueId"].itemByKey[cueID].id

                    if actionID is None:
                        actionID = childObj.mmCSMotionProperty.actorCueProp.cueActionID

                    actorCue = MMCSMotionActorCue(
                        startFrame,
                        endFrame,
                        actionID,
                        self.getMmRotation(childObj),
                        self.getMmPosition(childObj.location),
                        self.getMmPosition(obj.children[i].location),
                    )
                    actorCueData += self.getActorCueCmd(actorCue, isPlayer)

        return actorCueData

    def getCameraShotPointData(self, bones, useAT: bool):
        """Returns the Camera Point data from the bone data"""

        shotPoints: list[MMCSMotionCamPoint] = []

        if len(bones) < 4:
            raise RuntimeError("Camera Armature needs at least 4 bones!")

        for bone in bones:
            if bone.parent is not None:
                raise RuntimeError("Camera Armature bones are not allowed to have parent bones!")

            shotPoints.append(
                MMCSMotionCamPoint(
                    ("CS_CAM_CONTINUE" if self.useDecomp else "0"),
                    bone.mmCamShotPointProp.shotPointRoll if useAT else 0,
                    bone.mmCamShotPointProp.shotPointFrame,
                    bone.mmCamShotPointProp.shotPointViewAngle,
                    self.getMmPosition(bone.head if not useAT else bone.tail),
                )
            )

        # NOTE: because of the game's bug explained in the importer we need to add an extra dummy point when exporting
        shotPoints.append(MMCSMotionCamPoint("CS_CAM_STOP" if self.useDecomp else "-1", 0, 0, 0.0, [0, 0, 0]))
        return shotPoints

    def getCamCmdFunc(self, camMode: str, useAT: bool):
        """Returns the camera get function depending on the camera mode"""

        camCmdFuncMap = {
            "splineEyeOrAT": self.getCamATSplineCmd if useAT else self.getCamEyeSplineCmd,
            "splineEyeOrATRelPlayer": self.getCamATSplineRelToPlayerCmd
            if useAT
            else self.getCamEyeSplineRelToPlayerCmd,
            "eyeOrAT": self.getCamATCmd if useAT else self.getCamEyeCmd,
        }

        return camCmdFuncMap[camMode]

    def getCamClass(self, camMode: str, useAT: bool):
        """Returns the camera dataclass depending on the camera mode"""

        camCmdClassMap = {
            "splineEyeOrAT": MMCSMotionCamATSpline if useAT else MMCSMotionCamEyeSpline,
            "splineEyeOrATRelPlayer": MMCSMotionCamATSplineRelToPlayer
            if useAT
            else MMCSMotionCamEyeSplineRelToPlayer,
            "eyeOrAT": MMCSMotionCamAT if useAT else MMCSMotionCamEye,
        }

        return camCmdClassMap[camMode]

    def getCamListData(self, shotObj: Object, useAT: bool):
        """Returns the Camera Shot data from the corresponding Armatures"""

        camPointList = self.getCameraShotPointData(shotObj.data.bones, useAT)
        startFrame = shotObj.data.mmCamShotProp.shotStartFrame

        # "fake" end frame
        endFrame = (
            startFrame + max(2, sum(point.frame for point in camPointList)) + (camPointList[-2].frame if useAT else 1)
        )

        if not useAT:
            for pointData in camPointList:
                pointData.frame = 0
            self.camEndFrame = endFrame

        camData = self.getCamClass(shotObj.data.mmCamShotProp.shotCamMode, useAT)(startFrame, endFrame)
        return self.getCamCmdFunc(shotObj.data.mmCamShotProp.shotCamMode, useAT)(camData) + "".join(
            self.getCamPointCmd(pointData) for pointData in camPointList
        )

    def getCameraShotData(self):
        """Returns every Camera Shot commands"""

        shotObjects = self.csMotionObjects["camShot"]
        cameraShotData = ""

        if len(shotObjects) > 0:
            frameCount = -1
            for shotObj in shotObjects:
                cameraShotData += self.getCamListData(shotObj, False) + self.getCamListData(shotObj, True)
                frameCount = max(frameCount, self.camEndFrame + 1)
            self.frameCount += frameCount
            self.entryTotal += len(shotObjects) * 2

        return cameraShotData

    def getExportData(self):
        """Returns the cutscene data"""

        data = self.getActorCueListData(False) + self.getActorCueListData(True) + self.getCameraShotData()
        if self.addBeginEndCmds:
            data = (
                indent + f"CS_BEGIN_CUTSCENE({self.entryTotal}, {self.frameCount}),\n" + data + indent + "CS_END(),\n"
            )
        return data
