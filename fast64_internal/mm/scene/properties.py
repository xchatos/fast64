import os, bpy
from bpy.types import PropertyGroup, Object, Light, UILayout, Scene
from bpy.props import (
    EnumProperty,
    IntProperty,
    StringProperty,
    CollectionProperty,
    PointerProperty,
    BoolProperty,
    FloatVectorProperty,
)
from bpy.utils import register_class, unregister_class
from ...render_settings import on_update_mm_render_settings
from ...utility import prop_split, customExportWarning
from ..cutscene.properties import MMCSListProperty
from ..cutscene.operators import drawCSListAddOp
from ..cutscene.constants import mmEnumCSWriteType

from ..mm_utility import (
    onMenuTabChange,
    onHeaderMenuTabChange,
    drawCollectionOps,
    drawEnumWithCustom,
    drawAddButton,
    getEnumName,
)

from ..mm_constants import (
    mmEnumMusicSeq,
    mmEnumSceneID,
    mmEnumExitIndex,
    mmEnumTransitionAnims,
    mmEnumLightGroupMenu,
    mmEnumGlobalObject,
    mmEnumNaviHints,
    mmEnumSkybox,
    mmEnumCloudiness,
    mmEnumSkyboxLighting,
    mmEnumMapLocation,
    mmEnumCameraMode,
    mmEnumNightSeq,
    mmEnumAudioSessionPreset,
    mmEnumSceneMenu,
    mmEnumSceneMenuAlternate,
    mmEnumHeaderMenu,
    mmEnumDrawConfig,
    mmEnumHeaderMenuComplete,
)


class MMSceneCommon:
    mmEnumBootMode = [
        ("Play", "Play", "Play"),
        ("Map Select", "Map Select", "Map Select"),
        ("File Select", "File Select", "File Select"),
    ]

    def isSceneObj(self, obj):
        return obj.data is None and obj.mmEmptyType == "Scene"


class MMSceneProperties(PropertyGroup):
    write_dummy_room_list: BoolProperty(
        name="Dummy Room List",
        default=False,
        description=(
            "When exporting the scene to C, use NULL for the pointers to room "
            "start/end offsets, instead of the appropriate symbols"
        ),
    )


class MMExitProperty(PropertyGroup):
    expandTab: BoolProperty(name="Expand Tab")

    exitIndex: EnumProperty(items=mmEnumExitIndex, default="Default")
    exitIndexCustom: StringProperty(default="0x0000")

    # These are used when adding an entry to gEntranceTable
    scene: EnumProperty(items=mmEnumSceneID, default="SCENE_20SICHITAI2")
    sceneCustom: StringProperty(default="SCENE_20SICHITAI2")

    # These are used when adding an entry to gEntranceTable
    continueBGM: BoolProperty(default=False)
    displayTitleCard: BoolProperty(default=True)
    fadeInAnim: EnumProperty(items=mmEnumTransitionAnims, default="0x02")
    fadeInAnimCustom: StringProperty(default="0x02")
    fadeOutAnim: EnumProperty(items=mmEnumTransitionAnims, default="0x02")
    fadeOutAnimCustom: StringProperty(default="0x02")

    def draw_props(self, layout: UILayout, index: int, headerIndex: int, objName: str):
        box = layout.box()
        box.prop(self, "expandTab", text="Exit " + str(index + 1), icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT")
        if self.expandTab:
            drawCollectionOps(box, index, "Exit", headerIndex, objName)
            drawEnumWithCustom(box, self, "exitIndex", "Exit Index", "")
            if self.exitIndex != "Custom":
                box.label(text='This is unfinished, use "Custom".')
                exitGroup = box.column()
                exitGroup.enabled = False
                drawEnumWithCustom(exitGroup, self, "scene", "Scene", "")
                exitGroup.prop(self, "continueBGM", text="Continue BGM")
                exitGroup.prop(self, "displayTitleCard", text="Display Title Card")
                drawEnumWithCustom(exitGroup, self, "fadeInAnim", "Fade In Animation", "")
                drawEnumWithCustom(exitGroup, self, "fadeOutAnim", "Fade Out Animation", "")


class MMLightProperty(PropertyGroup):
    ambient: FloatVectorProperty(
        name="Ambient Color",
        size=4,
        min=0,
        max=1,
        default=(70 / 255, 40 / 255, 57 / 255, 1),
        subtype="COLOR",
        update=on_update_mm_render_settings,
    )
    useCustomDiffuse0: BoolProperty(name="Use Custom Diffuse 0 Light Object", update=on_update_mm_render_settings)
    useCustomDiffuse1: BoolProperty(name="Use Custom Diffuse 1 Light Object", update=on_update_mm_render_settings)
    diffuse0: FloatVectorProperty(
        name="",
        size=4,
        min=0,
        max=1,
        default=(180 / 255, 154 / 255, 138 / 255, 1),
        subtype="COLOR",
        update=on_update_mm_render_settings,
    )
    diffuse1: FloatVectorProperty(
        name="",
        size=4,
        min=0,
        max=1,
        default=(20 / 255, 20 / 255, 60 / 255, 1),
        subtype="COLOR",
        update=on_update_mm_render_settings,
    )
    diffuse0Custom: PointerProperty(name="Diffuse 0", type=Light, update=on_update_mm_render_settings)
    diffuse1Custom: PointerProperty(name="Diffuse 1", type=Light, update=on_update_mm_render_settings)
    fogColor: FloatVectorProperty(
        name="",
        size=4,
        min=0,
        max=1,
        default=(140 / 255, 120 / 255, 110 / 255, 1),
        subtype="COLOR",
        update=on_update_mm_render_settings,
    )
    fogNear: IntProperty(name="", default=993, min=0, max=2**10 - 1, update=on_update_mm_render_settings)
    transitionSpeed: IntProperty(name="", default=1, min=0, max=63, update=on_update_mm_render_settings)
    fogFar: IntProperty(name="", default=0x3200, min=0, max=2**16 - 1, update=on_update_mm_render_settings)
    expandTab: BoolProperty(name="Expand Tab")

    def draw_props(
        self, layout: UILayout, name: str, showExpandTab: bool, index: int, sceneHeaderIndex: int, objName: str
    ):
        if showExpandTab:
            box = layout.box().column()
            box.prop(self, "expandTab", text=name, icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT")
            expandTab = self.expandTab
        else:
            box = layout
            expandTab = True

        if expandTab:
            if index is not None:
                drawCollectionOps(box, index, "Light", sceneHeaderIndex, objName)
            prop_split(box, self, "ambient", "Ambient Color")

            if self.useCustomDiffuse0:
                prop_split(box, self, "diffuse0Custom", "Diffuse 0")
                box.label(text="Make sure light is not part of scene hierarchy.", icon="FILE_PARENT")
            else:
                prop_split(box, self, "diffuse0", "Diffuse 0")
            box.prop(self, "useCustomDiffuse0")

            if self.useCustomDiffuse1:
                prop_split(box, self, "diffuse1Custom", "Diffuse 1")
                box.label(text="Make sure light is not part of scene hierarchy.", icon="FILE_PARENT")
            else:
                prop_split(box, self, "diffuse1", "Diffuse 1")
            box.prop(self, "useCustomDiffuse1")

            prop_split(box, self, "fogColor", "Fog Color")
            prop_split(box, self, "fogNear", "Fog Near")
            prop_split(box, self, "fogFar", "Fog Far")
            prop_split(box, self, "transitionSpeed", "Transition Speed")


class MMLightGroupProperty(PropertyGroup):
    expandTab: BoolProperty()
    menuTab: EnumProperty(items=mmEnumLightGroupMenu)
    dawn: PointerProperty(type=MMLightProperty)
    day: PointerProperty(type=MMLightProperty)
    dusk: PointerProperty(type=MMLightProperty)
    night: PointerProperty(type=MMLightProperty)
    defaultsSet: BoolProperty()

    def draw_props(self, layout: UILayout):
        box = layout.column()
        box.row().prop(self, "menuTab", expand=True)
        if self.menuTab == "Dawn":
            self.dawn.draw_props(box, "Dawn", False, None, None, None)
        if self.menuTab == "Day":
            self.day.draw_props(box, "Day", False, None, None, None)
        if self.menuTab == "Dusk":
            self.dusk.draw_props(box, "Dusk", False, None, None, None)
        if self.menuTab == "Night":
            self.night.draw_props(box, "Night", False, None, None, None)


class MMSceneTableEntryProperty(PropertyGroup):
    drawConfig: EnumProperty(items=mmEnumDrawConfig, name="Scene Draw Config", default="SDC_DEFAULT")
    drawConfigCustom: StringProperty(name="Scene Draw Config Custom")
    hasTitle: BoolProperty(default=True)

    def draw_props(self, layout: UILayout):
        drawEnumWithCustom(layout, self, "drawConfig", "Draw Config", "")


class MMExtraCutsceneProperty(PropertyGroup):
    csObject: PointerProperty(
        name="Cutscene Object",
        type=Object,
        poll=lambda self, object: object.type == "EMPTY" and object.mmEmptyType == "Cutscene",
    )


class MMSceneHeaderProperty(PropertyGroup):
    expandTab: BoolProperty(name="Expand Tab")
    usePreviousHeader: BoolProperty(name="Use Previous Header", default=True)

    globalObject: EnumProperty(name="Global Object", default="OBJECT_GAMEPLAY_DANGEON_KEEP", items=mmEnumGlobalObject)
    globalObjectCustom: StringProperty(name="Global Object Custom", default="0x00")
    naviCup: EnumProperty(name="Navi Hints", default="0x00", items=mmEnumNaviHints)
    naviCupCustom: StringProperty(name="Navi Hints Custom", default="0x00")

    skyboxID: EnumProperty(name="Skybox", items=mmEnumSkybox, default="0x01")
    skyboxIDCustom: StringProperty(name="Skybox ID", default="0")
    skyboxCloudiness: EnumProperty(name="Cloudiness", items=mmEnumCloudiness, default="0x00")
    skyboxCloudinessCustom: StringProperty(name="Cloudiness ID", default="0x00")
    skyboxLighting: EnumProperty(
        name="Skybox Lighting",
        items=mmEnumSkyboxLighting,
        default="LIGHT_MODE_TIME",
        update=on_update_mm_render_settings,
    )
    skyboxLightingCustom: StringProperty(
        name="Skybox Lighting Custom", default="0x00", update=on_update_mm_render_settings
    )

    mapLocation: EnumProperty(name="Map Location", items=mmEnumMapLocation, default="0x00")
    mapLocationCustom: StringProperty(name="Skybox Lighting Custom", default="0x00")
    cameraMode: EnumProperty(name="Camera Mode", items=mmEnumCameraMode, default="0x00")
    cameraModeCustom: StringProperty(name="Camera Mode Custom", default="0x00")

    musicSeq: EnumProperty(name="Music Sequence", items=mmEnumMusicSeq, default="0x02")
    musicSeqCustom: StringProperty(name="Music Sequence ID", default="0x00")
    nightSeq: EnumProperty(name="Nighttime SFX", items=mmEnumNightSeq, default="0x00")
    nightSeqCustom: StringProperty(name="Nighttime SFX ID", default="0x00")
    audioSessionPreset: EnumProperty(name="Audio Session Preset", items=mmEnumAudioSessionPreset, default="0x00")
    audioSessionPresetCustom: StringProperty(name="Audio Session Preset", default="0x00")

    timeOfDayLights: PointerProperty(type=MMLightGroupProperty, name="Time Of Day Lighting")
    lightList: CollectionProperty(type=MMLightProperty, name="Lighting List")
    exitList: CollectionProperty(type=MMExitProperty, name="Exit List")

    writeCutscene: BoolProperty(name="Write Cutscene")
    csWriteType: EnumProperty(name="Cutscene Data Type", items=mmEnumCSWriteType, default="Embedded")
    csWriteCustom: StringProperty(name="CS hdr var:", default="")
    csWriteObject: PointerProperty(
        name="Cutscene Object",
        type=Object,
        poll=lambda self, object: object.type == "EMPTY" and object.mmEmptyType == "Cutscene",
    )

    # These properties are for the deprecated "Embedded" cutscene type. They have
    # not been removed as doing so would break any existing scenes made with this
    # type of cutscene data.
    csEndFrame: IntProperty(name="End Frame", min=0, default=100)
    csWriteTerminator: BoolProperty(name="Write Terminator (Code Execution)")
    csTermIdx: IntProperty(name="Index", min=0)
    csTermStart: IntProperty(name="Start Frm", min=0, default=99)
    csTermEnd: IntProperty(name="End Frm", min=0, default=100)
    csLists: CollectionProperty(type=MMCSListProperty, name="Cutscene Lists")

    extraCutscenes: CollectionProperty(type=MMExtraCutsceneProperty, name="Extra Cutscenes")

    sceneTableEntry: PointerProperty(type=MMSceneTableEntryProperty)

    menuTab: EnumProperty(name="Menu", items=mmEnumSceneMenu, update=onMenuTabChange)
    altMenuTab: EnumProperty(name="Menu", items=mmEnumSceneMenuAlternate)

    appendNullEntrance: BoolProperty(
        name="Append Null Entrance",
        description="Add an additional {0, 0} to the end of the EntranceEntry list.",
        default=False,
    )

    def draw_props(self, layout: UILayout, dropdownLabel: str, headerIndex: int, objName: str):
        from .operators import MM_SearchMusicSeqEnumOperator  # temp circular import fix

        if dropdownLabel is not None:
            layout.prop(self, "expandTab", text=dropdownLabel, icon="TRIA_DOWN" if self.expandTab else "TRIA_RIGHT")
            if not self.expandTab:
                return
        if headerIndex is not None and headerIndex > 3:
            drawCollectionOps(layout, headerIndex - 4, "Scene", None, objName)

        if headerIndex is not None and headerIndex > 0 and headerIndex < 4:
            layout.prop(self, "usePreviousHeader", text="Use Previous Header")
            if self.usePreviousHeader:
                return

        if headerIndex is None or headerIndex == 0:
            layout.row().prop(self, "menuTab", expand=True)
            menuTab = self.menuTab
        else:
            layout.row().prop(self, "altMenuTab", expand=True)
            menuTab = self.altMenuTab

        if menuTab == "General":
            general = layout.column()
            general.box().label(text="General")
            drawEnumWithCustom(general, self, "globalObject", "Global Object", "")
            drawEnumWithCustom(general, self, "naviCup", "Navi Hints", "")
            if headerIndex is None or headerIndex == 0:
                self.sceneTableEntry.draw_props(general)
            general.prop(self, "appendNullEntrance")

            skyboxAndSound = layout.column()
            skyboxAndSound.box().label(text="Skybox And Sound")
            drawEnumWithCustom(skyboxAndSound, self, "skyboxID", "Skybox", "")
            drawEnumWithCustom(skyboxAndSound, self, "skyboxCloudiness", "Cloudiness", "")
            drawEnumWithCustom(skyboxAndSound, self, "musicSeq", "Music Sequence", "")
            musicSearch = skyboxAndSound.operator(MM_SearchMusicSeqEnumOperator.bl_idname, icon="VIEWZOOM")
            musicSearch.objName = objName
            musicSearch.headerIndex = headerIndex if headerIndex is not None else 0
            drawEnumWithCustom(skyboxAndSound, self, "nightSeq", "Nighttime SFX", "")
            drawEnumWithCustom(skyboxAndSound, self, "audioSessionPreset", "Audio Session Preset", "")

            cameraAndWorldMap = layout.column()
            cameraAndWorldMap.box().label(text="Camera And World Map")
            drawEnumWithCustom(cameraAndWorldMap, self, "mapLocation", "Map Location", "")
            drawEnumWithCustom(cameraAndWorldMap, self, "cameraMode", "Camera Mode", "")

        elif menuTab == "Lighting":
            lighting = layout.column()
            lighting.box().label(text="Lighting List")
            drawEnumWithCustom(lighting, self, "skyboxLighting", "Lighting Mode", "")
            if self.skyboxLighting == "LIGHT_MODE_TIME":  # Time of Day
                self.timeOfDayLights.draw_props(lighting)
            else:
                for i in range(len(self.lightList)):
                    self.lightList[i].draw_props(lighting, "Lighting " + str(i), True, i, headerIndex, objName)
                drawAddButton(lighting, len(self.lightList), "Light", headerIndex, objName)

        elif menuTab == "Cutscene":
            cutscene = layout.column()
            r = cutscene.row()
            r.prop(self, "writeCutscene", text="Write Cutscene")
            if self.writeCutscene:
                r.prop(self, "csWriteType", text="Data")
                if self.csWriteType == "Custom":
                    cutscene.prop(self, "csWriteCustom")
                elif self.csWriteType == "Object":
                    cutscene.prop(self, "csWriteObject")
                else:
                    # This is the GUI setup / drawing for the properties for the
                    # deprecated "Embedded" cutscene type. They have not been removed
                    # as doing so would break any existing scenes made with this type
                    # of cutscene data.
                    cutscene.label(text='Embedded cutscenes are deprecated. Please use "Object" instead.')
                    cutscene.prop(self, "csEndFrame", text="End Frame")
                    cutscene.prop(self, "csWriteTerminator", text="Write Terminator (Code Execution)")
                    if self.csWriteTerminator:
                        r = cutscene.row()
                        r.prop(self, "csTermIdx", text="Index")
                        r.prop(self, "csTermStart", text="Start Frm")
                        r.prop(self, "csTermEnd", text="End Frm")
                    collectionType = "CSHdr." + str(0 if headerIndex is None else headerIndex)
                    for i, p in enumerate(self.csLists):
                        p.draw_props(cutscene, i, objName, collectionType)
                    drawCSListAddOp(cutscene, objName, collectionType)
            if headerIndex is None or headerIndex == 0:
                cutscene.label(text="Extra cutscenes (not in any header):")
                for i in range(len(self.extraCutscenes)):
                    box = cutscene.box().column()
                    drawCollectionOps(box, i, "extraCutscenes", None, objName, True)
                    box.prop(self.extraCutscenes[i], "csObject", text="CS obj")
                if len(self.extraCutscenes) == 0:
                    drawAddButton(cutscene, 0, "extraCutscenes", 0, objName)

        elif menuTab == "Exits":
            exitBox = layout.column()
            exitBox.box().label(text="Exit List")
            for i in range(len(self.exitList)):
                self.exitList[i].draw_props(exitBox, i, headerIndex, objName)

            drawAddButton(exitBox, len(self.exitList), "Exit", headerIndex, objName)


class MMAlternateSceneHeaderProperty(PropertyGroup):
    childNightHeader: PointerProperty(name="Child Night Header", type=MMSceneHeaderProperty)
    adultDayHeader: PointerProperty(name="Adult Day Header", type=MMSceneHeaderProperty)
    adultNightHeader: PointerProperty(name="Adult Night Header", type=MMSceneHeaderProperty)
    cutsceneHeaders: CollectionProperty(type=MMSceneHeaderProperty)

    headerMenuTab: EnumProperty(name="Header Menu", items=mmEnumHeaderMenu, update=onHeaderMenuTabChange)
    currentCutsceneIndex: IntProperty(min=4, default=4, update=onHeaderMenuTabChange)

    def draw_props(self, layout: UILayout, objName: str):
        headerSetup = layout.column()
        # headerSetup.box().label(text = "Alternate Headers")
        headerSetupBox = headerSetup.column()

        headerSetupBox.row().prop(self, "headerMenuTab", expand=True)
        if self.headerMenuTab == "Child Night":
            self.childNightHeader.draw_props(headerSetupBox, None, 1, objName)
        elif self.headerMenuTab == "Adult Day":
            self.adultDayHeader.draw_props(headerSetupBox, None, 2, objName)
        elif self.headerMenuTab == "Adult Night":
            self.adultNightHeader.draw_props(headerSetupBox, None, 3, objName)
        elif self.headerMenuTab == "Cutscene":
            prop_split(headerSetup, self, "currentCutsceneIndex", "Cutscene Index")
            drawAddButton(headerSetup, len(self.cutsceneHeaders), "Scene", None, objName)
            index = self.currentCutsceneIndex
            if index - 4 < len(self.cutsceneHeaders):
                self.cutsceneHeaders[index - 4].draw_props(headerSetup, None, index, objName)
            else:
                headerSetup.label(text="No cutscene header for this index.", icon="QUESTION")


class MMBootupSceneOptions(PropertyGroup):
    bootToScene: BoolProperty(default=False, name="Boot To Scene")
    overrideHeader: BoolProperty(default=False, name="Override Header")
    headerOption: EnumProperty(items=mmEnumHeaderMenuComplete, name="Header", default="Child Day")
    spawnIndex: IntProperty(name="Spawn", min=0)
    newGameOnly: BoolProperty(
        default=False,
        name="Override Scene On New Game Only",
        description="Only use this starting scene after loading a new save file",
    )
    newGameName: StringProperty(default="Link", name="New Game Name")
    bootMode: EnumProperty(default="Play", name="Boot Mode", items=MMSceneCommon.mmEnumBootMode)

    # see src/code/z_play.c:Play_Init() - can't access more than 16 cutscenes?
    cutsceneIndex: IntProperty(min=4, max=19, default=4, name="Cutscene Index")

    def draw_props(self, layout: UILayout):
        layout.prop(self, "bootToScene", text="Boot To Scene (Hackeroot)")
        if self.bootToScene:
            layout.prop(self, "newGameOnly")
            prop_split(layout, self, "bootMode", "Boot Mode")
            if self.bootMode == "Play":
                prop_split(layout, self, "newGameName", "New Game Name")
            if self.bootMode != "Map Select":
                prop_split(layout, self, "spawnIndex", "Spawn")
                layout.prop(self, "overrideHeader")
                if self.overrideHeader:
                    prop_split(layout, self, "headerOption", "Header Option")
                    if self.headerOption == "Cutscene":
                        prop_split(layout, self, "cutsceneIndex", "Cutscene Index")


class MMRemoveSceneSettingsProperty(PropertyGroup):
    name: StringProperty(name="Name", default="spot03")
    subFolder: StringProperty(name="Subfolder", default="overworld")
    customExport: BoolProperty(name="Custom Export Path")
    option: EnumProperty(items=mmEnumSceneID, default="SCENE_20SICHITAI2")

    def draw_props(self, layout: UILayout):
        if self.option == "Custom":
            prop_split(layout, self, "subFolder", "Subfolder")
            prop_split(layout, self, "name", "Name")


class MMExportSceneSettingsProperty(PropertyGroup):
    name: StringProperty(name="Name", default="spot03")
    subFolder: StringProperty(name="Subfolder", default="overworld")
    exportPath: StringProperty(name="Directory", subtype="FILE_PATH")
    customExport: BoolProperty(name="Custom Export Path")
    singleFile: BoolProperty(
        name="Export as Single File",
        default=False,
        description="Does not split the scene and rooms into multiple files.",
    )
    option: EnumProperty(items=mmEnumSceneID, default="SCENE_20SICHITAI2")

    def draw_props(self, layout: UILayout):
        if self.customExport:
            prop_split(layout, self, "exportPath", "Directory")
            prop_split(layout, self, "name", "Name")
            customExportWarning(layout)
        else:
            if self.option == "Custom":
                prop_split(layout, self, "subFolder", "Subfolder")
                prop_split(layout, self, "name", "Name")

        prop_split(layout, bpy.context.scene, "mmSceneExportObj", "Scene Object")

        layout.prop(self, "singleFile")
        layout.prop(self, "customExport")


class MMImportSceneSettingsProperty(PropertyGroup):
    name: StringProperty(name="Name", default="spot03")
    subFolder: StringProperty(name="Subfolder", default="overworld")
    destPath: StringProperty(name="Directory", subtype="FILE_PATH")
    isCustomDest: BoolProperty(name="Custom Path")
    includeMesh: BoolProperty(name="Mesh", default=True)
    includeCollision: BoolProperty(name="Collision", default=True)
    includeActors: BoolProperty(name="Actors", default=True)
    includeCullGroups: BoolProperty(name="Cull Groups", default=True)
    includeLights: BoolProperty(name="Lights", default=True)
    includeCameras: BoolProperty(name="Cameras", default=True)
    includePaths: BoolProperty(name="Paths", default=True)
    includeWaterBoxes: BoolProperty(name="Water Boxes", default=True)
    includeCutscenes: BoolProperty(name="Cutscenes", default=False)
    option: EnumProperty(items=mmEnumSceneID, default="SCENE_20SICHITAI2")

    def draw_props(self, layout: UILayout, sceneOption: str):
        col = layout.column()
        includeButtons1 = col.row(align=True)
        includeButtons1.prop(self, "includeMesh", toggle=1)
        includeButtons1.prop(self, "includeCollision", toggle=1)
        includeButtons1.prop(self, "includeActors", toggle=1)

        includeButtons2 = col.row(align=True)
        includeButtons2.prop(self, "includeCullGroups", toggle=1)
        includeButtons2.prop(self, "includeLights", toggle=1)
        includeButtons2.prop(self, "includeCameras", toggle=1)

        includeButtons3 = col.row(align=True)
        includeButtons3.prop(self, "includePaths", toggle=1)
        includeButtons3.prop(self, "includeWaterBoxes", toggle=1)
        includeButtons3.prop(self, "includeCutscenes", toggle=1)
        col.prop(self, "isCustomDest")

        if self.isCustomDest:
            prop_split(col, self, "destPath", "Directory")
            prop_split(col, self, "name", "Name")
        else:
            if self.option == "Custom":
                prop_split(col, self, "subFolder", "Subfolder")
                prop_split(col, self, "name", "Name")

        if "SCENE_JABU_JABU" in sceneOption:
            col.label(text="Pulsing wall effect won't be imported.", icon="ERROR")


classes = (
    MMExitProperty,
    MMLightProperty,
    MMLightGroupProperty,
    MMSceneTableEntryProperty,
    MMExtraCutsceneProperty,
    MMSceneHeaderProperty,
    MMAlternateSceneHeaderProperty,
    MMBootupSceneOptions,
    MMRemoveSceneSettingsProperty,
    MMExportSceneSettingsProperty,
    MMImportSceneSettingsProperty,
)


def mm_scene_props_register():
    for cls in classes:
        register_class(cls)

    Object.mmSceneHeader = PointerProperty(type=MMSceneHeaderProperty)
    Object.mmAlternateSceneHeaders = PointerProperty(type=MMAlternateSceneHeaderProperty)
    Scene.mmSceneExportObj = PointerProperty(type=Object, poll=MMSceneCommon.isSceneObj)
    Scene.mmSceneExportSettings = PointerProperty(type=MMExportSceneSettingsProperty)
    Scene.mmSceneImportSettings = PointerProperty(type=MMImportSceneSettingsProperty)
    Scene.mmSceneRemoveSettings = PointerProperty(type=MMRemoveSceneSettingsProperty)


def mm_scene_props_unregister():
    del Object.mmSceneHeader
    del Object.mmAlternateSceneHeaders
    del Scene.mmSceneExportObj
    del Scene.mmSceneExportSettings
    del Scene.mmSceneImportSettings
    del Scene.mmSceneRemoveSettings

    for cls in reversed(classes):
        unregister_class(cls)
