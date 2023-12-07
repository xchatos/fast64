from ...mm_utility import getCutsceneName, getCustomProperty

from .classes import (
    MMCSList,
    MMCSTextbox,
    MMCSLighting,
    MMCSTime,
    MMCSBGM,
    MMCSMisc,
    MMCS0x09,
    MMCSUnk,
    MMCutscene,
)


def readCutsceneData(csParentOut, csParentIn):
    for listIn in csParentIn.csLists:
        listOut = MMCSList()
        listOut.listType = listIn.listType
        listOut.unkType, listOut.fxType, listOut.fxStartFrame, listOut.fxEndFrame = (
            listIn.unkType,
            listIn.fxType,
            listIn.fxStartFrame,
            listIn.fxEndFrame,
        )
        listData = []
        if listOut.listType == "Textbox":
            for entryIn in listIn.textbox:
                entryOut = MMCSTextbox()
                entryOut.textboxType = entryIn.textboxType
                entryOut.messageId = entryIn.messageId
                entryOut.ocarinaSongAction = entryIn.ocarinaSongAction
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                entryOut.type = entryIn.type
                entryOut.topOptionBranch = entryIn.topOptionBranch
                entryOut.bottomOptionBranch = entryIn.bottomOptionBranch
                entryOut.ocarinaMessageId = entryIn.ocarinaMessageId
                listOut.entries.append(entryOut)
        elif listOut.listType == "Lighting":
            for entryIn in listIn.lighting:
                entryOut = MMCSLighting()
                entryOut.index = entryIn.index
                entryOut.startFrame = entryIn.startFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "Time":
            for entryIn in listIn.time:
                entryOut = MMCSTime()
                entryOut.startFrame = entryIn.startFrame
                entryOut.hour = entryIn.hour
                entryOut.minute = entryIn.minute
                listOut.entries.append(entryOut)
        elif listOut.listType in {"PlayBGM", "StopBGM", "FadeBGM"}:
            for entryIn in listIn.bgm:
                entryOut = MMCSBGM()
                entryOut.value = entryIn.value
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "Misc":
            for entryIn in listIn.misc:
                entryOut = MMCSMisc()
                entryOut.operation = entryIn.operation
                entryOut.startFrame = entryIn.startFrame
                entryOut.endFrame = entryIn.endFrame
                listOut.entries.append(entryOut)
        elif listOut.listType == "0x09":
            for entryIn in listIn.nine:
                entryOut = MMCS0x09()
                entryOut.startFrame = entryIn.startFrame
                entryOut.unk2 = entryIn.unk2
                entryOut.unk3 = entryIn.unk3
                entryOut.unk4 = entryIn.unk4
                listOut.entries.append(entryOut)
        elif listOut.listType == "Unk":
            for entryIn in listIn.unk:
                entryOut = MMCSUnk()
                entryOut.unk1 = entryIn.unk1
                entryOut.unk2 = entryIn.unk2
                entryOut.unk3 = entryIn.unk3
                entryOut.unk4 = entryIn.unk4
                entryOut.unk5 = entryIn.unk5
                entryOut.unk6 = entryIn.unk6
                entryOut.unk7 = entryIn.unk7
                entryOut.unk8 = entryIn.unk8
                entryOut.unk9 = entryIn.unk9
                entryOut.unk10 = entryIn.unk10
                entryOut.unk11 = entryIn.unk11
                entryOut.unk12 = entryIn.unk12
                listOut.entries.append(entryOut)
        csParentOut.csLists.append(listOut)


def convertCutsceneObject(obj):
    cs = MMCutscene()
    cs.name = getCutsceneName(obj)
    csprop = obj.mmCutsceneProperty
    cs.csEndFrame = getCustomProperty(csprop, "csEndFrame")
    cs.csWriteTerminator = getCustomProperty(csprop, "csWriteTerminator")
    cs.csTermIdx = getCustomProperty(csprop, "csTermIdx")
    cs.csTermStart = getCustomProperty(csprop, "csTermStart")
    cs.csTermEnd = getCustomProperty(csprop, "csTermEnd")
    readCutsceneData(cs, csprop)
    return cs
