from os import path
from dataclasses import dataclass
from .mm_getters import getXMLRoot
from .mm_data import Mm_BaseElement


@dataclass
class Mm_ActorElement(Mm_BaseElement):
    category: str
    tiedObjects: list[str]


class Mm_ActorData:
    """Everything related to Mm Actors"""

    def __init__(self):
        # Path to the ``ActorList.xml`` file
        actorXML = path.dirname(path.abspath(__file__)) + "\\xml\\ActorList.xml"

        actorXML = "G:\\Misc Repos\\fast64\\fast64_internal\\mm\\data\\xml\\ActorList.xml"

        print("starting getXMLRoot" + actorXML)
        actorRoot = getXMLRoot(actorXML)

        # general actor list
        self.actorList: list[Mm_ActorElement] = []

        print("starting xml iteration")
        for actor in actorRoot.iterfind("Actor"):
            tiedObjects = []
            objKey = actor.get("ObjectKey")
            actorName = f"{actor.attrib['Name']} - {actor.attrib['ID'].removeprefix('ACTOR_')}"
            if objKey is not None:  # actors don't always use an object
                tiedObjects = objKey.split(",")
            self.actorList.append(
                Mm_ActorElement(
                    actor.attrib["ID"],
                    actor.attrib["Key"],
                    actorName,
                    int(actor.attrib["Index"]),
                    actor.attrib["Category"],
                    tiedObjects,
                )
            )
        self.actorsByKey = {actor.key: actor for actor in self.actorList}
        self.actorsByID = {actor.id: actor for actor in self.actorList}

        # list of tuples used by Blender's enum properties
        lastIndex = max(1, *(actor.index for actor in self.actorList))
        self.mmEnumActorID = [("None", f"{i} (Deleted from the XML)", "None") for i in range(lastIndex)]
        self.mmEnumActorID.insert(0, ("Custom", "Custom Actor", "Custom"))
        for actor in self.actorList:
            self.mmEnumActorID[actor.index] = (actor.id, actor.name, actor.id)
