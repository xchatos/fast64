from .....utility import CData, indent
from ....mm_level_classes import MMScene, MMRoom, MMActor, MMTransitionActor, MMEntrance


###################
# Written to Room #
###################

# Actor List


def getActorEntry(actor: MMActor):
    """Returns a single actor entry"""
    posData = "{ " + ", ".join(f"{round(pos)}" for pos in actor.position) + " }"
    rotData = "{ " + "".join(actor.rotation) + " }"

    actorInfos = [actor.actorID, posData, rotData, actor.actorParam]
    infoDescs = ["Actor ID", "Position", "Rotation", "Parameters"]

    return (
        indent
        + (f"// {actor.actorName}\n" + indent if actor.actorName != "" else "")
        + "{\n"
        + ",\n".join((indent * 2) + f"/* {desc:10} */ {info}" for desc, info in zip(infoDescs, actorInfos))
        + ("\n" + indent + "},\n")
    )


def getActorList(outRoom: MMRoom, headerIndex: int):
    """Returns the actor list for the current header"""
    actorList = CData()
    listName = f"ActorEntry {outRoom.actorListName(headerIndex)}"

    # .h
    actorList.header = f"extern {listName}[];\n"

    # .c
    actorList.source = (
        (f"{listName}[{outRoom.getActorLengthDefineName(headerIndex)}]" + " = {\n")
        + "\n".join(getActorEntry(actor) for actor in outRoom.actorList)
        + "};\n\n"
    )

    return actorList


####################
# Written to Scene #
####################

# Transition Actor List


def getTransitionActorEntry(transActor: MMTransitionActor):
    """Returns a single transition actor entry"""
    sides = [(transActor.frontRoom, transActor.frontCam), (transActor.backRoom, transActor.backCam)]
    roomData = "{ " + ", ".join(f"{room}, {cam}" for room, cam in sides) + " }"
    posData = "{ " + ", ".join(f"{round(pos)}" for pos in transActor.position) + " }"
    rotData = f"DEG_TO_BINANG({(transActor.rotationY * (180 / 0x8000)):.3f})"

    actorInfos = [roomData, transActor.actorID, posData, rotData, transActor.actorParam]
    infoDescs = ["Room & Cam Index (Front, Back)", "Actor ID", "Position", "Rotation Y", "Parameters"]

    return (
        (indent + f"// {transActor.actorName}\n" + indent if transActor.actorName != "" else "")
        + "{\n"
        + ",\n".join((indent * 2) + f"/* {desc:30} */ {info}" for desc, info in zip(infoDescs, actorInfos))
        + ("\n" + indent + "},\n")
    )


def getTransitionActorList(outScene: MMScene, headerIndex: int):
    """Returns the transition actor list for the current header"""
    transActorList = CData()
    listName = f"TransitionActorEntry {outScene.transitionActorListName(headerIndex)}"

    # .h
    transActorList.header = f"extern {listName}[];\n"

    # .c
    transActorList.source = (
        (f"{listName}[]" + " = {\n")
        + "\n".join(getTransitionActorEntry(transActor) for transActor in outScene.transitionActorList)
        + "};\n\n"
    )

    return transActorList


# Entrance List


def getSpawnActorList(outScene: MMScene, headerIndex: int):
    """Returns the spawn actor list for the current header"""
    spawnActorList = CData()
    listName = f"ActorEntry {outScene.startPositionsName(headerIndex)}"

    # .h
    spawnActorList.header = f"extern {listName}[];\n"

    # .c
    spawnActorList.source = (
        (f"{listName}[]" + " = {\n")
        + "".join(getActorEntry(spawnActor) for spawnActor in outScene.startPositions.values())
        + "};\n\n"
    )

    return spawnActorList


def getSpawnEntry(entrance: MMEntrance):
    """Returns a single spawn entry"""
    return indent + "{ " + f"{entrance.startPositionIndex}, {entrance.roomIndex}" + " },\n"


def getSpawnList(outScene: MMScene, headerIndex: int):
    """Returns the spawn list for the current header"""
    spawnList = CData()
    listName = f"EntranceEntry {outScene.entranceListName(headerIndex)}"

    # .h
    spawnList.header = f"extern {listName}[];\n"

    # .c
    spawnList.source = (
        (f"{listName}[]" + " = {\n")
        + (indent + "// { Spawn Actor List Index, Room Index }\n")
        + "".join(getSpawnEntry(entrance) for entrance in outScene.entranceList)
        + "};\n\n"
    )

    return spawnList


def getActorCutsceneList(outScene: MMScene, headerIndex: int):
    """Returns the spawn list for the current header"""
    actorCsList = CData()
    listName = f"ActorCutscene {outScene.actorCutsceneListName(headerIndex)}"

    # .h
    actorCsList.header = f"extern {listName}[];\n"

    # .c
    actorCsList.source = (
        (f"{listName}[]" + " = {\n")
        + (indent)
        + "".join("{ -1, -1, -1, 0, -1, 0, 255, 0, 1, 32 },\n")
        + "};\n\n"
    )

    return actorCsList

def getAnimMaterialsList(outScene: MMScene, headerIndex: int):
    """Returns the spawn list for the current header"""
    animMatList = CData()
    listName = f"AnimatedMaterial {outScene.animMaterialsListName(headerIndex)}"

    # .h
    animMatList.header = f"extern {listName}[];\n"

    # .c
    animMatList.source = (
        (f"{listName}[]" + " = {\n")
        + (indent)
        + "".join("{ 0, 6, NULL },\n")
        + "};\n\n"
    )

    return animMatList



def getMinimapList(outScene: MMScene, headerIndex: int):
    """Returns the spawn list for the current header"""
    minimapList = CData()
    listName = f"MinimapList {outScene.minimapListName(headerIndex)}"
    listName2 = f"MinimapEntry {outScene.minimapListName(headerIndex)}"

    # .h
    minimapList.header = (f"extern {listName};\n"
        + f"extern {listName2}_entries[];\n")

    # .c
    minimapList.source = (
        (f"{listName}" + " = {\n")
        + (indent)
        + "".join(f"{outScene.minimapListName(headerIndex)}_entries, 0\n")
        + "};\n\n"
        + (f"{listName2}_entries[]" + " = {\n")
        + (indent)
        + "".join("{ 0xFFFF, 0x0000, 0x0000, 0x0000, 0x0000 },\n")
        + "};\n\n"
    )

    return minimapList
