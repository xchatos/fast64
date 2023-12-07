from dataclasses import dataclass
from os import path
from ...utility import PluginError
from .mm_getters import getXMLRoot
from .mm_data import Mm_BaseElement

# Note: "object" in this context refers to an Mm Object file (like ``gameplay_keep``)


@dataclass
class Mm_ObjectElement(Mm_BaseElement):
    pass


class Mm_ObjectData:
    """Everything related to Mm objects"""

    def __init__(self):
        # general object list
        self.objectList: list[Mm_ObjectElement] = []

        # Path to the ``ObjectList.xml`` file
        objectXML = path.dirname(path.abspath(__file__)) + "/xml/ObjectList.xml"
        objectRoot = getXMLRoot(objectXML)

        for obj in objectRoot.iterfind("Object"):
            objName = f"{obj.attrib['Name']} - {obj.attrib['ID'].removeprefix('OBJECT_')}"
            self.objectList.append(
                Mm_ObjectElement(obj.attrib["ID"], obj.attrib["Key"], objName, int(obj.attrib["Index"]))
            )

        self.objectsByID = {obj.id: obj for obj in self.objectList}
        self.objectsByKey = {obj.key: obj for obj in self.objectList}

        # list of tuples used by Blender's enum properties
        self.deletedEntry = ("None", "(Deleted from the XML)", "None")
        lastIndex = max(1, *(obj.index for obj in self.objectList))
        self.mmEnumObjectKey = self.getObjectIDList(lastIndex + 1, False)

        # create the legacy object list for old blends
        self.mmEnumObjectIDLegacy = self.getObjectIDList(self.objectsByKey["obj_timeblock"].index + 1, True)

        # validate the legacy list, if there's any None element then something's wrong
        if self.deletedEntry in self.mmEnumObjectIDLegacy:
            raise PluginError("ERROR: Legacy Object List doesn't match!")

    def getObjectIDList(self, max: int, isLegacy: bool):
        """Generates and returns the object list in the right order"""
        objList = [self.deletedEntry] * max
        for obj in self.objectList:
            if obj.index < max:
                identifier = obj.id if isLegacy else obj.key
                objList[obj.index] = (identifier, obj.name, obj.id)
        objList[0] = ("Custom", "Custom Object", "Custom")
        return objList
