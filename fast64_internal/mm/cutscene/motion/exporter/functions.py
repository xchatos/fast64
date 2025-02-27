import bpy

from bpy.types import Object
from .....utility import PluginError
from .classes import MMCSMotionExport


def getCSMotionObjects(csName: str):
    """Returns the object list containing every object from the cutscene to export"""

    csMotionObjects: dict[str, list[Object]] = {
        "Cutscene": [],
        "CS Actor Cue List": [],
        "CS Player Cue List": [],
        "camShot": [],
    }

    if csName is None:
        raise PluginError("ERROR: The cutscene name is None!")

    for obj in bpy.data.objects:
        isEmptyObj = obj.type == "EMPTY"

        # look for the cutscene object based on the cutscene name
        parentCheck = obj.parent is not None and obj.parent.name == f"Cutscene.{csName}"
        csObjCheck = isEmptyObj and obj.mmEmptyType == "Cutscene" and obj.name == f"Cutscene.{csName}"
        if parentCheck or csObjCheck:
            # add the relevant objects based on the empty type or if it's an armature
            if isEmptyObj and obj.mmEmptyType in csMotionObjects.keys():
                csMotionObjects[obj.mmEmptyType].append(obj)

            if obj.type == "ARMATURE" and obj.parent.mmEmptyType == "Cutscene":
                csMotionObjects["camShot"].append(obj)

    return csMotionObjects


def getCutsceneMotionData(csName: str, addBeginEndCmds: bool):
    """Returns the initialised cutscene exporter"""

    # this allows us to change the exporter's variables to get what we need
    return MMCSMotionExport(
        getCSMotionObjects(csName),
        bpy.context.scene.fast64.mm.hackerFeaturesEnabled or bpy.context.scene.useDecompFeatures,
        addBeginEndCmds,
    )
