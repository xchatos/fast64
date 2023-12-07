import bpy
from bpy.utils import register_class, unregister_class
from ..utility import prop_split, gammaInverse
from .mm_constants import mmEnumEmptyType
from .mm_utility import getSceneObj, getRoomObj
from .scene.properties import MMSceneProperties
from .room.properties import MMObjectProperty, MMRoomHeaderProperty, MMAlternateRoomHeaderProperty
from .collision.properties import MMWaterBoxProperty
from .cutscene.properties import MMCutsceneProperty
from .cutscene.motion.properties import (
    MMCutsceneMotionProperty,
    MMCSMotionActorCueListProperty,
    MMCSMotionActorCueProperty,
)

from .actor.properties import (
    MMActorProperty,
    MMTransitionActorProperty,
    MMEntranceProperty,
)


def drawSceneHeader(box: bpy.types.UILayout, obj: bpy.types.Object):
    objName = obj.name
    obj.mmSceneHeader.draw_props(box, None, None, objName)
    if obj.mmSceneHeader.menuTab == "Alternate":
        obj.mmAlternateSceneHeaders.draw_props(box, objName)
    box.prop(obj.fast64.mm.scene, "write_dummy_room_list")


def drawLODProperty(box, obj):
    col = box.column()
    col.box().label(text="LOD Settings (Blender Units)")
    for otherObj in obj.children:
        if bpy.context.scene.exportHiddenGeometry or not otherObj.hide_get():
            prop_split(col, otherObj, "f3d_lod_z", otherObj.name)
    col.prop(obj, "f3d_lod_always_render_farthest")


def setLightPropertyValues(lightProp, ambient, diffuse0, diffuse1, fogColor, fogNear):
    lightProp.ambient = gammaInverse([value / 255 for value in ambient]) + [1]
    lightProp.diffuse0 = gammaInverse([value / 255 for value in diffuse0]) + [1]
    lightProp.diffuse1 = gammaInverse([value / 255 for value in diffuse1]) + [1]
    lightProp.fogColor = gammaInverse([value / 255 for value in fogColor]) + [1]
    lightProp.fogNear = fogNear


def onUpdateMMEmptyType(self, context):
    isNoneEmpty = self.mmEmptyType == "None"
    isBoxEmpty = self.mmEmptyType == "Water Box"
    isSphereEmpty = self.mmEmptyType == "Cull Group"
    self.show_name = not (isBoxEmpty or isNoneEmpty or isSphereEmpty)
    self.show_axis = not (isBoxEmpty or isNoneEmpty or isSphereEmpty)

    if isBoxEmpty:
        self.empty_display_type = "CUBE"

    if isSphereEmpty:
        self.empty_display_type = "SPHERE"

    if self.mmEmptyType == "Scene":
        if len(self.mmSceneHeader.lightList) == 0:
            light = self.mmSceneHeader.lightList.add()
        if not self.mmSceneHeader.timeOfDayLights.defaultsSet:
            self.mmSceneHeader.timeOfDayLights.defaultsSet = True
            timeOfDayLights = self.mmSceneHeader.timeOfDayLights
            setLightPropertyValues(
                timeOfDayLights.dawn, [70, 45, 57], [180, 154, 138], [20, 20, 60], [140, 120, 100], 0x3E1
            )
            setLightPropertyValues(
                timeOfDayLights.day, [105, 90, 90], [255, 255, 240], [50, 50, 90], [100, 100, 120], 0x3E4
            )
            setLightPropertyValues(
                timeOfDayLights.dusk, [120, 90, 0], [250, 135, 50], [30, 30, 60], [120, 70, 50], 0x3E3
            )
            setLightPropertyValues(timeOfDayLights.night, [40, 70, 100], [20, 20, 35], [50, 50, 100], [0, 0, 30], 0x3E0)


class MM_ManualUpgrade(bpy.types.Operator):
    bl_idname = "object.mm_manual_upgrade"
    bl_label = "Upgrade Fast64 MM Object Data"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context):
        MM_ObjectProperties.upgrade_changed_props()
        return {"FINISHED"}


class MMObjectPanel(bpy.types.Panel):
    bl_label = "Object Inspector"
    bl_idname = "OBJECT_PT_MM_Object_Inspector"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.gameEditorMode == "MM"  and (context.object is not None and context.object.data is None)

    def draw(self, context):
        prop_split(self.layout, context.scene, "gameEditorMode", "Game")
        box = self.layout.box()
        box.box().label(text="MM Object Inspector")
        obj = context.object
        objName = obj.name
        prop_split(box, obj, "mmEmptyType", "Object Type")

        sceneObj = getSceneObj(obj)
        roomObj = getRoomObj(obj)

        altSceneProp = sceneObj.mmAlternateSceneHeaders if sceneObj is not None else None
        altRoomProp = roomObj.mmAlternateRoomHeaders if roomObj is not None else None

        if obj.mmEmptyType == "Actor":
            actorProp: MMActorProperty = obj.mmActorProperty
            actorProp.draw_props(box, altRoomProp, objName)

        elif obj.mmEmptyType == "Transition Actor":
            transActorProp: MMTransitionActorProperty = obj.mmTransitionActorProperty
            transActorProp.draw_props(box, altSceneProp, roomObj, objName)

        elif obj.mmEmptyType == "Water Box":
            waterBoxProps: MMWaterBoxProperty = obj.mmWaterBoxProperty
            waterBoxProps.draw_props(box)

        elif obj.mmEmptyType == "Scene":
            drawSceneHeader(box, obj)

        elif obj.mmEmptyType == "Room":
            roomProp: MMRoomHeaderProperty = obj.mmRoomHeader
            roomProp.draw_props(box, None, None, objName)
            if obj.mmRoomHeader.menuTab == "Alternate":
                roomAltProp: MMAlternateRoomHeaderProperty = obj.mmAlternateRoomHeaders
                roomAltProp.draw_props(box, objName)

        elif obj.mmEmptyType == "Entrance":
            entranceProp: MMEntranceProperty = obj.mmEntranceProperty
            entranceProp.draw_props(box, obj, altSceneProp, objName)

        elif obj.mmEmptyType == "Cull Group":
            cullGroupProp: MMCullGroupProperty = obj.mmCullGroupProperty
            cullGroupProp.draw_props(box)

        elif obj.mmEmptyType == "LOD":
            drawLODProperty(box, obj)

        elif obj.mmEmptyType == "Cutscene":
            csProp: MMCutsceneProperty = obj.mmCutsceneProperty
            csProp.draw_props(box, obj)

        elif obj.mmEmptyType in [
            "CS Actor Cue List",
            "CS Player Cue List",
            "CS Actor Cue Preview",
            "CS Player Cue Preview",
        ]:
            labelPrefix = "Player" if "Player" in obj.mmEmptyType else "Actor"
            actorCueListProp: MMCSMotionActorCueListProperty = obj.mmCSMotionProperty.actorCueListProp
            actorCueListProp.draw_props(box, obj.mmEmptyType == f"CS {labelPrefix} Cue Preview", labelPrefix, obj.name)

        elif obj.mmEmptyType in ["CS Actor Cue", "CS Player Cue", "CS Dummy Cue"]:
            labelPrefix = "Player" if obj.parent.mmEmptyType == "CS Player Cue List" else "Actor"
            actorCueProp: MMCSMotionActorCueProperty = obj.mmCSMotionProperty.actorCueProp
            actorCueProp.draw_props(box, labelPrefix, obj.mmEmptyType == "CS Dummy Cue", obj.name)

        elif obj.mmEmptyType == "None":
            box.label(text="Geometry can be parented to this.")


class MM_ObjectProperties(bpy.types.PropertyGroup):
    scene: bpy.props.PointerProperty(type=MMSceneProperties)

    @staticmethod
    def upgrade_changed_props():
        for obj in bpy.data.objects:
            if obj.type == "EMPTY":
                if obj.mmEmptyType == "Room":
                    MMObjectProperty.upgrade_object(obj)
                if any(obj.name.startswith(elem) for elem in ["ActionList.", "Point.", "Preview."]):
                    MMCutsceneMotionProperty.upgrade_object(obj)

                    if "Point." in obj.name:
                        parentObj = obj.parent
                        if parentObj is not None:
                            if parentObj.children[-1] == obj:
                                obj.mmEmptyType = "CS Dummy Cue"
                        else:
                            print("WARNING: An Actor Cue has been detected outside an Actor Cue List: " + obj.name)
            elif obj.type == "ARMATURE":
                if obj.parent.name.startswith("Cutscene.") or obj.parent.mmEmptyType == "Cutscene":
                    MMCutsceneMotionProperty.upgrade_object(obj)


class MMCullGroupProperty(bpy.types.PropertyGroup):
    sizeControlsCull: bpy.props.BoolProperty(default=True, name="Empty Size Controls Cull Depth")
    manualRadius: bpy.props.IntProperty(min=0)

    def draw_props(self, layout: bpy.types.UILayout):
        col = layout.column()
        col.prop(self, "sizeControlsCull")
        if not self.sizeControlsCull:
            prop_split(col, self, "manualRadius", "Radius (MM Units)")
        col.label(text="Meshes generate cull groups automatically.", icon="INFO")
        col.label(text="This is only for custom cull group shapes.")
        col.label(text="Use Options -> Transform -> Affect Only -> Parent ", icon="INFO")
        col.label(text="to move object without affecting children.")


mm_obj_classes = (
    MMSceneProperties,
    MM_ObjectProperties,
    MMCullGroupProperty,
    MM_ManualUpgrade,
)

mm_obj_panel_classes = (MMObjectPanel,)


def mm_obj_panel_register():
    for cls in mm_obj_panel_classes:
        register_class(cls)


def mm_obj_panel_unregister():
    for cls in mm_obj_panel_classes:
        unregister_class(cls)


def mm_obj_register():
    for cls in mm_obj_classes:
        register_class(cls)

    bpy.types.Object.mmEmptyType = bpy.props.EnumProperty(
        name="MM Object Type", items=mmEnumEmptyType, default="None", update=onUpdateMMEmptyType
    )

    bpy.types.Scene.mmActiveHeaderLock = bpy.props.BoolProperty(default=False)
    bpy.types.Object.mmCullGroupProperty = bpy.props.PointerProperty(type=MMCullGroupProperty)


def mm_obj_unregister():
    del bpy.types.Scene.mmActiveHeaderLock
    del bpy.types.Object.mmEmptyType
    del bpy.types.Object.mmCullGroupProperty

    for cls in reversed(mm_obj_classes):
        unregister_class(cls)
