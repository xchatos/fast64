from dataclasses import dataclass, field
from os import path
from .mm_getters import getXMLRoot
from .mm_data import Mm_BaseElement

# Note: "enumData" in this context refers to an Mm Object file (like ``gameplay_keep``)


@dataclass
class Mm_ItemElement(Mm_BaseElement):
    pass


@dataclass
class Mm_EnumElement(Mm_BaseElement):
    items: list[Mm_ItemElement]
    itemByKey: dict[str, Mm_ItemElement] = field(default_factory=dict)
    itemByIndex: dict[int, Mm_ItemElement] = field(default_factory=dict)
    itemById: dict[int, Mm_ItemElement] = field(default_factory=dict)

    def __post_init__(self):
        self.itemByKey = {item.key: item for item in self.items}
        self.itemByIndex = {item.index: item for item in self.items}
        self.itemById = {item.id: item for item in self.items}


class Mm_EnumData:
    """Cutscene and misc enum data"""

    def __init__(self):
        # general enumData list
        self.enumDataList: list[Mm_EnumElement] = []

        # Path to the ``EnumData.xml`` file
        enumDataXML = path.dirname(path.abspath(__file__)) + "/xml/EnumData.xml"
        enumDataRoot = getXMLRoot(enumDataXML)

        for enum in enumDataRoot.iterfind("Enum"):
            self.enumDataList.append(
                Mm_EnumElement(
                    enum.attrib["ID"],
                    enum.attrib["Key"],
                    None,
                    None,
                    [
                        Mm_ItemElement(
                            item.attrib["ID"],
                            item.attrib["Key"],
                            item.attrib["ID"],
                            int(item.attrib["Index"]),
                        )
                        for item in enum
                    ],
                )
            )

        # create list of tuples used by Blender's enum properties
        self.deletedEntry = ("None", "(Deleted from the XML)", "None")

        self.mmEnumCsCmd: list[tuple[str, str, str]] = []
        self.mmEnumCsMiscType: list[tuple[str, str, str]] = []
        self.mmEnumCsTextType: list[tuple[str, str, str]] = []
        self.mmEnumCsFadeOutSeqPlayer: list[tuple[str, str, str]] = []
        self.mmEnumCsTransitionType: list[tuple[str, str, str]] = []
        self.mmEnumCsDestination: list[tuple[str, str, str]] = []
        self.mmEnumCsPlayerCueId: list[tuple[str, str, str]] = []
        self.mmEnumNaviQuestHintType: list[tuple[str, str, str]] = []

        self.enumByID = {enum.id: enum for enum in self.enumDataList}
        self.enumByKey = {enum.key: enum for enum in self.enumDataList}

        for key in self.enumByKey.keys():
            setattr(self, "mmEnum" + key[0].upper() + key[1:], self.getMmEnumData(key))

    def getMmEnumData(self, enumKey: str):
        enum = self.enumByKey[enumKey]
        firstIndex = min(1, *(item.index for item in enum.items))
        lastIndex = max(1, *(item.index for item in enum.items)) + 1
        enumData = [self.deletedEntry] * lastIndex
        custom = ("Custom", "Custom", "Custom")

        for item in enum.items:
            if item.index < lastIndex:
                identifier = item.key
                enumData[item.index] = (identifier, item.name, item.id)

        if firstIndex > 0:
            enumData[0] = custom
        else:
            enumData.insert(0, custom)

        return enumData
