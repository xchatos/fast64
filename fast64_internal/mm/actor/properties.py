from bpy.types import Object, PropertyGroup, UILayout
from bpy.utils import register_class, unregister_class
from bpy.props import EnumProperty, StringProperty, IntProperty, BoolProperty, CollectionProperty, PointerProperty
from ...utility import prop_split, label_split
from ..mm_constants import mmData, mmEnumSceneSetupPreset, mmEnumCamTransition
from ..scene.properties import MMAlternateSceneHeaderProperty
from ..room.properties import MMAlternateRoomHeaderProperty
from .operators import MM_SearchActorIDEnumOperator

from ..mm_utility import (
    getRoomObj,
    getEnumName,
    drawAddButton,
    drawCollectionOps,
    drawEnumWithCustom,
)


class MMActorHeaderItemProperty(PropertyGroup):
    headerIndex: IntProperty(name="Scene Setup", min=4, default=4)
    expandTab: BoolProperty(name="Expand Tab")

    def draw_props(
        self,
        layout: UILayout,
        propUser: str,
        index: int,
        altProp: MMAlternateSceneHeaderProperty | MMAlternateRoomHeaderProperty,
        objName: str,
    ):
        box = layout.column()
        row = box.row()
        row.prop(self, "headerIndex", text="")
        drawCollectionOps(row.row(align=True), index, propUser, None, objName, compact=True)
        if altProp is not None and self.headerIndex >= len(altProp.cutsceneHeaders) + 4:
            box.label(text="Above header does not exist.", icon="QUESTION")


class MMActorHeaderProperty(PropertyGroup):
    sceneSetupPreset: EnumProperty(name="Scene Setup Preset", items=mmEnumSceneSetupPreset, default="All Scene Setups")
    childDayHeader: BoolProperty(name="Child Day Header", default=True)
    childNightHeader: BoolProperty(name="Child Night Header", default=True)
    adultDayHeader: BoolProperty(name="Adult Day Header", default=True)
    adultNightHeader: BoolProperty(name="Adult Night Header", default=True)
    cutsceneHeaders: CollectionProperty(type=MMActorHeaderItemProperty)

    def checkHeader(self, index: int) -> bool:
        if index == 0:
            return self.childDayHeader
        elif index == 1:
            return self.childNightHeader
        elif index == 2:
            return self.adultDayHeader
        elif index == 3:
            return self.adultNightHeader
        else:
            return index in [value.headerIndex for value in self.cutsceneHeaders]

    def draw_props(
        self,
        layout: UILayout,
        propUser: str,
        altProp: MMAlternateSceneHeaderProperty | MMAlternateRoomHeaderProperty,
        objName: str,
    ):
        headerSetup = layout.column()
        # headerSetup.box().label(text = "Alternate Headers")
        prop_split(headerSetup, self, "sceneSetupPreset", "Scene Setup Preset")
        if self.sceneSetupPreset == "Custom":
            headerSetupBox = headerSetup.column()
            headerSetupBox.prop(self, "childDayHeader", text="Child Day")
            prevHeaderName = "childDayHeader"
            childNightRow = headerSetupBox.row()
            if altProp is None or altProp.childNightHeader.usePreviousHeader:
                # Draw previous header checkbox (so get previous state), but labeled
                # as current one and grayed out
                childNightRow.prop(self, prevHeaderName, text="Child Night")
                childNightRow.enabled = False
            else:
                childNightRow.prop(self, "childNightHeader", text="Child Night")
                prevHeaderName = "childNightHeader"
            adultDayRow = headerSetupBox.row()
            if altProp is None or altProp.adultDayHeader.usePreviousHeader:
                adultDayRow.prop(self, prevHeaderName, text="Adult Day")
                adultDayRow.enabled = False
            else:
                adultDayRow.prop(self, "adultDayHeader", text="Adult Day")
                prevHeaderName = "adultDayHeader"
            adultNightRow = headerSetupBox.row()
            if altProp is None or altProp.adultNightHeader.usePreviousHeader:
                adultNightRow.prop(self, prevHeaderName, text="Adult Night")
                adultNightRow.enabled = False
            else:
                adultNightRow.prop(self, "adultNightHeader", text="Adult Night")

            headerSetupBox.row().label(text="Cutscene headers to include this actor in:")
            for i in range(len(self.cutsceneHeaders)):
                headerItemProps: MMActorHeaderItemProperty = self.cutsceneHeaders[i]
                headerItemProps.draw_props(headerSetup, propUser, i, altProp, objName)
            drawAddButton(headerSetup, len(self.cutsceneHeaders), propUser, None, objName)


class MMActorProperty(PropertyGroup):
    actorID: EnumProperty(name="Actor", items=mmData.actorData.mmEnumActorID, default="ACTOR_PLAYER")
    actorIDCustom: StringProperty(name="Actor ID", default="ACTOR_PLAYER")
    actorParam: StringProperty(name="Actor Parameter", default="0x0000")
    rotOverride: BoolProperty(name="Override Rotation", default=False)
    rotOverrideX: StringProperty(name="Rot X", default="0")
    rotOverrideY: StringProperty(name="Rot Y", default="0")
    rotOverrideZ: StringProperty(name="Rot Z", default="0")
    headerSettings: PointerProperty(type=MMActorHeaderProperty)

    def draw_props(self, layout: UILayout, altRoomProp: MMAlternateRoomHeaderProperty, objName: str):
        # prop_split(layout, actorProp, 'actorID', 'Actor')
        actorIDBox = layout.column()
        # actorIDBox.box().label(text = "Settings")
        searchOp = actorIDBox.operator(MM_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
        searchOp.actorUser = "Actor"
        searchOp.objName = objName

        split = actorIDBox.split(factor=0.5)

        if self.actorID == "None":
            actorIDBox.box().label(text="This Actor was deleted from the XML file.")
            return

        split.label(text="Actor ID")
        split.label(text=getEnumName(mmData.actorData.mmEnumActorID, self.actorID))

        if self.actorID == "Custom":
            # actorIDBox.prop(actorProp, 'actorIDCustom', text = 'Actor ID')
            prop_split(actorIDBox, self, "actorIDCustom", "")

        # layout.box().label(text = 'Actor IDs defined in include/z64actors.h.')
        prop_split(actorIDBox, self, "actorParam", "Actor Parameter")

        actorIDBox.prop(self, "rotOverride", text="Override Rotation (ignore Blender rot)")
        if self.rotOverride:
            prop_split(actorIDBox, self, "rotOverrideX", "Rot X")
            prop_split(actorIDBox, self, "rotOverrideY", "Rot Y")
            prop_split(actorIDBox, self, "rotOverrideZ", "Rot Z")

        headerProp: MMActorHeaderProperty = self.headerSettings
        headerProp.draw_props(actorIDBox, "Actor", altRoomProp, objName)


class MMTransitionActorProperty(PropertyGroup):
    roomIndex: IntProperty(min=0)
    cameraTransitionFront: EnumProperty(items=mmEnumCamTransition, default="0x00")
    cameraTransitionFrontCustom: StringProperty(default="0x00")
    cameraTransitionBack: EnumProperty(items=mmEnumCamTransition, default="0x00")
    cameraTransitionBackCustom: StringProperty(default="0x00")
    dontTransition: BoolProperty(default=False)

    actor: PointerProperty(type=MMActorProperty)

    def draw_props(
        self, layout: UILayout, altSceneProp: MMAlternateSceneHeaderProperty, roomObj: Object, objName: str
    ):
        actorIDBox = layout.column()
        searchOp = actorIDBox.operator(MM_SearchActorIDEnumOperator.bl_idname, icon="VIEWZOOM")
        searchOp.actorUser = "Transition Actor"
        searchOp.objName = objName

        split = actorIDBox.split(factor=0.5)
        split.label(text="Actor ID")
        split.label(text=getEnumName(mmData.actorData.mmEnumActorID, self.actor.actorID))

        if self.actor.actorID == "Custom":
            prop_split(actorIDBox, self.actor, "actorIDCustom", "")

        # layout.box().label(text = 'Actor IDs defined in include/z64actors.h.')
        prop_split(actorIDBox, self.actor, "actorParam", "Actor Parameter")

        if roomObj is None:
            actorIDBox.label(text="This must be part of a Room empty's hierarchy.", icon="OUTLINER")
        else:
            actorIDBox.prop(self, "dontTransition")
            if not self.dontTransition:
                label_split(actorIDBox, "Room To Transition From", str(roomObj.mmRoomHeader.roomIndex))
                prop_split(actorIDBox, self, "roomIndex", "Room To Transition To")
        actorIDBox.label(text='Y+ side of door faces toward the "from" room.', icon="ORIENTATION_NORMAL")
        drawEnumWithCustom(actorIDBox, self, "cameraTransitionFront", "Camera Transition Front", "")
        drawEnumWithCustom(actorIDBox, self, "cameraTransitionBack", "Camera Transition Back", "")

        headerProps: MMActorHeaderProperty = self.actor.headerSettings
        headerProps.draw_props(actorIDBox, "Transition Actor", altSceneProp, objName)


class MMEntranceProperty(PropertyGroup):
    # This is also used in entrance list, and roomIndex is obtained from the room this empty is parented to.
    spawnIndex: IntProperty(min=0)
    customActor: BoolProperty(name="Use Custom Actor")
    actor: PointerProperty(type=MMActorProperty)

    def draw_props(self, layout: UILayout, obj: Object, altSceneProp: MMAlternateSceneHeaderProperty, objName: str):
        box = layout.column()
        # box.box().label(text = "Properties")
        roomObj = getRoomObj(obj)
        if roomObj is not None:
            split = box.split(factor=0.5)
            split.label(text="Room Index")
            split.label(text=str(roomObj.mmRoomHeader.roomIndex))
        else:
            box.label(text="This must be part of a Room empty's hierarchy.", icon="OUTLINER")

        entranceProp = obj.mmEntranceProperty
        prop_split(box, entranceProp, "spawnIndex", "Spawn Index")
        prop_split(box, entranceProp.actor, "actorParam", "Actor Param")
        box.prop(entranceProp, "customActor")
        if entranceProp.customActor:
            prop_split(box, entranceProp.actor, "actorIDCustom", "Actor ID Custom")

        headerProps: MMActorHeaderProperty = entranceProp.actor.headerSettings
        headerProps.draw_props(box, "Entrance", altSceneProp, objName)


classes = (
    MMActorHeaderItemProperty,
    MMActorHeaderProperty,
    MMActorProperty,
    MMTransitionActorProperty,
    MMEntranceProperty,
)


def mm_actor_props_register():
    for cls in classes:
        register_class(cls)

    Object.mmActorProperty = PointerProperty(type=MMActorProperty)
    Object.mmTransitionActorProperty = PointerProperty(type=MMTransitionActorProperty)
    Object.mmEntranceProperty = PointerProperty(type=MMEntranceProperty)


def mm_actor_props_unregister():
    del Object.mmActorProperty
    del Object.mmTransitionActorProperty
    del Object.mmEntranceProperty

    for cls in reversed(classes):
        unregister_class(cls)
