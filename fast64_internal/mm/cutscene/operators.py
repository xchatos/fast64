import os
import re

from bpy.path import abspath
from bpy.ops import object
from bpy.props import StringProperty, EnumProperty, IntProperty
from bpy.types import Scene, Operator, Context, UILayout
from bpy.utils import register_class, unregister_class
from ...utility import CData, PluginError, writeCData, raisePluginError
from ..mm_utility import getCollection
from ..scene.exporter.to_c import mmCutsceneDataToC
from .exporter import convertCutsceneObject
from .constants import mmEnumCSTextboxType, mmEnumCSListType, mmEnumCSListTypeIcons
from .motion.importer import importCutsceneData
from .motion.exporter import getCutsceneMotionData


def checkGetFilePaths(context: Context):
    cpath = abspath(context.scene.mmCutsceneExportPath)

    if not cpath.endswith(".c"):
        raise PluginError("Output file must end with .c")

    hpath = cpath[:-1] + "h"
    headerfilename = os.path.basename(hpath)

    return cpath, hpath, headerfilename


def mmCutsceneIncludes(headerfilename):
    ret = CData()
    ret.source = (
        '#include "ultra64.h"\n'
        + '#include "z64.h"\n'
        + '#include "macros.h"\n'
        + '#include "command_macros_base.h"\n'
        + '#include "z64cutscene_commands.h"\n\n'
        + '#include "'
        + headerfilename
        + '"\n\n'
    )
    return ret


def drawCSListAddOp(layout: UILayout, objName: str, collectionType):
    def addButton(row):
        nonlocal l
        op = row.operator(MMCSListAdd.bl_idname, text=mmEnumCSListType[l][1], icon=mmEnumCSListTypeIcons[l])
        op.collectionType = collectionType
        op.listType = mmEnumCSListType[l][0]
        op.objName = objName
        l += 1

    box = layout.column(align=True)
    l = 0
    row = box.row(align=True)
    row.label(text="Add:")
    addButton(row)
    for _ in range(3):
        row = box.row(align=True)
        for _ in range(3):
            addButton(row)


def insertCutsceneData(filePath: str, csName: str):
    """Inserts the motion data in the cutscene and returns the new data"""
    fileLines = []
    includes = mmCutsceneIncludes("").source.split("\n")

    # if the file is not found then it's likely a new file that needs to be created
    try:
        with open(filePath, "r") as inputFile:
            fileLines = inputFile.readlines()
        fileLines = fileLines[len(includes) - 1 :]
    except FileNotFoundError:
        fileLines = []

    foundCutscene = False
    motionExporter = getCutsceneMotionData(csName, False)
    beginIndex = 0

    for i, line in enumerate(fileLines):
        # skip commented lines
        if not line.startswith("//") and not line.startswith("/*"):
            if f"CutsceneData {csName}" in line:
                foundCutscene = True

            if foundCutscene:
                if "CS_BEGIN_CUTSCENE" in line:
                    # save the index of the line that contains the entry total and the framecount for later use
                    beginIndex = i

                # looking at next line to see if we reached the end of the cs script
                index = i + 1
                if index < len(fileLines) and "CS_END" in fileLines[index]:
                    # exporting first to get the new framecount and the total of entries values
                    fileLines.insert(index, motionExporter.getExportData())

                    # update framecount and entry total values
                    beginLine = fileLines[beginIndex]
                    reMatch = re.search(r"\b\(([0-9a-fA-F, ]*)\b", beginLine)
                    if reMatch is not None:
                        params = reMatch[1].split(", ")
                        entryTotal = int(params[0], base=0)
                        frameCount = int(params[1], base=0)
                        entries = re.sub(
                            r"\b\(([0-9a-fA-F]*)\b", f"({entryTotal + motionExporter.entryTotal}", beginLine
                        )
                        frames = re.sub(r"\b([0-9a-fA-F]*)\)", f"{frameCount + motionExporter.frameCount})", beginLine)
                        fileLines[beginIndex] = f"{entries.split(', ')[0]}, {frames.split(', ')[1]}"
                    else:
                        raise PluginError("ERROR: Can't find `CS_BEGIN_CUTSCENE()` parameters!")
                    break

    fileData = CData()

    if not foundCutscene:
        print(f"WARNING: Can't find Cutscene ``{csName}``, inserting data at the end of the file.")
        motionExporter.addBeginEndCmds = True
        csArrayName = f"CutsceneData {csName}[]"
        fileLines.append("\n" + csArrayName + " = {\n" + motionExporter.getExportData() + "};\n")
        fileData.header = f"{csArrayName};\n"

    fileData.source = "".join(line for line in fileLines)
    return fileData


class MMCSTextboxAdd(Operator):
    bl_idname = "object.mm_cstextbox_add"
    bl_label = "Add CS Textbox"
    bl_options = {"REGISTER", "UNDO"}

    collectionType: StringProperty()
    textboxType: EnumProperty(items=mmEnumCSTextboxType)
    listIndex: IntProperty()
    objName: StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, self.listIndex)
        newTextboxElement = collection.add()
        newTextboxElement.textboxType = self.textboxType
        return {"FINISHED"}


class MMCSListAdd(Operator):
    bl_idname = "object.mm_cslist_add"
    bl_label = "Add CS List"
    bl_options = {"REGISTER", "UNDO"}

    collectionType: StringProperty()
    listType: EnumProperty(items=mmEnumCSListType)
    objName: StringProperty()

    def execute(self, context):
        collection = getCollection(self.objName, self.collectionType, None)
        newList = collection.add()
        newList.listType = self.listType
        return {"FINISHED"}


class MM_ImportCutscene(Operator):
    bl_idname = "object.mm_import_cutscenes"
    bl_label = "Import All Cutscenes"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        try:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")

            path = abspath(context.scene.mmCutsceneImportPath)
            context.scene.mmCSNumber = importCutsceneData(path, None)

            self.report({"INFO"}, "Successfully imported cutscenes")
            return {"FINISHED"}
        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}


class MM_ExportCutscene(Operator):
    bl_idname = "object.mm_export_cutscene"
    bl_label = "Export Cutscene"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        try:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")

            activeObj = context.view_layer.objects.active

            if activeObj is None or activeObj.data is not None or activeObj.mmEmptyType != "Cutscene":
                raise PluginError("You must select a cutscene object")

            if activeObj.parent is not None:
                raise PluginError("Cutscene object must not be parented to anything")

            cpath, hpath, headerfilename = checkGetFilePaths(context)
            csdata = mmCutsceneIncludes(headerfilename)
            converted = convertCutsceneObject(activeObj)

            if context.scene.exportMotionOnly:
                csdata.append(insertCutsceneData(cpath, activeObj.name.removeprefix("Cutscene.")))
            else:
                csdata.append(mmCutsceneDataToC(converted, converted.name))
            writeCData(csdata, hpath, cpath)

            self.report({"INFO"}, "Successfully exported cutscene")
            return {"FINISHED"}
        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}


class MM_ExportAllCutscenes(Operator):
    bl_idname = "object.mm_export_all_cutscenes"
    bl_label = "Export All Cutscenes"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        try:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")

            cpath, hpath, headerfilename = checkGetFilePaths(context)
            csdata = mmCutsceneIncludes(headerfilename)
            count = 0

            for obj in context.view_layer.objects:
                if obj.type == "EMPTY" and obj.mmEmptyType == "Cutscene":
                    if obj.parent is not None:
                        print(f"Parent: {obj.parent.name}, Object: {obj.name}")
                        raise PluginError("Cutscene object must not be parented to anything")

                    converted = convertCutsceneObject(obj)
                    if context.scene.exportMotionOnly:
                        raise PluginError("ERROR: Not implemented yet.")
                    else:
                        csdata.append(mmCutsceneDataToC(converted, converted.name))
                    count += 1

            if count == 0:
                raise PluginError("Could not find any cutscenes to export")

            writeCData(csdata, hpath, cpath)
            self.report({"INFO"}, "Successfully exported " + str(count) + " cutscenes")
            return {"FINISHED"}
        except Exception as e:
            raisePluginError(self, e)
            return {"CANCELLED"}


mm_cutscene_classes = (
    MMCSTextboxAdd,
    MMCSListAdd,
    MM_ImportCutscene,
    MM_ExportCutscene,
    MM_ExportAllCutscenes,
)


def mm_cutscene_ops_register():
    for cls in mm_cutscene_classes:
        register_class(cls)

    Scene.mmCutsceneExportPath = StringProperty(name="File", subtype="FILE_PATH")
    Scene.mmCutsceneImportPath = StringProperty(name="File", subtype="FILE_PATH")
    Scene.mmCSNumber = IntProperty(default=1, min=0)


def mm_cutscene_ops_unregister():
    for cls in reversed(mm_cutscene_classes):
        unregister_class(cls)

    del Scene.mmCSNumber
    del Scene.mmCutsceneImportPath
    del Scene.mmCutsceneExportPath
