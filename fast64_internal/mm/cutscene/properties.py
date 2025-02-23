import bpy
from bpy.types import PropertyGroup, Object, UILayout, Scene, Context
from bpy.props import StringProperty, EnumProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty
from bpy.utils import register_class, unregister_class
from ...utility import PluginError, prop_split
from ..mm_utility import MMCollectionAdd, drawCollectionOps
from .operators import MMCSTextboxAdd, drawCSListAddOp
from .constants import mmEnumCSTextboxType, mmEnumCSListType, mmEnumCSTransitionType, mmEnumCSTextboxTypeIcons
from .motion.preview import previewFrameHandler

from .motion.operators import (
    MMCSMotionPlayPreview,
    MMCSMotionCreateCameraShot,
    MMCSMotionCreatePlayerCueList,
    MMCSMotionCreateActorCueList,
)


# Perhaps this should have been called something like MMCSParentPropertyType,
# but now it needs to keep the same name to not break existing scenes which use
# the cutscene system.
class MMCSProperty:
    propName = None
    attrName = None
    subprops = ["startFrame", "endFrame"]
    expandTab: BoolProperty(default=True)
    startFrame: IntProperty(name="", default=0, min=0)
    endFrame: IntProperty(name="", default=1, min=0)

    def getName(self):
        return self.propName

    def filterProp(self, name, listProp):
        return True

    def filterName(self, name, listProp):
        return name

    def draw(self, layout, listProp, listIndex, cmdIndex, objName, collectionType):
        layout.prop(
            self,
            "expandTab",
            text=self.getName() + " " + str(cmdIndex),
            icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT",
        )
        if not self.expandTab:
            return
        box = layout.box().column()
        drawCollectionOps(box, cmdIndex, collectionType + "." + self.attrName, listIndex, objName)
        for p in self.subprops:
            if self.filterProp(p, listProp):
                prop_split(box, self, p, self.filterName(p, listProp))


class MMCSTextboxProperty(MMCSProperty, PropertyGroup):
    propName = "Textbox"
    attrName = "textbox"
    subprops = [
        "messageId",
        "ocarinaSongAction",
        "startFrame",
        "endFrame",
        "type",
        "topOptionBranch",
        "bottomOptionBranch",
        "ocarinaMessageId",
    ]
    textboxType: EnumProperty(items=mmEnumCSTextboxType)
    messageId: StringProperty(name="", default="0x0000")
    ocarinaSongAction: StringProperty(name="", default="0x0000")
    type: StringProperty(name="", default="0x0000")
    topOptionBranch: StringProperty(name="", default="0x0000")
    bottomOptionBranch: StringProperty(name="", default="0x0000")
    ocarinaMessageId: StringProperty(name="", default="0x0000")

    def getName(self):
        return self.textboxType

    def filterProp(self, name, listProp):
        if self.textboxType == "Text":
            return name not in ["ocarinaSongAction", "ocarinaMessageId"]
        elif self.textboxType == "None":
            return name in ["startFrame", "endFrame"]
        elif self.textboxType == "LearnSong":
            return name in ["ocarinaSongAction", "startFrame", "endFrame", "ocarinaMessageId"]
        else:
            raise PluginError("Invalid property name for MMCSTextboxProperty")


class MMCSLightingProperty(MMCSProperty, PropertyGroup):
    propName = "Lighting"
    attrName = "lighting"
    subprops = ["index", "startFrame"]
    index: IntProperty(name="", default=1, min=1)


class MMCSTimeProperty(MMCSProperty, PropertyGroup):
    propName = "Time"
    attrName = "time"
    subprops = ["startFrame", "hour", "minute"]
    hour: IntProperty(name="", default=23, min=0, max=23)
    minute: IntProperty(name="", default=59, min=0, max=59)


class MMCSBGMProperty(MMCSProperty, PropertyGroup):
    propName = "BGM"
    attrName = "bgm"
    subprops = ["value", "startFrame", "endFrame"]
    value: StringProperty(name="", default="0x0000")

    def filterProp(self, name, listProp):
        return name != "endFrame" or listProp.listType == "FadeBGM"

    def filterName(self, name, listProp):
        if name == "value":
            return "Fade Type" if listProp.listType == "FadeBGM" else "Sequence"
        return name


class MMCSMiscProperty(MMCSProperty, PropertyGroup):
    propName = "Misc"
    attrName = "misc"
    subprops = ["operation", "startFrame", "endFrame"]
    operation: IntProperty(name="", default=1, min=1, max=35)


class MMCS0x09Property(MMCSProperty, PropertyGroup):
    propName = "0x09"
    attrName = "nine"
    subprops = ["startFrame", "unk2", "unk3", "unk4"]
    unk2: StringProperty(name="", default="0x00")
    unk3: StringProperty(name="", default="0x00")
    unk4: StringProperty(name="", default="0x00")


class MMCSUnkProperty(MMCSProperty, PropertyGroup):
    propName = "Unk"
    attrName = "unk"
    subprops = ["unk1", "unk2", "unk3", "unk4", "unk5", "unk6", "unk7", "unk8", "unk9", "unk10", "unk11", "unk12"]
    unk1: StringProperty(name="", default="0x00000000")
    unk2: StringProperty(name="", default="0x00000000")
    unk3: StringProperty(name="", default="0x00000000")
    unk4: StringProperty(name="", default="0x00000000")
    unk5: StringProperty(name="", default="0x00000000")
    unk6: StringProperty(name="", default="0x00000000")
    unk7: StringProperty(name="", default="0x00000000")
    unk8: StringProperty(name="", default="0x00000000")
    unk9: StringProperty(name="", default="0x00000000")
    unk10: StringProperty(name="", default="0x00000000")
    unk11: StringProperty(name="", default="0x00000000")
    unk12: StringProperty(name="", default="0x00000000")


class MMCSListProperty(PropertyGroup):
    expandTab: BoolProperty(default=True)

    listType: EnumProperty(items=mmEnumCSListType)
    textbox: CollectionProperty(type=MMCSTextboxProperty)
    lighting: CollectionProperty(type=MMCSLightingProperty)
    time: CollectionProperty(type=MMCSTimeProperty)
    bgm: CollectionProperty(type=MMCSBGMProperty)
    misc: CollectionProperty(type=MMCSMiscProperty)
    nine: CollectionProperty(type=MMCS0x09Property)
    unk: CollectionProperty(type=MMCSUnkProperty)

    unkType: StringProperty(name="", default="0x0001")
    fxType: EnumProperty(items=mmEnumCSTransitionType)
    fxStartFrame: IntProperty(name="", default=0, min=0)
    fxEndFrame: IntProperty(name="", default=1, min=0)

    def draw_props(self, layout: UILayout, listIndex: int, objName: str, collectionType: str):
        layout.prop(
            self,
            "expandTab",
            text=self.listType + " List" if self.listType != "FX" else "Scene Trans FX",
            icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT",
        )
        if not self.expandTab:
            return
        box = layout.box().column()
        drawCollectionOps(box, listIndex, collectionType, None, objName, False)

        if self.listType == "Textbox":
            attrName = "textbox"
        elif self.listType == "FX":
            prop_split(box, self, "fxType", "Transition")
            prop_split(box, self, "fxStartFrame", "Start Frame")
            prop_split(box, self, "fxEndFrame", "End Frame")
            return
        elif self.listType == "Lighting":
            attrName = "lighting"
        elif self.listType == "Time":
            attrName = "time"
        elif self.listType in ["PlayBGM", "StopBGM", "FadeBGM"]:
            attrName = "bgm"
        elif self.listType == "Misc":
            attrName = "misc"
        elif self.listType == "0x09":
            attrName = "nine"
        elif self.listType == "Unk":
            prop_split(box, self, "unkType", "Unk List Type")
            attrName = "unk"
        else:
            raise PluginError("Internal error: invalid listType " + self.listType)

        dat = getattr(self, attrName)
        for i, p in enumerate(dat):
            p.draw(box, self, listIndex, i, objName, collectionType)
        if len(dat) == 0:
            box.label(text="No items in " + self.listType + " List.")
        if self.listType == "Textbox":
            row = box.row(align=True)
            for l in range(3):
                addOp = row.operator(
                    MMCSTextboxAdd.bl_idname,
                    text="Add " + mmEnumCSTextboxType[l][1],
                    icon=mmEnumCSTextboxTypeIcons[l],
                )
                addOp.collectionType = collectionType + ".textbox"
                addOp.textboxType = mmEnumCSTextboxType[l][0]
                addOp.listIndex = listIndex
                addOp.objName = objName
        else:
            addOp = box.operator(MMCollectionAdd.bl_idname, text="Add item to " + self.listType + " List")
            addOp.option = len(dat)
            addOp.collectionType = collectionType + "." + attrName
            addOp.subIndex = listIndex
            addOp.objName = objName


class MMCutsceneCommandBase:
    startFrame: IntProperty(min=0)
    endFrame: IntProperty(min=0)


class MMCutsceneTransitionProperty(MMCutsceneCommandBase, PropertyGroup):
    type: StringProperty(default="Unknown")


class MMCutsceneMiscProperty(MMCutsceneCommandBase, PropertyGroup):
    type: StringProperty(default="Unknown")


class MMCutscenePreviewProperty(PropertyGroup):
    useWidescreen: BoolProperty(
        name="Use Widescreen Camera", default=False, update=lambda self, context: self.updateWidescreen(context)
    )

    transitionList: CollectionProperty(type=MMCutsceneTransitionProperty)
    miscList: CollectionProperty(type=MMCutsceneMiscProperty)

    trigger: BoolProperty(default=False)  # for ``CS_TRANS_TRIGGER_INSTANCE``
    isFixedCamSet: BoolProperty(default=False)
    prevFrame: IntProperty(default=-1)
    nextFrame: IntProperty(default=1)

    def updateWidescreen(self, context: Context):
        if self.useWidescreen:
            context.scene.render.resolution_x = 426
        else:
            context.scene.render.resolution_x = 320
        context.scene.render.resolution_y = 240

        # force a refresh of the current frame
        previewFrameHandler(context.scene)


class MMCutsceneProperty(PropertyGroup):
    csEndFrame: IntProperty(name="End Frame", min=0, default=100)
    csWriteTerminator: BoolProperty(name="Write Terminator (Code Execution)")
    csTermIdx: IntProperty(name="Index", min=0)
    csTermStart: IntProperty(name="Start Frm", min=0, default=99)
    csTermEnd: IntProperty(name="End Frm", min=0, default=100)
    csLists: CollectionProperty(type=MMCSListProperty, name="Cutscene Lists")

    preview: PointerProperty(type=MMCutscenePreviewProperty)

    def draw_props(self, layout: UILayout, obj: Object):
        split = layout.split(factor=0.5)
        split.label(text="Player Age for Preview")
        split.prop(bpy.context.scene, "mmpreviewPlayerAge", text="")

        split = layout.split(factor=0.5)
        split.operator(MMCSMotionCreateCameraShot.bl_idname, icon="VIEW_CAMERA")
        split.operator(MMCSMotionPlayPreview.bl_idname, icon="RESTRICT_VIEW_OFF")

        split = layout.split(factor=0.5)
        split.operator(MMCSMotionCreatePlayerCueList.bl_idname)
        split.operator(MMCSMotionCreateActorCueList.bl_idname)

        layout.prop(self.preview, "useWidescreen")

        layout.prop(self, "csEndFrame")
        layout.prop(self, "csWriteTerminator")
        if self.csWriteTerminator:
            r = layout.row()
            r.prop(self, "csTermIdx")
            r.prop(self, "csTermStart")
            r.prop(self, "csTermEnd")
        for i, p in enumerate(self.csLists):
            p.draw_props(layout, i, obj.name, "Cutscene")

        drawCSListAddOp(layout, obj.name, "Cutscene")


classes = (
    MMCSTextboxProperty,
    MMCSLightingProperty,
    MMCSTimeProperty,
    MMCSBGMProperty,
    MMCSMiscProperty,
    MMCS0x09Property,
    MMCSUnkProperty,
    MMCSListProperty,
    MMCutsceneTransitionProperty,
    MMCutsceneMiscProperty,
    MMCutscenePreviewProperty,
    MMCutsceneProperty,
)


def mm_cutscene_props_register():
    for cls in classes:
        register_class(cls)

    Object.mmCutsceneProperty = PointerProperty(type=MMCutsceneProperty)
    Scene.mmCSPreviewNodesReady = BoolProperty(default=False)
    Scene.mmCSPreviewCSObj = PointerProperty(type=Object)


def mm_cutscene_props_unregister():
    del Scene.mmCSPreviewCSObj
    del Scene.mmCSPreviewNodesReady
    del Object.mmCutsceneProperty

    for cls in reversed(classes):
        unregister_class(cls)
