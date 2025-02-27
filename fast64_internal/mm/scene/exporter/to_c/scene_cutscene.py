from .....utility import CData, PluginError, indent
from ....mm_level_classes import MMScene
from ....cutscene.constants import mmEnumCSTextboxTypeEntryC, mmEnumCSListTypeListC, mmEnumCSListTypeEntryC
from ....cutscene.motion.exporter import getCutsceneMotionData


def mmCutsceneDataToC(csParent, csName):
    # csParent can be MMCutscene or MMScene
    motionExporter = getCutsceneMotionData(csName, False)
    motionData = motionExporter.getExportData()
    data = CData()
    data.header = "extern CutsceneData " + csName + "[];\n"
    data.source = "CutsceneData " + csName + "[] = {\n"
    nentries = len(csParent.csLists) + (1 if csParent.csWriteTerminator else 0)
    frameDiff = 0
    if motionExporter.frameCount > csParent.csEndFrame:
        frameDiff = motionExporter.frameCount - csParent.csEndFrame
    data.source += (
        indent + f"CS_BEGIN_CUTSCENE({nentries + motionExporter.entryTotal}, "
    ) + f"{csParent.csEndFrame + frameDiff}),\n"
    if csParent.csWriteTerminator:
        data.source += (
            "\tCS_TERMINATOR("
            + str(csParent.csTermIdx)
            + ", "
            + str(csParent.csTermStart)
            + ", "
            + str(csParent.csTermEnd)
            + "),\n"
        )
    for list in csParent.csLists:
        data.source += "\t" + mmEnumCSListTypeListC[list.listType] + "("
        if list.listType == "Unk":
            data.source += list.unkType + ", "
        if list.listType == "FX":
            data.source += list.fxType + ", " + str(list.fxStartFrame) + ", " + str(list.fxEndFrame)
        else:
            data.source += str(len(list.entries))
        data.source += "),\n"
        for e in list.entries:
            data.source += "\t\t"
            if list.listType == "Textbox":
                data.source += mmEnumCSTextboxTypeEntryC[e.textboxType]
            else:
                data.source += mmEnumCSListTypeEntryC[list.listType]
            data.source += "("
            if list.listType == "Textbox":
                if e.textboxType == "Text":
                    data.source += (
                        e.messageId
                        + ", "
                        + str(e.startFrame)
                        + ", "
                        + str(e.endFrame)
                        + ", "
                        + e.type
                        + ", "
                        + e.topOptionBranch
                        + ", "
                        + e.bottomOptionBranch
                    )
                elif e.textboxType == "None":
                    data.source += str(e.startFrame) + ", " + str(e.endFrame)
                elif e.textboxType == "LearnSong":
                    data.source += (
                        e.ocarinaSongAction
                        + ", "
                        + str(e.startFrame)
                        + ", "
                        + str(e.endFrame)
                        + ", "
                        + e.ocarinaMessageId
                    )
            elif list.listType == "Lighting":
                data.source += (
                    str(e.index) + ", " + str(e.startFrame) + ", " + str(e.startFrame + 1) + ", 0, 0, 0, 0, 0, 0, 0, 0"
                )
            elif list.listType == "Time":
                data.source += (
                    "1, "
                    + str(e.startFrame)
                    + ", "
                    + str(e.startFrame + 1)
                    + ", "
                    + str(e.hour)
                    + ", "
                    + str(e.minute)
                    + ", 0"
                )
            elif list.listType in ["PlayBGM", "StopBGM", "FadeBGM"]:
                data.source += e.value
                if list.listType != "FadeBGM":
                    data.source += " + 1"  # Game subtracts 1 to get actual seq
                data.source += ", " + str(e.startFrame) + ", " + str(e.endFrame) + ", 0, 0, 0, 0, 0, 0, 0, 0"
            elif list.listType == "Misc":
                data.source += (
                    str(e.operation)
                    + ", "
                    + str(e.startFrame)
                    + ", "
                    + str(e.endFrame)
                    + ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"
                )
            elif list.listType == "0x09":
                data.source += (
                    "0, "
                    + str(e.startFrame)
                    + ", "
                    + str(e.startFrame + 1)
                    + ", "
                    + e.unk2
                    + ", "
                    + e.unk3
                    + ", "
                    + e.unk4
                    + ", 0, 0"
                )
            elif list.listType == "Unk":
                data.source += (
                    e.unk1
                    + ", "
                    + e.unk2
                    + ", "
                    + e.unk3
                    + ", "
                    + e.unk4
                    + ", "
                    + e.unk5
                    + ", "
                    + e.unk6
                    + ", "
                    + e.unk7
                    + ", "
                    + e.unk8
                    + ", "
                    + e.unk9
                    + ", "
                    + e.unk10
                    + ", "
                    + e.unk11
                    + ", "
                    + e.unk12
                )
            else:
                raise PluginError("Internal error: invalid cutscene list type " + list.listType)
            data.source += "),\n"
    data.source += motionData
    data.source += "\tCS_END(),\n"
    data.source += "};\n\n"
    return data


def getSceneCutscenes(outScene: MMScene):
    cutscenes: list[CData] = []
    altHeaders: list[MMScene] = [
        outScene,
        outScene.childNightHeader,
        outScene.adultDayHeader,
        outScene.adultNightHeader,
    ]
    altHeaders.extend(outScene.cutsceneHeaders)
    csObjects = []

    for i, curHeader in enumerate(altHeaders):
        # curHeader is either None or an MMScene. This can either be the main scene itself,
        # or one of the alternate / cutscene headers.
        if curHeader is not None and curHeader.writeCutscene:
            if curHeader.csWriteType == "Embedded":
                cutscenes.append(mmCutsceneDataToC(curHeader, curHeader.cutsceneDataName(i)))
            elif curHeader.csWriteType == "Object" and curHeader.csWriteObject.name not in csObjects:
                cutscenes.append(mmCutsceneDataToC(curHeader.csWriteObject, curHeader.csWriteObject.name))
                csObjects.append(curHeader.csWriteObject.name)

    for extraCs in outScene.extraCutscenes:
        if not extraCs.name in csObjects:
            cutscenes.append(mmCutsceneDataToC(extraCs, extraCs.name))
            csObjects.append(extraCs.name)

    return cutscenes
