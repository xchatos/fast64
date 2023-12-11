import math
from ..utility import PluginError
from .mm_utility import BoxEmpty, convertIntTo2sComplement, getCustomProperty

mmEnumConveyer = [
    ("None", "None", "None"),
    ("Land", "Land", "Land"),
    ("Water", "Water", "Water"),
]

mmEnumFloorSetting = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x05", "Void (Small)", "Void (Small)"),
    ("0x06", "Grab Wall", "Grab Wall"),
    ("0x08", "Stop Air Momentum", "Stop Air Momentum"),
    ("0x09", "Fall Instead Of Jumping", "Fall Instead Of Jumping"),
    ("0x0B", "Dive", "Dive"),
    ("0x0C", "Void (Large)", "Void (Large)"),
]

mmEnumWallSetting = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "No Ledge Grab", "No Ledge Grab"),
    ("0x02", "Ladder", "Ladder"),
    ("0x03", "Ladder Top", "Ladder Top"),
    ("0x04", "Vines", "Vines"),
    ("0x05", "Crawl Space", "Crawl Space"),
    ("0x06", "Crawl Space 2", "Crawl Space 2"),
    ("0x07", "Push Block", "Push Block"),
]

mmEnumFloorProperty = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Haunted Wasteland Camera", "Haunted Wasteland Camera"),
    ("0x02", "Hurt Floor (Spikes)", "Hurt Floor (Spikes)"),
    ("0x03", "Hurt Floor (Lava)", "Hurt Floor (Lava)"),
    ("0x04", "Shallow Sand", "Shallow Sand"),
    ("0x05", "Slippery", "Slippery"),
    ("0x06", "No Fall Damage", "No Fall Damage"),
    ("0x07", "Quicksand Crossing (Epona Uncrossable)", "Quicksand Crossing (Epona Uncrossable)"),
    ("0x08", "Jabu Jabu's Belly", "Jabu Jabu's Belly"),
    ("0x09", "Void", "Void"),
    ("0x0A", "Link Looks Up", "Link Looks Up"),
    ("0x0B", "Quicksand Crossing (Epona Crossable)", "Quicksand Crossing (Epona Crossable)"),
]

mmEnumCollisionTerrain = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Walkable", "Walkable"),
    ("0x01", "Steep", "Steep"),
    ("0x02", "Walkable (Preserves Exit Flags)", "Walkable (Preserves Exit Flags)"),
    ("0x03", "Walkable (?)", "Walkable (?)"),
]

mmEnumCollisionSound = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Dirt", "Dirt (aka Earth)"),
    ("0x01", "Sand", "Sand"),
    ("0x02", "Stone", "Stone"),
    ("0x03", "Shallow Dirt", "Shallow Dirt"),
    ("0x04", "Shallow Water", "Shallow Water"),
    ("0x05", "Deep Water", "Deep Water"),
    ("0x06", "Tall Grass", "Tall Grass"),
    ("0x07", "Lava", "Lava (aka Goo)"),
    ("0x08", "Grass", "Grass (aka Earth 2)"),
    ("0x09", "Carpet", "Carpet (aka Loose Earth)"),
    ("0x0A", "Wood", "Wood (aka Packed Earth)"),
    ("0x0B", "Bridge", "Bridge (WOOD_PLANK)"),
    ("0x0C", "Vine", "Vine"),
    ("0x0D", "Deep Dirt", "Deep Dirt"),
    ("0x0E", "Snow", "Snow"),
    ("0x0F", "Ice", "Ice"),
]

mmEnumConveyorSpeed = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Slow", "Slow"),
    ("0x02", "Medium", "Medium"),
    ("0x03", "Fast", "Fast"),
]

mmEnumCameraCrawlspaceSType = [
    ("Custom", "Custom", "Custom"),
    ("CAM_SET_CRAWLSPACE", "Crawlspace", "Crawlspace"),
]

mmEnumCameraSType = [
    ("Custom", "Custom", "Custom"),
    ("CAM_SET_NONE", "Cam_set_none", "Cam_set_none"),
    ("CAM_SET_NORMAL0", "Cam_set_normal0", "Generic camera 0, used in various places NORMAL0"),
    ("CAM_SET_NORMAL3", "Cam_set_normal3", "Generic camera 3, used in various places NORMAL3"),
    ("CAM_SET_PIVOT_DIVING", "Cam_set_pivot_diving", "Player diving from the surface of the water to underwater not as zora CIRCLE5"),
    ("CAM_SET_HORSE", "Cam_set_horse", "Reiding a horse HORSE0"),
    ("CAM_SET_ZORA_DIVING", "Cam_set_zora_diving", "Parallel's Pivot Diving, but as Zora. However, Zora does not dive like a human. So this setting appears to not be used ZORA0"),
    ("CAM_SET_PREREND_FIXED", "Cam_set_prerend_fixed", "Unused remnant of OoT: camera is fixed in position and rotation PREREND0"),
    ("CAM_SET_PREREND_PIVOT", "Cam_set_prerend_pivot", "Unused remnant of OoT: Camera is fixed in position with fixed pitch, but is free to rotate in the yaw direction 360 degrees PREREND1"),
    ("CAM_SET_DOORC", "Cam_set_doorc", "Generic room door transitions, camera moves and follows player as the door is open and closed DOORC"),
    ("CAM_SET_DEMO0", "Cam_set_demo0", "Unknown, possibly related to treasure chest game as goron? DEMO0"),
    ("CAM_SET_FREE0", "Cam_set_free0", "Free Camera, manual control is given, no auto-updating eye or at FREE0"),
    ("CAM_SET_BIRDS_EYE_VIEW_0", "Cam_set_birds_eye_view_0", "Appears unused. Camera is a top-down view FUKAN0"),
    ("CAM_SET_NORMAL1", "Cam_set_normal1", "Generic camera 1, used in various places NORMAL1"),
    ("CAM_SET_NANAME", "Cam_set_naname", "Unknown, slanted or tilted. Behaves identical to Normal0 except with added roll NANAME"),
    ("CAM_SET_CIRCLE0", "Cam_set_circle0", "Used in Curiosity Shop, Pirates Fortress, Mayor's Residence CIRCLE0"),
    ("CAM_SET_FIXED0", "Cam_set_fixed0", "Used in Sakon's Hideout puzzle rooms, milk bar stage FIXED0"),
    ("CAM_SET_SPIRAL_DOOR", "Cam_set_spiral_door", "Exiting a Spiral Staircase SPIRAL"),
    ("CAM_SET_DUNGEON0", "Cam_set_dungeon0", "Generic dungeon camera 0, used in various places DUNGEON0"),
    ("CAM_SET_ITEM0", "Cam_set_item0", "Getting an item and holding it above Player's head (from small chest, freestanding, npc, ...) ITEM0"),
    ("CAM_SET_ITEM1", "Cam_set_item1", "Looking at player while playing the ocarina ITEM1"),
    ("CAM_SET_ITEM2", "Cam_set_item2", "Bottles: drinking, releasing fairy, dropping fish ITEM2"),
    ("CAM_SET_ITEM3", "Cam_set_item3", "Bottles: catching fish or bugs, showing an item ITEM3"),
    ("CAM_SET_NAVI", "Cam_set_navi", "Song of Soaring, variations of playing Song of Time NAVI"),
    ("CAM_SET_WARP_PAD_MOON", "Cam_set_warp_pad_moon", "Warp circles from Goron Trial on the moon WARP0"),
    ("CAM_SET_DEATH", "Cam_set_death", "Player death animation when health goes to 0 DEATH"),
    ("CAM_SET_REBIRTH", "Cam_set_rebirth", "Unknown set with camDataId = -9 (it's not being revived by a fairy) REBIRTH"),
    ("CAM_SET_LONG_CHEST_OPENING", "Cam_set_long_chest_opening", "Long cutscene when opening a big chest with a major item TREASURE"),
    ("CAM_SET_MASK_TRANSFORMATION", "Cam_set_mask_transformation", "Putting on a transformation mask TRANSFORM"),
    ("CAM_SET_ATTENTION", "Cam_set_attention", "Unknown, set with camDataId = -15 ATTENTION"),
    ("CAM_SET_WARP_PAD_ENTRANCE", "Cam_set_warp_pad_entrance", "Warp pad from start of a dungeon to the boss-room WARP1"),
    ("CAM_SET_DUNGEON1", "Cam_set_dungeon1", "Generic dungeon camera 1, used in various places DUNGEON1"),
    ("CAM_SET_FIXED1", "Cam_set_fixed1", "Fixes camera in place, used in various places eg. entering Stock Pot Inn, hiting a switch, giving witch a red potion, shop browsing FIXED1"),
    ("CAM_SET_FIXED2", "Cam_set_fixed2", "Used in Pinnacle Rock after defeating Sea Monsters, and by Tatl in Fortress FIXED2"),
    ("CAM_SET_MAZE", "Cam_set_maze", "Unused. Set to use Camera_Parallel2(), which is only Camera_Noop() MAZE"),
    ("CAM_SET_REMOTEBOMB", "Cam_set_remotebomb", "Unused. Set to use Camera_Parallel2(), which is only Camera_Noop(). But also related to Play_ChangeCameraSetting? REMOTEBOMB"),
    ("CAM_SET_CIRCLE1", "Cam_set_circle1", "Unknown CIRCLE1"),
    ("CAM_SET_CIRCLE2", "Cam_set_circle2", "Looking at far-away NPCs eg. Garo in Road to Ikana, Hungry Goron, Tingle CIRCLE2"),
    ("CAM_SET_CIRCLE3", "Cam_set_circle3", "Used in curiosity shop, goron racetrack, final room in Sakon's hideout, other places CIRCLE3"),
    ("CAM_SET_CIRCLE4", "Cam_set_circle4", "Used during the races on the doggy racetrack CIRCLE4"),
    ("CAM_SET_FIXED3", "Cam_set_fixed3", "Used in Stock Pot Inn Toilet and Tatl cutscene after woodfall FIXED3"),
    ("CAM_SET_TOWER_ASCENT", "Cam_set_tower_ascent", "Various climbing structures (Snowhead climb to the temple entrance) TOWER0"),
    ("CAM_SET_PARALLEL0", "Cam_set_parallel0", "Unknown PARALLEL0"),
    ("CAM_SET_NORMALD", "Cam_set_normald", "Unknown, set with camDataId = -20 NORMALD"),
    ("CAM_SET_SUBJECTD", "Cam_set_subjectd", "Unknown, set with camDataId = -21 SUBJECTD"),
    ("CAM_SET_START0", "Cam_set_start0", "Entering a room, either Dawn of a New Day reload, or entering a door where the camera is fixed on the other end START0"),
    ("CAM_SET_START2", "Cam_set_start2", "Entering a scene, camera is put at a low angle eg. Grottos, Deku Palace, Stock Pot Inn START2"),
    ("CAM_SET_STOP0", "Cam_set_stop0", "Called in z_play STOP0"),
    ("CAM_SET_BOAT_CRUISE", "Cam_set_boat_cruise", "Koume's boat cruise JCRUISING"),
    ("CAM_SET_VERTICAL_CLIMB", "Cam_set_vertical_climb", "Large vertical climbs, such as Mountain Village wall or Pirates Fortress ladder. CLIMBMAZE"),
    ("CAM_SET_SIDED", "Cam_set_sided", "Unknown, set with camDataId = -24 SIDED"),
    ("CAM_SET_DUNGEON2", "Cam_set_dungeon2", "Generic dungeon camera 2, used in various places DUNGEON2"),
    ("CAM_SET_BOSS_ODOLWA", "Cam_set_boss_odolwa", "Odolwa's Lair, also used in GBT entrance: BOSS_SHIGE"),
    ("CAM_SET_KEEPBACK", "Cam_set_keepback", "Unknown. Possibly related to climbing something? KEEPBACK"),
    ("CAM_SET_CIRCLE6", "Cam_set_circle6", "Used in select regions from Ikana CIRCLE6"),
    ("CAM_SET_CIRCLE7", "Cam_set_circle7", "Unknown CIRCLE7"),
    ("CAM_SET_MINI_BOSS", "Cam_set_mini_boss", "Used during the various minibosses of the CHUBOSS"),
    ("CAM_SET_RFIXED1", "Cam_set_rfixed1", "Talking to Koume stuck on the floor in woods of mystery RFIXED1"),
    ("CAM_SET_TREASURE_CHEST_MINIGAME", "Cam_set_treasure_chest_minigame", "Treasure Chest Shop in East Clock Town, minigame location TRESURE1"),
    ("CAM_SET_HONEY_AND_DARLING_1", "Cam_set_honey_and_darling_1", "Honey and Darling Minigames BOMBBASKET"),
    ("CAM_SET_CIRCLE8", "Cam_set_circle8", "Used by Stone Tower moving platforms, Falling eggs in Marine Lab, Bugs into soilpatch cutscene CIRCLE8"),
    ("CAM_SET_BIRDS_EYE_VIEW_1", "Cam_set_birds_eye_view_1", "Camera is a top-down view. Used in Fisherman's minigame and Deku Palace FUKAN1"),
    ("CAM_SET_DUNGEON3", "Cam_set_dungeon3", "Generic dungeon camera 3, used in various places DUNGEON3"),
    ("CAM_SET_TELESCOPE", "Cam_set_telescope", "Observatory telescope and Curiosity Shop Peep-Hole TELESCOPE"),
    ("CAM_SET_ROOM0", "Cam_set_room0", "Certain rooms eg. inside the clock tower ROOM0"),
    ("CAM_SET_RCIRC0", "Cam_set_rcirc0", "Used by a few NPC cutscenes, focus close on the NPC RCIRC0"),
    ("CAM_SET_CIRCLE9", "Cam_set_circle9", "Used by Sakon Hideout entrance and Deku Palace Maze CIRCLE9"),
    ("CAM_SET_ONTHEPOLE", "Cam_set_onthepole", "Somewhere in Snowhead Temple and Woodfall Temple ONTHEPOLE"),
    ("CAM_SET_INBUSH", "Cam_set_inbush", "Various bush environments eg. grottos, Swamp Spider House, Termina Field grass bushes, Deku Palace near bean INBUSH"),
    ("CAM_SET_BOSS_MAJORA", "Cam_set_boss_majora", "Majora's Lair: BOSS_LAST "),
    ("CAM_SET_BOSS_TWINMOLD", "Cam_set_boss_twinmold", "Twinmold's Lair: BOSS_INI"),
    ("CAM_SET_BOSS_GOHT", "Cam_set_boss_goht", "Goht's Lair: BOSS_HAK "),
    ("CAM_SET_BOSS_GYORG", "Cam_set_boss_gyorg", "Gyorg's Lair: BOSS_KON"),
    ("CAM_SET_CONNECT0", "Cam_set_connect0", "Smoothly and gradually return camera to Player after a cutscene CONNECT0"),
    ("CAM_SET_PINNACLE_ROCK", "Cam_set_pinnacle_rock", "Pinnacle Rock pit MORAY"),
    ("CAM_SET_NORMAL2", "Cam_set_normal2", "Generic camera 2, used in various places NORMAL2"),
    ("CAM_SET_HONEY_AND_DARLING_2", "Cam_set_honey_and_darling_2", "BOMBBOWL"),
    ("CAM_SET_CIRCLEA", "Cam_set_circlea", "Unknown, Circle 10 CIRCLEA"),
    ("CAM_SET_WHIRLPOOL", "Cam_set_whirlpool", "Great Bay Temple Central Room Whirlpool WHIRLPOOL"),
    ("CAM_SET_CUCCO_SHACK", "Cam_set_cucco_shack", "KOKKOGAME"),
    ("CAM_SET_GIANT", "Cam_set_giant", "Giants Mask in Twinmold's Lair GIANT"),
    ("CAM_SET_SCENE0", "Cam_set_scene0", "Entering doors to a new scene SCENE0"),
    ("CAM_SET_ROOM1", "Cam_set_room1", "Certain rooms eg. some rooms in Stock Pot Inn ROOM1"),
    ("CAM_SET_WATER2", "Cam_set_water2", "Swimming as Zora in Great Bay Temple WATER2"),
    ("CAM_SET_WOODFALL_SWAMP", "Cam_set_woodfall_swamp", "Woodfall inside the swamp, but not on the platforms, SOKONASI"),
    ("CAM_SET_FORCEKEEP", "Cam_set_forcekeep", "Unknown FORCEKEEP"),
    ("CAM_SET_PARALLEL1", "Cam_set_parallel1", "Unknown PARALLEL1"),
    ("CAM_SET_START1", "Cam_set_start1", "Used when entering the lens cave START1"),
    ("CAM_SET_ROOM2", "Cam_set_room2", "Certain rooms eg. Deku King's Chamber, Ocean Spider House ROOM2"),
    ("CAM_SET_NORMAL4", "Cam_set_normal4", "Generic camera 4, used in Ikana Graveyard NORMAL4"),
    ("CAM_SET_ELEGY_SHELL", "Cam_set_elegy_shell", "cutscene after playing elegy of emptyness and spawning a shell SHELL"),
    ("CAM_SET_DUNGEON4", "Cam_set_dungeon4", "Used in Pirates Fortress Interior, hidden room near hookshot DUNGEON4"),
]

decomp_compat_map_CameraSType = {
    "CAM_SET_HORSE0": "CAM_SET_HORSE",
    "CAM_SET_BOSS_GOMA": "CAM_SET_BOSS_GOHMA",
    "CAM_SET_BOSS_DODO": "CAM_SET_BOSS_DODONGO",
    "CAM_SET_BOSS_BARI": "CAM_SET_BOSS_BARINADE",
    "CAM_SET_BOSS_FGANON": "CAM_SET_BOSS_PHANTOM_GANON",
    "CAM_SET_BOSS_BAL": "CAM_SET_BOSS_VOLVAGIA",
    "CAM_SET_BOSS_SHADES": "CAM_SET_BOSS_BONGO",
    "CAM_SET_BOSS_MOFA": "CAM_SET_BOSS_MORPHA",
    "CAM_SET_TWIN0": "CAM_SET_BOSS_TWINROVA_PLATFORM",
    "CAM_SET_TWIN1": "CAM_SET_BOSS_TWINROVA_FLOOR",
    "CAM_SET_BOSS_GANON1": "CAM_SET_BOSS_GANONDORF",
    "CAM_SET_BOSS_GANON2": "CAM_SET_BOSS_GANON",
    "CAM_SET_TOWER0": "CAM_SET_TOWER_CLIMB",
    "CAM_SET_TOWER1": "CAM_SET_TOWER_UNUSED",
    "CAM_SET_FIXED0": "CAM_SET_MARKET_BALCONY",
    "CAM_SET_FIXED1": "CAM_SET_CHU_BOWLING",
    "CAM_SET_CIRCLE0": "CAM_SET_PIVOT_CRAWLSPACE",
    "CAM_SET_CIRCLE2": "CAM_SET_PIVOT_SHOP_BROWSING",
    "CAM_SET_CIRCLE3": "CAM_SET_PIVOT_IN_FRONT",
    "CAM_SET_PREREND0": "CAM_SET_PREREND_FIXED",
    "CAM_SET_PREREND1": "CAM_SET_PREREND_PIVOT",
    "CAM_SET_PREREND3": "CAM_SET_PREREND_SIDE_SCROLL",
    "CAM_SET_RAIL3": "CAM_SET_CRAWLSPACE",
    "CAM_SET_CIRCLE4": "CAM_SET_PIVOT_CORNER",
    "CAM_SET_CIRCLE5": "CAM_SET_PIVOT_WATER_SURFACE",
    "CAM_SET_DEMO0": "CAM_SET_CS_0",
    "CAM_SET_DEMO1": "CAM_SET_CS_TWISTED_HALLWAY",
    "CAM_SET_MORI1": "CAM_SET_FOREST_BIRDS_EYE",
    "CAM_SET_ITEM0": "CAM_SET_SLOW_CHEST_CS",
    "CAM_SET_ITEM1": "CAM_SET_ITEM_UNUSED",
    "CAM_SET_DEMO3": "CAM_SET_CS_3",
    "CAM_SET_DEMO4": "CAM_SET_CS_ATTENTION",
    "CAM_SET_UFOBEAN": "CAM_SET_BEAN_GENERIC",
    "CAM_SET_LIFTBEAN": "CAM_SET_BEAN_LOST_WOODS",
    "CAM_SET_SCENE0": "CAM_SET_SCENE_UNUSED",
    "CAM_SET_SCENE1": "CAM_SET_SCENE_TRANSITION",
    "CAM_SET_HIDAN1": "CAM_SET_ELEVATOR_PLATFORM",
    "CAM_SET_HIDAN2": "CAM_SET_FIRE_STAIRCASE",
    "CAM_SET_MORI2": "CAM_SET_FOREST_UNUSED",
    "CAM_SET_MORI3": "CAM_SET_FOREST_DEFEAT_POE",
    "CAM_SET_TAKO": "CAM_SET_BIG_OCTO",
    "CAM_SET_SPOT05A": "CAM_SET_MEADOW_BIRDS_EYE",
    "CAM_SET_SPOT05B": "CAM_SET_MEADOW_UNUSED",
    "CAM_SET_HIDAN3": "CAM_SET_FIRE_BIRDS_EYE",
    "CAM_SET_ITEM2": "CAM_SET_TURN_AROUND",
    "CAM_SET_CIRCLE6": "CAM_SET_PIVOT_VERTICAL",
    "CAM_SET_DEMOC": "CAM_SET_CS_C",
    "CAM_SET_UO_FIBER": "CAM_SET_JABU_TENTACLE",
    "CAM_SET_TEPPEN": "CAM_SET_DIRECTED_YAW",
    "CAM_SET_CIRCLE7": "CAM_SET_PIVOT_FROM_SIDE",
}


class MMCollisionVertex:
    def __init__(self, position):
        self.position = position


class MMCollisionPolygon:
    def __init__(self, indices, normal, distance):
        self.indices = indices
        self.normal = normal
        self.distance = distance

    def convertShort02(self, ignoreCamera, ignoreActor, ignoreProjectile):
        vertPart = self.indices[0] & 0x1FFF
        colPart = (1 if ignoreCamera else 0) + (2 if ignoreActor else 0) + (4 if ignoreProjectile else 0)

        return vertPart | (colPart << 13)

    def convertShort04(self, enableConveyor):
        vertPart = self.indices[1] & 0x1FFF
        conveyorPart = 1 if enableConveyor else 0

        return vertPart | (conveyorPart << 13)

    def convertShort06(self):
        return self.indices[2] & 0x1FFF


class MMPolygonType:
    def __eq__(self, other):
        return (
            self.eponaBlock == other.eponaBlock
            and self.decreaseHeight == other.decreaseHeight
            and self.floorSetting == other.floorSetting
            and self.wallSetting == other.wallSetting
            and self.floorProperty == other.floorProperty
            and self.exitID == other.exitID
            and self.cameraID == other.cameraID
            and self.isWallDamage == other.isWallDamage
            and self.enableConveyor == other.enableConveyor
            and self.conveyorRotation == other.conveyorRotation
            and self.conveyorSpeed == other.conveyorSpeed
            and self.hookshotable == other.hookshotable
            and self.echo == other.echo
            and self.lightingSetting == other.lightingSetting
            and self.terrain == other.terrain
            and self.sound == other.sound
            and self.ignoreCameraCollision == other.ignoreCameraCollision
            and self.ignoreActorCollision == other.ignoreActorCollision
            and self.ignoreProjectileCollision == other.ignoreProjectileCollision
        )

    def __ne__(self, other):
        return (
            self.eponaBlock != other.eponaBlock
            or self.decreaseHeight != other.decreaseHeight
            or self.floorSetting != other.floorSetting
            or self.wallSetting != other.wallSetting
            or self.floorProperty != other.floorProperty
            or self.exitID != other.exitID
            or self.cameraID != other.cameraID
            or self.isWallDamage != other.isWallDamage
            or self.enableConveyor != other.enableConveyor
            or self.conveyorRotation != other.conveyorRotation
            or self.conveyorSpeed != other.conveyorSpeed
            or self.hookshotable != other.hookshotable
            or self.echo != other.echo
            or self.lightingSetting != other.lightingSetting
            or self.terrain != other.terrain
            or self.sound != other.sound
            or self.ignoreCameraCollision != other.ignoreCameraCollision
            or self.ignoreActorCollision != other.ignoreActorCollision
            or self.ignoreProjectileCollision != other.ignoreProjectileCollision
        )

    def __hash__(self):
        return hash(
            (
                self.eponaBlock,
                self.decreaseHeight,
                self.floorSetting,
                self.wallSetting,
                self.floorProperty,
                self.exitID,
                self.cameraID,
                self.isWallDamage,
                self.enableConveyor,
                self.conveyorRotation,
                self.conveyorSpeed,
                self.hookshotable,
                self.echo,
                self.lightingSetting,
                self.terrain,
                self.sound,
                self.ignoreCameraCollision,
                self.ignoreActorCollision,
                self.ignoreProjectileCollision,
            )
        )

    def __init__(self):
        self.eponaBlock = None  # eponaBlock
        self.decreaseHeight = None  # decreaseHeight
        self.floorSetting = None  # floorSetting
        self.wallSetting = None  # wallSetting
        self.floorProperty = None  # floorProperty
        self.exitID = None  # exitID
        self.cameraID = None  # cameraID
        self.isWallDamage = None  # isWallDamage
        self.enableConveyor = None
        self.conveyorRotation = None  # conveyorDirection
        self.conveyorSpeed = None  # conveyorSpeed
        self.hookshotable = None  # hookshotable
        self.echo = None  # echo
        self.lightingSetting = None  # lightingSetting
        self.terrain = None  # terrain
        self.sound = None  # sound
        self.ignoreCameraCollision = None
        self.ignoreActorCollision = None
        self.ignoreProjectileCollision = None

    def convertHigh(self):
        value = (
            ((1 if self.eponaBlock else 0) << 31)
            | ((1 if self.decreaseHeight else 0) << 30)
            | (int(self.floorSetting, 16) << 26)
            | (int(self.wallSetting, 16) << 21)
            | (int(self.floorProperty, 16) << 13)
            | (self.exitID << 8)
            | (self.cameraID << 0)
        )

        return convertIntTo2sComplement(value, 4, False)

    def convertLow(self):
        value = (
            ((1 if self.isWallDamage else 0) << 27)
            | (self.conveyorRotation << 21)
            | (self.conveyorSpeed << 18)
            | ((1 if self.hookshotable else 0) << 17)
            | (int(self.echo, 16) << 11)
            | (self.lightingSetting << 6)
            | (int(self.terrain, 16) << 4)
            | (int(self.sound, 16) << 0)
        )

        return convertIntTo2sComplement(value, 4, False)


class MMCollision:
    def __init__(self, ownerName):
        self.ownerName = ownerName
        self.bounds = []
        self.vertices = []
        # dict of polygon type : polygon list
        self.polygonGroups = {}
        self.cameraData = None
        self.waterBoxes = []

    def polygonCount(self):
        count = 0
        for polygonType, polygons in self.polygonGroups.items():
            count += len(polygons)
        return count

    def headerName(self):
        return self.ownerName + "_collisionHeader"

    def verticesName(self):
        return self.ownerName + "_vertices"

    def polygonsName(self):
        return self.ownerName + "_polygons"

    def polygonTypesName(self):
        return self.ownerName + "_polygonTypes"

    def camDataName(self):
        return self.ownerName + "_camData"

    def waterBoxesName(self):
        return self.ownerName + "_waterBoxes"


def getPolygonType(collisionProp):
    polygonType = MMPolygonType()
    polygonType.ignoreCameraCollision = collisionProp.ignoreCameraCollision
    polygonType.ignoreActorCollision = collisionProp.ignoreActorCollision
    polygonType.ignoreProjectileCollision = collisionProp.ignoreProjectileCollision
    polygonType.eponaBlock = collisionProp.eponaBlock
    polygonType.decreaseHeight = collisionProp.decreaseHeight
    polygonType.floorSetting = getCustomProperty(collisionProp, "floorSetting")
    polygonType.wallSetting = getCustomProperty(collisionProp, "wallSetting")
    polygonType.floorProperty = getCustomProperty(collisionProp, "floorProperty")
    polygonType.exitID = collisionProp.exitID
    polygonType.cameraID = collisionProp.cameraID
    polygonType.isWallDamage = collisionProp.isWallDamage
    polygonType.enableConveyor = collisionProp.conveyorOption == "Land"
    if collisionProp.conveyorOption != "None":
        polygonType.conveyorRotation = int(collisionProp.conveyorRotation / (2 * math.pi) * 0x3F)
        polygonType.conveyorSpeed = int(getCustomProperty(collisionProp, "conveyorSpeed"), 16) + (
            4 if collisionProp.conveyorKeepMomentum else 0
        )
    else:
        polygonType.conveyorRotation = 0
        polygonType.conveyorSpeed = 0

    polygonType.hookshotable = collisionProp.hookshotable
    polygonType.echo = collisionProp.echo
    polygonType.lightingSetting = collisionProp.lightingSetting
    polygonType.terrain = getCustomProperty(collisionProp, "terrain")
    polygonType.sound = getCustomProperty(collisionProp, "sound")
    return polygonType


class MMWaterBox(BoxEmpty):
    def __init__(self, roomIndex, lightingSetting, cameraSetting, flag19, position, scale, emptyScale):
        self.roomIndex = roomIndex
        self.lightingSetting = lightingSetting
        self.cameraSetting = cameraSetting
        self.flag19 = flag19
        BoxEmpty.__init__(self, position, scale, emptyScale)

    def propertyData(self):
        value = (
            ((1 if self.flag19 else 0) << 19)
            | (int(self.roomIndex) << 13)
            | (self.lightingSetting << 8)
            | (self.cameraSetting << 0)
        )
        return convertIntTo2sComplement(value, 4, False)


class MMCameraData:
    def __init__(self, ownerName):
        self.ownerName = ownerName
        self.camPosDict = {}

    def camDataName(self):
        return self.ownerName + "_camData"

    def camPositionsName(self):
        return self.ownerName + "_camPosData"

    def validateCamPositions(self):
        count = 0
        while count < len(self.camPosDict):
            if count not in self.camPosDict:
                raise PluginError(
                    "Error: Camera positions do not have a consecutive list of indices.\n"
                    + "Missing index: "
                    + str(count)
                )
            count = count + 1


class MMCameraPosData:
    def __init__(self, camSType, hasPositionData, position, rotation, fov, bgImageOverrideIndex):
        self.camSType = camSType
        self.position = position
        self.rotation = rotation
        self.fov = fov
        self.bgImageOverrideIndex = bgImageOverrideIndex
        self.unknown = -1
        self.hasPositionData = hasPositionData


class MMCrawlspaceData:
    def __init__(self, camSType):
        self.camSType = camSType
        self.points = []
