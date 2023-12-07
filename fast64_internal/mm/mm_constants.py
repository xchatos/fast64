from .data import Mm_Data

mmData = Mm_Data()

mmEnumRoomShapeType = [
    # ("Custom", "Custom", "Custom"),
    ("ROOM_SHAPE_TYPE_NORMAL", "Normal", "Normal"),
    ("ROOM_SHAPE_TYPE_IMAGE", "Image", "Image"),
    ("ROOM_SHAPE_TYPE_CULLABLE", "Cullable", "Cullable"),
]

mmRoomShapeStructs = [
    "RoomShapeNormal",
    "RoomShapeImage",
    "RoomShapeCullable",
]

mmRoomShapeEntryStructs = [
    "RoomShapeDListsEntry",
    "RoomShapeDListsEntry",
    "RoomShapeCullableEntry",
]


mmEnumSceneMenu = [
    ("General", "General", "General"),
    ("Lighting", "Lighting", "Lighting"),
    ("Cutscene", "Cutscene", "Cutscene"),
    ("Exits", "Exits", "Exits"),
    ("Alternate", "Alternate", "Alternate"),
]

mmEnumRenderScene = [
    ("General", "General", "General"),
    ("Alternate", "Alternate", "Alternate"),
]

mmEnumSceneMenuAlternate = [
    ("General", "General", "General"),
    ("Lighting", "Lighting", "Lighting"),
    ("Cutscene", "Cutscene", "Cutscene"),
    ("Exits", "Exits", "Exits"),
]

mmEnumRoomMenu = [
    ("General", "General", "General"),
    ("Objects", "Objects", "Objects"),
    ("Alternate", "Alternate", "Alternate"),
]

mmEnumRoomMenuAlternate = [
    ("General", "General", "General"),
    ("Objects", "Objects", "Objects"),
]

mmEnumHeaderMenu = [
    ("Child Night", "Child Night", "Child Night"),
    ("Adult Day", "Adult Day", "Adult Day"),
    ("Adult Night", "Adult Night", "Adult Night"),
    ("Cutscene", "Cutscene", "Cutscene"),
]

mmEnumHeaderMenuComplete = [
    ("Child Day", "Child Day", "Child Day"),
    ("Child Night", "Child Night", "Child Night"),
    ("Adult Day", "Adult Day", "Adult Day"),
    ("Adult Night", "Adult Night", "Adult Night"),
    ("Cutscene", "Cutscene", "Cutscene"),
]

mmEnumLightGroupMenu = [
    ("Dawn", "Dawn", "Dawn"),
    ("Day", "Day", "Day"),
    ("Dusk", "Dusk", "Dusk"),
    ("Night", "Night", "Night"),
]

mmEnumLinkIdle = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "Sneezing", "Sneezing"),
    ("0x02", "Wiping Forehead", "Wiping Forehead"),
    ("0x04", "Yawning", "Yawning"),
    ("0x07", "Gasping For Breath", "Gasping For Breath"),
    ("0x09", "Brandish Sword", "Brandish Sword"),
    ("0x0A", "Adjust Tunic", "Adjust Tunic"),
    ("0xFF", "Hops On Epona", "Hops On Epona"),
]

# Make sure to add exceptions in utility.py - selectMeshChildrenOnly
mmEnumEmptyType = [
    ("None", "None", "None"),
    ("Scene", "Scene", "Scene"),
    ("Room", "Room", "Room"),
    ("Actor", "Actor", "Actor"),
    ("Transition Actor", "Transition Actor", "Transition Actor"),
    ("Entrance", "Entrance", "Entrance"),
    ("Water Box", "Water Box", "Water Box"),
    ("Cull Group", "Custom Cull Group", "Cull Group"),
    ("LOD", "LOD Group", "LOD Group"),
    ("Cutscene", "Cutscene Main", "Cutscene"),
    ("CS Actor Cue List", "CS Actor Cue List", "CS Actor Cue List"),
    ("CS Actor Cue", "CS Actor Cue", "CS Actor Cue"),
    ("CS Player Cue List", "CS Player Cue List", "CS Player Cue List"),
    ("CS Player Cue", "CS Player Cue", "CS Player Cue"),
    ("CS Actor Cue Preview", "CS Actor Cue Preview", "CS Actor Cue Preview"),
    ("CS Player Cue Preview", "CS Player Cue Preview", "CS Player Cue Preview"),
    ("CS Dummy Cue", "CS Dummy Cue", "CS Dummy Cue"),
    # ('Camera Volume', 'Camera Volume', 'Camera Volume'),
]

mmEnumCloudiness = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Sunny", "Sunny"),
    ("0x01", "Cloudy", "Cloudy"),
]

mmEnumCameraMode = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x10", "Two Views, No C-Up", "Two Views, No C-Up"),
    ("0x20", "Rotating Background, Bird's Eye C-Up", "Rotating Background, Bird's Eye C-Up"),
    ("0x30", "Fixed Background, No C-Up", "Fixed Background, No C-Up"),
    ("0x40", "Rotating Background, No C-Up", "Rotating Background, No C-Up"),
    ("0x50", "Shooting Gallery", "Shooting Gallery"),
]

mmEnumMapLocation = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Hyrule Field", "Hyrule Field"),
    ("0x01", "Kakariko Village", "Kakariko Village"),
    ("0x02", "Graveyard", "Graveyard"),
    ("0x03", "Zora's River", "Zora's River"),
    ("0x04", "Kokiri Forest", "Kokiri Forest"),
    ("0x05", "Sacred Forest Meadow", "Sacred Forest Meadow"),
    ("0x06", "Lake Hylia", "Lake Hylia"),
    ("0x07", "Zora's Domain", "Zora's Domain"),
    ("0x08", "Zora's Fountain", "Zora's Fountain"),
    ("0x09", "Gerudo Valley", "Gerudo Valley"),
    ("0x0A", "Lost Woods", "Lost Woods"),
    ("0x0B", "Desert Colossus", "Desert Colossus"),
    ("0x0C", "Gerudo's Fortress", "Gerudo's Fortress"),
    ("0x0D", "Haunted Wasteland", "Haunted Wasteland"),
    ("0x0E", "Market", "Market"),
    ("0x0F", "Hyrule Castle", "Hyrule Castle"),
    ("0x10", "Death Mountain Trail", "Death Mountain Trail"),
    ("0x11", "Death Mountain Crater", "Death Mountain Crater"),
    ("0x12", "Goron City", "Goron City"),
    ("0x13", "Lon Lon Ranch", "Lon Lon Ranch"),
    ("0x14", "Dampe's Grave & Windmill", "Dampe's Grave & Windmill"),
    ("0x15", "Ganon's Castle", "Ganon's Castle"),
    ("0x16", "Grottos & Fairy Fountains", "Grottos & Fairy Fountains"),
]

mmEnumSkybox = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Standard Sky", "Standard Sky"),
    ("0x02", "Hylian Bazaar", "Hylian Bazaar"),
    ("0x03", "Brown Cloudy Sky", "Brown Cloudy Sky"),
    ("0x04", "Market Ruins", "Market Ruins"),
    ("0x05", "Black Cloudy Night", "Black Cloudy Night"),
    ("0x07", "Link's House", "Link's House"),
    ("0x09", "Market (Main Square, Day)", "Market (Main Square, Day)"),
    ("0x0A", "Market (Main Square, Night)", "Market (Main Square, Night)"),
    ("0x0B", "Happy Mask Shop", "Happy Mask Shop"),
    ("0x0C", "Know-It-All Brothers' House", "Know-It-All Brothers' House"),
    ("0x0E", "Kokiri Twins' House", "Kokiri Twins' House"),
    ("0x0F", "Stable", "Stable"),
    ("0x10", "Stew Lady's House", "Stew Lady's House"),
    ("0x11", "Kokiri Shop", "Kokiri Shop"),
    ("0x13", "Goron Shop", "Goron Shop"),
    ("0x14", "Zora Shop", "Zora Shop"),
    ("0x16", "Kakariko Potions Shop", "Kakariko Potions Shop"),
    ("0x17", "Hylian Potions Shop", "Hylian Potions Shop"),
    ("0x18", "Bomb Shop", "Bomb Shop"),
    ("0x1A", "Dog Lady's House", "Dog Lady's House"),
    ("0x1B", "Impa's House", "Impa's House"),
    ("0x1C", "Gerudo Tent", "Gerudo Tent"),
    ("0x1D", "Environment Color", "Environment Color"),
    ("0x20", "Mido's House", "Mido's House"),
    ("0x21", "Saria's House", "Saria's House"),
    ("0x22", "Dog Guy's House", "Dog Guy's House"),
]

mmEnumSkyboxLighting = [
    # see ``LightMode`` enum in ``z64environment.h``
    ("Custom", "Custom", "Custom"),
    ("LIGHT_MODE_TIME", "Time Of Day", "Time Of Day"),
    ("LIGHT_MODE_SETTINGS", "Indoor", "Indoor"),
]

mmEnumAudioSessionPreset = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "0x00", "0x00"),
]

mmEnumMusicSeq = [
    ("Custom", "Custom", "Custom"),
    ("0x02", "Hyrule Field", "Hyrule Field"),
    ("0x03", "Hyrule Field (Initial Segment From Loading Area)", "Hyrule Field (Initial Segment From Loading Area)"),
    ("0x04", "Hyrule Field (Moving Segment 1)", "Hyrule Field (Moving Segment 1)"),
    ("0x05", "Hyrule Field (Moving Segment 2)", "Hyrule Field (Moving Segment 2)"),
    ("0x06", "Hyrule Field (Moving Segment 3)", "Hyrule Field (Moving Segment 3)"),
    ("0x07", "Hyrule Field (Moving Segment 4)", "Hyrule Field (Moving Segment 4)"),
    ("0x08", "Hyrule Field (Moving Segment 5)", "Hyrule Field (Moving Segment 5)"),
    ("0x09", "Hyrule Field (Moving Segment 6)", "Hyrule Field (Moving Segment 6)"),
    ("0x0A", "Hyrule Field (Moving Segment 7)", "Hyrule Field (Moving Segment 7)"),
    ("0x0B", "Hyrule Field (Moving Segment 8)", "Hyrule Field (Moving Segment 8)"),
    ("0x0C", "Hyrule Field (Moving Segment 9)", "Hyrule Field (Moving Segment 9)"),
    ("0x0D", "Hyrule Field (Moving Segment 10)", "Hyrule Field (Moving Segment 10)"),
    ("0x0E", "Hyrule Field (Moving Segment 11)", "Hyrule Field (Moving Segment 11)"),
    ("0x0F", "Hyrule Field (Enemy Approaches)", "Hyrule Field (Enemy Approaches)"),
    ("0x10", "Hyrule Field (Enemy Near Segment 1)", "Hyrule Field (Enemy Near Segment 1)"),
    ("0x11", "Hyrule Field (Enemy Near Segment 2)", "Hyrule Field (Enemy Near Segment 2)"),
    ("0x12", "Hyrule Field (Enemy Near Segment 3)", "Hyrule Field (Enemy Near Segment 3)"),
    ("0x13", "Hyrule Field (Enemy Near Segment 4)", "Hyrule Field (Enemy Near Segment 4)"),
    ("0x14", "Hyrule Field (Standing Still Segment 1)", "Hyrule Field (Standing Still Segment 1)"),
    ("0x15", "Hyrule Field (Standing Still Segment 2)", "Hyrule Field (Standing Still Segment 2)"),
    ("0x16", "Hyrule Field (Standing Still Segment 3)", "Hyrule Field (Standing Still Segment 3)"),
    ("0x17", "Hyrule Field (Standing Still Segment 4)", "Hyrule Field (Standing Still Segment 4)"),
    ("0x18", "Dodongo's Cavern", "Dodongo's Cavern"),
    ("0x19", "Kakariko Village (Adult)", "Kakariko Village (Adult)"),
    ("0x1A", "Enemy Battle", "Enemy Battle"),
    ("0x1B", "Boss Battle 00", "Boss Battle 00"),
    ("0x1C", "Inside the Deku Tree", "Inside the Deku Tree"),
    ("0x1D", "Market", "Market"),
    ("0x1E", "Title Theme", "Title Theme"),
    ("0x1F", "Link's House", "Link's House"),
    ("0x20", "Game Over", "Game Over"),
    ("0x21", "Boss Clear", "Boss Clear"),
    ("0x22", "Item Get", "Item Get"),
    ("0x23", "Opening Ganon", "Opening Ganon"),
    ("0x24", "Heart Get", "Heart Get"),
    ("0x25", "Prelude Of Light", "Prelude Of Light"),
    ("0x26", "Inside Jabu-Jabu's Belly", "Inside Jabu-Jabu's Belly"),
    ("0x27", "Kakariko Village (Child)", "Kakariko Village (Child)"),
    ("0x28", "Great Fairy's Fountain", "Great Fairy's Fountain"),
    ("0x29", "Zelda's Theme", "Zelda's Theme"),
    ("0x2A", "Fire Temple", "Fire Temple"),
    ("0x2B", "Open Treasure Chest", "Open Treasure Chest"),
    ("0x2C", "Forest Temple", "Forest Temple"),
    ("0x2D", "Hyrule Castle Courtyard", "Hyrule Castle Courtyard"),
    ("0x2E", "Ganondorf's Theme", "Ganondorf's Theme"),
    ("0x2F", "Lon Lon Ranch", "Lon Lon Ranch"),
    ("0x30", "Goron City", "Goron City "),
    ("0x31", "Hyrule Field Morning Theme", "Hyrule Field Morning Theme"),
    ("0x32", "Spiritual Stone Get", "Spiritual Stone Get"),
    ("0x33", "Bolero of Fire", "Bolero of Fire"),
    ("0x34", "Minuet of Woods", "Minuet of Woods"),
    ("0x35", "Serenade of Water", "Serenade of Water"),
    ("0x36", "Requiem of Spirit", "Requiem of Spirit"),
    ("0x37", "Nocturne of Shadow", "Nocturne of Shadow"),
    ("0x38", "Mini-Boss Battle", "Mini-Boss Battle"),
    ("0x39", "Obtain Small Item", "Obtain Small Item"),
    ("0x3A", "Temple of Time", "Temple of Time"),
    ("0x3B", "Escape from Lon Lon Ranch", "Escape from Lon Lon Ranch"),
    ("0x3C", "Kokiri Forest", "Kokiri Forest"),
    ("0x3D", "Obtain Fairy Ocarina", "Obtain Fairy Ocarina"),
    ("0x3E", "Lost Woods", "Lost Woods"),
    ("0x3F", "Spirit Temple", "Spirit Temple"),
    ("0x40", "Horse Race", "Horse Race"),
    ("0x41", "Horse Race Goal", "Horse Race Goal"),
    ("0x42", "Ingo's Theme", "Ingo's Theme"),
    ("0x43", "Obtain Medallion", "Obtain Medallion"),
    ("0x44", "Ocarina Saria's Song", "Ocarina Saria's Song"),
    ("0x45", "Ocarina Epona's Song", "Ocarina Epona's Song"),
    ("0x46", "Ocarina Zelda's Lullaby", "Ocarina Zelda's Lullaby"),
    ("0x47", "Sun's Song", "Sun's Song"),
    ("0x48", "Song of Time", "Song of Time"),
    ("0x49", "Song of Storms", "Song of Storms"),
    ("0x4A", "Fairy Flying", "Fairy Flying"),
    ("0x4B", "Deku Tree", "Deku Tree"),
    ("0x4C", "Windmill Hut", "Windmill Hut"),
    ("0x4D", "Legend of Hyrule", "Legend of Hyrule"),
    ("0x4E", "Shooting Gallery", "Shooting Gallery"),
    ("0x4F", "Sheik's Theme", "Sheik's Theme"),
    ("0x50", "Zora's Domain", "Zora's Domain"),
    ("0x51", "Enter Zelda", "Enter Zelda"),
    ("0x52", "Goodbye to Zelda", "Goodbye to Zelda"),
    ("0x53", "Master Sword", "Master Sword"),
    ("0x54", "Ganon Intro", "Ganon Intro"),
    ("0x55", "Shop", "Shop"),
    ("0x56", "Chamber of the Sages", "Chamber of the Sages"),
    ("0x57", "File Select", "File Select"),
    ("0x58", "Ice Cavern", "Ice Cavern"),
    ("0x59", "Open Door of Temple of Time", "Open Door of Temple of Time"),
    ("0x5A", "Kaepora Gaebora's Theme", "Kaepora Gaebora's Theme"),
    ("0x5B", "Shadow Temple", "Shadow Temple"),
    ("0x5C", "Water Temple", "Water Temple"),
    ("0x5D", "Ganon's Castle Bridge", "Ganon's Castle Bridge"),
    ("0x5E", "Ocarina of Time", "Ocarina of Time"),
    ("0x5F", "Gerudo Valley", "Gerudo Valley"),
    ("0x60", "Potion Shop", "Potion Shop"),
    ("0x61", "Kotake & Koume's Theme", "Kotake & Koume's Theme"),
    ("0x62", "Escape from Ganon's Castle", "Escape from Ganon's Castle"),
    ("0x63", "Ganon's Castle Under Ground", "Ganon's Castle Under Ground"),
    ("0x64", "Ganondorf Battle", "Ganondorf Battle"),
    ("0x65", "Ganon Battle", "Ganon Battle"),
    ("0x66", "Seal of Six Sages", "Seal of Six Sages"),
    ("0x67", "End Credits I", "End Credits I"),
    ("0x68", "End Credits II", "End Credits II"),
    ("0x69", "End Credits III", "End Credits III"),
    ("0x6A", "End Credits IV", "End Credits IV"),
    ("0x6B", "King Dodongo & Volvagia Boss Battle", "King Dodongo & Volvagia Boss Battle"),
    ("0x6C", "Mini-Game", "Mini-Game"),
]

mmEnumNightSeq = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Standard night [day and night cycle]", "0x00"),
    ("0x01", "Standard night [Kakariko]", "0x01"),
    ("0x02", "Distant storm [Graveyard]", "0x02"),
    ("0x03", "Howling wind and cawing [Ganon's Castle]", "0x03"),
    ("0x04", "Wind + night birds [Kokiri]", "0x04"),
    ("0x05", "Wind + crickets", "0x05"),
    ("0x06", "Wind", "0x06"),
    ("0x07", "Howling wind", "0x07"),
    ("0x08", "Wind + crickets", "0x08"),
    ("0x09", "Wind + crickets", "0x09"),
    ("0x0A", "Tubed howling wind [Wasteland]", "0x0A"),
    ("0x0B", "Tubed howling wind [Colossus]", "0x0B"),
    ("0x0C", "Wind", "0x0C"),
    ("0x0D", "Wind + crickets", "0x0D"),
    ("0x0E", "Wind + crickets", "0x0E"),
    ("0x0F", "Wind + birds", "0x0F"),
    ("0x10", "Wind + crickets", "0x10"),
    ("0x11", "?", "0x11"),
    ("0x12", "Wind + crickets", "0x12"),
    ("0x13", "Day music always playing", "0x13"),
    ("0x14", "Silence", "0x14"),
    ("0x16", "Silence", "0x16"),
    ("0x17", "High tubed wind + rain", "0x17"),
    ("0x18", "Silence", "0x18"),
    ("0x19", "Silence", "0x19"),
    ("0x1A", "High tubed wind + rain", "0x1A"),
    ("0x1B", "Silence", "0x1B"),
    ("0x1C", "Rain", "0x1C"),
    ("0x1D", "High tubed wind + rain", "0x1D"),
    ("0x1E", "Silence", "0x1E"),
    ("0x1F", "High tubed wind + rain ", "0x1F"),
]

mmEnumGlobalObject = [
    ("Custom", "Custom", "Custom"),
    ("OBJECT_INVALID", "None", "None"),
    ("OBJECT_GAMEPLAY_FIELD_KEEP", "Overworld", "gameplay_field_keep"),
    ("OBJECT_GAMEPLAY_DANGEON_KEEP", "Dungeon", "gameplay_dangeon_keep"),
]

mmEnumNaviHints = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "None", "None"),
    ("0x01", "Overworld", "elf_message_field"),
    ("0x02", "Dungeon", "elf_message_ydan"),
]

mmEnumTransitionAnims = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Spiky", "Spiky"),
    ("0x01", "Triforce", "Triforce"),
    ("0x02", "Slow Black Fade", "Slow Black Fade"),
    ("0x03", "Slow Day/White, Slow Night/Black Fade", "Slow Day/White, Slow Night/Black Fade"),
    ("0x04", "Fast Day/Black, Slow Night/Black Fade", "Fast Day/Black, Slow Night/Black Fade"),
    ("0x05", "Fast Day/White, Slow Night/Black Fade", "Fast Day/White, Slow Night/Black Fade"),
    ("0x06", "Very Slow Day/White, Slow Night/Black Fade", "Very Slow Day/White, Slow Night/Black Fade"),
    ("0x07", "Very Slow Day/White, Slow Night/Black Fade", "Very Slow Day/White, Slow Night/Black Fade"),
    ("0x0E", "Slow Sandstorm Fade", "Slow Sandstorm Fade"),
    ("0x0F", "Fast Sandstorm Fade", "Fast Sandstorm Fade"),
    ("0x20", "Iris Fade", "Iris Fade"),
    ("0x2C", "Shortcut Transition", "Shortcut Transition"),
]

# The order of this list matters (normal Mm scene order as defined by ``scene_table.h``)
mmEnumSceneID = [
    ("Custom", "Custom", "Custom"),
    ("SCENE_DEKU_TREE", "Inside the Deku Tree (Ydan)", "Ydan"),
    ("SCENE_DODONGOS_CAVERN", "Dodongo's Cavern (Ddan)", "Ddan"),
    ("SCENE_JABU_JABU", "Inside Jabu Jabu's Belly (Bdan)", "Bdan"),
    ("SCENE_FOREST_TEMPLE", "Forest Temple (Bmori1)", "Bmori1"),
    ("SCENE_FIRE_TEMPLE", "Fire Temple (Hidan)", "Hidan"),
    ("SCENE_WATER_TEMPLE", "Water Temple (Mizusin)", "Mizusin"),
    ("SCENE_SPIRIT_TEMPLE", "Spirit Temple (Jyasinzou)", "Jyasinzou"),
    ("SCENE_SHADOW_TEMPLE", "Shadow Temple (Hakadan)", "Hakadan"),
    ("SCENE_BOTTOM_OF_THE_WELL", "Bottom of the Well (Hakadanch)", "Hakadanch"),
    ("SCENE_ICE_CAVERN", "Ice Cavern (Ice Doukuto)", "Ice Doukuto"),
    ("SCENE_GANONS_TOWER", "Ganon's Tower (Ganon)", "Ganon"),
    ("SCENE_GERUDO_TRAINING_GROUND", "Gerudo Training Ground (Men)", "Men"),
    ("SCENE_THIEVES_HIDEOUT", "Thieves' Hideout (Gerudoway)", "Gerudoway"),
    ("SCENE_INSIDE_GANONS_CASTLE", "Inside Ganon's Castle (Ganontika)", "Ganontika"),
    ("SCENE_GANONS_TOWER_COLLAPSE_INTERIOR", "Ganon's Tower (Collapsing) (Ganon Sonogo)", "Ganon Sonogo"),
    (
        "SCENE_INSIDE_GANONS_CASTLE_COLLAPSE",
        "Inside Ganon's Castle (Collapsing) (Ganontika Sonogo)",
        "Ganontika Sonogo",
    ),
    ("SCENE_TREASURE_BOX_SHOP", "Treasure Chest Shop (Takaraya)", "Takaraya"),
    ("SCENE_DEKU_TREE_BOSS", "Gohma's Lair (Ydan Boss)", "Ydan Boss"),
    ("SCENE_DODONGOS_CAVERN_BOSS", "King Dodongo's Lair (Ddan Boss)", "Ddan Boss"),
    ("SCENE_JABU_JABU_BOSS", "Barinade's Lair (Bdan Boss)", "Bdan Boss"),
    ("SCENE_FOREST_TEMPLE_BOSS", "Phantom Ganon's Lair (Moribossroom)", "Moribossroom"),
    ("SCENE_FIRE_TEMPLE_BOSS", "Volvagia's Lair (Fire Bs)", "Fire Bs"),
    ("SCENE_WATER_TEMPLE_BOSS", "Morpha's Lair (Mizusin Bs)", "Mizusin Bs"),
    ("SCENE_SPIRIT_TEMPLE_BOSS", "Twinrova's Lair & Iron Knuckle Mini-Boss Room (Jyasinboss)", "Jyasinboss"),
    ("SCENE_SHADOW_TEMPLE_BOSS", "Bongo Bongo's Lair (Hakadan Bs)", "Hakadan Bs"),
    ("SCENE_GANONDORF_BOSS", "Ganondorf's Lair (Ganon Boss)", "Ganon Boss"),
    (
        "SCENE_GANONS_TOWER_COLLAPSE_EXTERIOR",
        "Ganondorf's Death Scene (Tower Escape Exterior) (Ganon Final)",
        "Ganon Final",
    ),
    ("SCENE_MARKET_ENTRANCE_DAY", "Market Entrance (Child - Day) (Entra)", "Entra"),
    ("SCENE_MARKET_ENTRANCE_NIGHT", "Market Entrance (Child - Night) (Entra N)", "Entra N"),
    ("SCENE_MARKET_ENTRANCE_RUINS", "Market Entrance (Ruins) (Enrui)", "Enrui"),
    ("SCENE_BACK_ALLEY_DAY", "Back Alley (Day) (Market Alley)", "Market Alley"),
    ("SCENE_BACK_ALLEY_NIGHT", "Back Alley (Night) (Market Alley N)", "Market Alley N"),
    ("SCENE_MARKET_DAY", "Market (Child - Day) (Market Day)", "Market Day"),
    ("SCENE_MARKET_NIGHT", "Market (Child - Night) (Market Night)", "Market Night"),
    ("SCENE_MARKET_RUINS", "Market (Ruins) (Market Ruins)", "Market Ruins"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_DAY", "Temple of Time Exterior (Day) (Shrine)", "Shrine"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_NIGHT", "Temple of Time Exterior (Night) (Shrine N)", "Shrine N"),
    ("SCENE_TEMPLE_OF_TIME_EXTERIOR_RUINS", "Temple of Time Exterior (Ruins) (Shrine R)", "Shrine R"),
    ("SCENE_KNOW_IT_ALL_BROS_HOUSE", "Know-It-All Brothers' House (Kokiri Home)", "Kokiri Home"),
    ("SCENE_TWINS_HOUSE", "Twins' House (Kokiri Home3)", "Kokiri Home3"),
    ("SCENE_MIDOS_HOUSE", "Mido's House (Kokiri Home4)", "Kokiri Home4"),
    ("SCENE_SARIAS_HOUSE", "Saria's House (Kokiri Home5)", "Kokiri Home5"),
    ("SCENE_KAKARIKO_CENTER_GUEST_HOUSE", "Carpenter Boss's House (Kakariko)", "Kakariko"),
    ("SCENE_BACK_ALLEY_HOUSE", "Back Alley House (Man in Green) (Kakariko3)", "Kakariko3"),
    ("SCENE_BAZAAR", "Bazaar (Shop1)", "Shop1"),
    ("SCENE_KOKIRI_SHOP", "Kokiri Shop (Kokiri Shop)", "Kokiri Shop"),
    ("SCENE_GORON_SHOP", "Goron Shop (Golon)", "Golon"),
    ("SCENE_ZORA_SHOP", "Zora Shop (Zoora)", "Zoora"),
    ("SCENE_POTION_SHOP_KAKARIKO", "Kakariko Potion Shop (Drag)", "Drag"),
    ("SCENE_POTION_SHOP_MARKET", "Market Potion Shop (Alley Shop)", "Alley Shop"),
    ("SCENE_BOMBCHU_SHOP", "Bombchu Shop (Night Shop)", "Night Shop"),
    ("SCENE_HAPPY_MASK_SHOP", "Happy Mask Shop (Face Shop)", "Face Shop"),
    ("SCENE_LINKS_HOUSE", "Link's House (Link Home)", "Link Home"),
    ("SCENE_DOG_LADY_HOUSE", "Back Alley House (Dog Lady) (Impa)", "Impa"),
    ("SCENE_STABLE", "Stable (Malon Stable)", "Malon Stable"),
    ("SCENE_IMPAS_HOUSE", "Impa's House (Labo)", "Labo"),
    ("SCENE_LAKESIDE_LABORATORY", "Lakeside Laboratory (Hylia Labo)", "Hylia Labo"),
    ("SCENE_CARPENTERS_TENT", "Carpenters' Tent (Tent)", "Tent"),
    ("SCENE_GRAVEKEEPERS_HUT", "Gravekeeper's Hut (Hut)", "Hut"),
    ("SCENE_GREAT_FAIRYS_FOUNTAIN_MAGIC", "Great Fairy's Fountain (Upgrades) (Daiyousei Izumi)", "Daiyousei Izumi"),
    ("SCENE_FAIRYS_FOUNTAIN", "Fairy's Fountain (Healing Fairies) (Yousei Izumi Tate)", "Yousei Izumi Tate"),
    ("SCENE_GREAT_FAIRYS_FOUNTAIN_SPELLS", "Great Fairy's Fountain (Spells) (Yousei Izumi Yoko)", "Yousei Izumi Yoko"),
    ("SCENE_GROTTOS", "Grottos (Kakusiana)", "Kakusiana"),
    ("SCENE_REDEAD_GRAVE", "Grave (Redead) (Hakaana)", "Hakaana"),
    ("SCENE_GRAVE_WITH_FAIRYS_FOUNTAIN", "Grave (Fairy's Fountain) (Hakaana2)", "Hakaana2"),
    ("SCENE_ROYAL_FAMILYS_TOMB", "Royal Family's Tomb (Hakaana Ouke)", "Hakaana Ouke"),
    ("SCENE_SHOOTING_GALLERY", "Shooting Gallery (Syatekijyou)", "Syatekijyou"),
    ("SCENE_TEMPLE_OF_TIME", "Temple of Time (Tokinoma)", "Tokinoma"),
    ("SCENE_CHAMBER_OF_THE_SAGES", "Chamber of the Sages (Kenjyanoma)", "Kenjyanoma"),
    ("SCENE_CASTLE_COURTYARD_GUARDS_DAY", "Castle Hedge Maze (Day) (Hairal Niwa)", "Hairal Niwa"),
    ("SCENE_CASTLE_COURTYARD_GUARDS_NIGHT", "Castle Hedge Maze (Night) (Hairal Niwa N)", "Hairal Niwa N"),
    ("SCENE_CUTSCENE_MAP", "Cutscene Map (Hiral Demo)", "Hiral Demo"),
    ("SCENE_WINDMILL_AND_DAMPES_GRAVE", "Dampé's Grave & Windmill (Hakasitarelay)", "Hakasitarelay"),
    ("SCENE_FISHING_POND", "Fishing Pond (Turibori)", "Turibori"),
    ("SCENE_CASTLE_COURTYARD_ZELDA", "Castle Courtyard (Nakaniwa)", "Nakaniwa"),
    ("SCENE_BOMBCHU_BOWLING_ALLEY", "Bombchu Bowling Alley (Bowling)", "Bowling"),
    ("SCENE_LON_LON_BUILDINGS", "Lon Lon Ranch House & Tower (Souko)", "Souko"),
    ("SCENE_MARKET_GUARD_HOUSE", "Guard House (Miharigoya)", "Miharigoya"),
    ("SCENE_POTION_SHOP_GRANNY", "Granny's Potion Shop (Mahouya)", "Mahouya"),
    ("SCENE_GANON_BOSS", "Ganon's Tower Collapse & Battle Arena (Ganon Demo)", "Ganon Demo"),
    ("SCENE_HOUSE_OF_SKULLTULA", "House of Skulltula (Kinsuta)", "Kinsuta"),
    ("SCENE_HYRULE_FIELD", "Hyrule Field (Spot00)", "Spot00"),
    ("SCENE_KAKARIKO_VILLAGE", "Kakariko Village (Spot01)", "Spot01"),
    ("SCENE_GRAVEYARD", "Graveyard (Spot02)", "Spot02"),
    ("SCENE_ZORAS_RIVER", "Zora's River (Spot03)", "Spot03"),
    ("SCENE_KOKIRI_FOREST", "Kokiri Forest (Spot04)", "Spot04"),
    ("SCENE_SACRED_FOREST_MEADOW", "Sacred Forest Meadow (Spot05)", "Spot05"),
    ("SCENE_LAKE_HYLIA", "Lake Hylia (Spot06)", "Spot06"),
    ("SCENE_ZORAS_DOMAIN", "Zora's Domain (Spot07)", "Spot07"),
    ("SCENE_ZORAS_FOUNTAIN", "Zora's Fountain (Spot08)", "Spot08"),
    ("SCENE_GERUDO_VALLEY", "Gerudo Valley (Spot09)", "Spot09"),
    ("SCENE_LOST_WOODS", "Lost Woods (Spot10)", "Spot10"),
    ("SCENE_DESERT_COLOSSUS", "Desert Colossus (Spot11)", "Spot11"),
    ("SCENE_GERUDOS_FORTRESS", "Gerudo's Fortress (Spot12)", "Spot12"),
    ("SCENE_HAUNTED_WASTELAND", "Haunted Wasteland (Spot13)", "Spot13"),
    ("SCENE_HYRULE_CASTLE", "Hyrule Castle (Spot15)", "Spot15"),
    ("SCENE_DEATH_MOUNTAIN_TRAIL", "Death Mountain Trail (Spot16)", "Spot16"),
    ("SCENE_DEATH_MOUNTAIN_CRATER", "Death Mountain Crater (Spot17)", "Spot17"),
    ("SCENE_GORON_CITY", "Goron City (Spot18)", "Spot18"),
    ("SCENE_LON_LON_RANCH", "Lon Lon Ranch (Spot20)", "Spot20"),
    ("SCENE_OUTSIDE_GANONS_CASTLE", "Ganon's Castle Exterior (Ganon Tou)", "Ganon Tou"),
    ("SCENE_TEST01", "Jungle Gym (Test01)", "Test01"),
    ("SCENE_BESITU", "Ganondorf Test Room (Besitu)", "Besitu"),
    ("SCENE_DEPTH_TEST", "Depth Test (Depth Test)", "Depth Test"),
    ("SCENE_SYOTES", "Stalfos Mini-Boss Room (Syotes)", "Syotes"),
    ("SCENE_SYOTES2", "Stalfos Boss ROom (Syotes2)", "Syotes2"),
    ("SCENE_SUTARU", "Sutaru (Sutaru)", "Sutaru"),
    ("SCENE_HAIRAL_NIWA2", "Castle Hedge Maze (Early) (Hairal Niwa2)", "Hairal Niwa2"),
    ("SCENE_SASATEST", "Sasatest (Sasatest)", "Sasatest"),
    ("SCENE_TESTROOM", "Treasure Chest Room (Testroom)", "Testroom"),
]

mmSceneIDToName = {
    "SCENE_DEKU_TREE": "ydan",
    "SCENE_DODONGOS_CAVERN": "ddan",
    "SCENE_JABU_JABU": "bdan",
    "SCENE_FOREST_TEMPLE": "Bmori1",
    "SCENE_FIRE_TEMPLE": "HIDAN",
    "SCENE_WATER_TEMPLE": "MIZUsin",
    "SCENE_SPIRIT_TEMPLE": "jyasinzou",
    "SCENE_SHADOW_TEMPLE": "HAKAdan",
    "SCENE_BOTTOM_OF_THE_WELL": "HAKAdanCH",
    "SCENE_ICE_CAVERN": "ice_doukutu",
    "SCENE_GANONS_TOWER": "ganon",
    "SCENE_GERUDO_TRAINING_GROUND": "men",
    "SCENE_THIEVES_HIDEOUT": "gerudoway",
    "SCENE_INSIDE_GANONS_CASTLE": "ganontika",
    "SCENE_GANONS_TOWER_COLLAPSE_INTERIOR": "ganon_sonogo",
    "SCENE_INSIDE_GANONS_CASTLE_COLLAPSE": "ganontikasonogo",
    "SCENE_TREASURE_BOX_SHOP": "takaraya",
    "SCENE_DEKU_TREE_BOSS": "ydan_boss",
    "SCENE_DODONGOS_CAVERN_BOSS": "ddan_boss",
    "SCENE_JABU_JABU_BOSS": "bdan_boss",
    "SCENE_FOREST_TEMPLE_BOSS": "moribossroom",
    "SCENE_FIRE_TEMPLE_BOSS": "FIRE_bs",
    "SCENE_WATER_TEMPLE_BOSS": "MIZUsin_bs",
    "SCENE_SPIRIT_TEMPLE_BOSS": "jyasinboss",
    "SCENE_SHADOW_TEMPLE_BOSS": "HAKAdan_bs",
    "SCENE_GANONDORF_BOSS": "ganon_boss",
    "SCENE_GANONS_TOWER_COLLAPSE_EXTERIOR": "ganon_final",
    "SCENE_MARKET_ENTRANCE_DAY": "entra",
    "SCENE_MARKET_ENTRANCE_NIGHT": "entra_n",
    "SCENE_MARKET_ENTRANCE_RUINS": "enrui",
    "SCENE_BACK_ALLEY_DAY": "market_alley",
    "SCENE_BACK_ALLEY_NIGHT": "market_alley_n",
    "SCENE_MARKET_DAY": "market_day",
    "SCENE_MARKET_NIGHT": "market_night",
    "SCENE_MARKET_RUINS": "market_ruins",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_DAY": "shrine",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_NIGHT": "shrine_n",
    "SCENE_TEMPLE_OF_TIME_EXTERIOR_RUINS": "shrine_r",
    "SCENE_KNOW_IT_ALL_BROS_HOUSE": "kokiri_home",
    "SCENE_TWINS_HOUSE": "kokiri_home3",
    "SCENE_MIDOS_HOUSE": "kokiri_home4",
    "SCENE_SARIAS_HOUSE": "kokiri_home5",
    "SCENE_KAKARIKO_CENTER_GUEST_HOUSE": "kakariko",
    "SCENE_BACK_ALLEY_HOUSE": "kakariko3",
    "SCENE_BAZAAR": "shop1",
    "SCENE_KOKIRI_SHOP": "kokiri_shop",
    "SCENE_GORON_SHOP": "golon",
    "SCENE_ZORA_SHOP": "zoora",
    "SCENE_POTION_SHOP_KAKARIKO": "drag",
    "SCENE_POTION_SHOP_MARKET": "alley_shop",
    "SCENE_BOMBCHU_SHOP": "night_shop",
    "SCENE_HAPPY_MASK_SHOP": "face_shop",
    "SCENE_LINKS_HOUSE": "link_home",
    "SCENE_DOG_LADY_HOUSE": "impa",
    "SCENE_STABLE": "malon_stable",
    "SCENE_IMPAS_HOUSE": "labo",
    "SCENE_LAKESIDE_LABORATORY": "hylia_labo",
    "SCENE_CARPENTERS_TENT": "tent",
    "SCENE_GRAVEKEEPERS_HUT": "hut",
    "SCENE_GREAT_FAIRYS_FOUNTAIN_MAGIC": "daiyousei_izumi",
    "SCENE_FAIRYS_FOUNTAIN": "yousei_izumi_tate",
    "SCENE_GREAT_FAIRYS_FOUNTAIN_SPELLS": "yousei_izumi_yoko",
    "SCENE_GROTTOS": "kakusiana",
    "SCENE_REDEAD_GRAVE": "hakaana",
    "SCENE_GRAVE_WITH_FAIRYS_FOUNTAIN": "hakaana2",
    "SCENE_ROYAL_FAMILYS_TOMB": "hakaana_ouke",
    "SCENE_SHOOTING_GALLERY": "syatekijyou",
    "SCENE_TEMPLE_OF_TIME": "tokinoma",
    "SCENE_CHAMBER_OF_THE_SAGES": "kenjyanoma",
    "SCENE_CASTLE_COURTYARD_GUARDS_DAY": "hairal_niwa",
    "SCENE_CASTLE_COURTYARD_GUARDS_NIGHT": "hairal_niwa_n",
    "SCENE_CUTSCENE_MAP": "hiral_demo",
    "SCENE_WINDMILL_AND_DAMPES_GRAVE": "hakasitarelay",
    "SCENE_FISHING_POND": "turibori",
    "SCENE_CASTLE_COURTYARD_ZELDA": "nakaniwa",
    "SCENE_BOMBCHU_BOWLING_ALLEY": "bowling",
    "SCENE_LON_LON_BUILDINGS": "souko",
    "SCENE_MARKET_GUARD_HOUSE": "miharigoya",
    "SCENE_POTION_SHOP_GRANNY": "mahouya",
    "SCENE_GANON_BOSS": "ganon_demo",
    "SCENE_HOUSE_OF_SKULLTULA": "kinsuta",
    "SCENE_HYRULE_FIELD": "spot00",
    "SCENE_KAKARIKO_VILLAGE": "spot01",
    "SCENE_GRAVEYARD": "spot02",
    "SCENE_ZORAS_RIVER": "spot03",
    "SCENE_KOKIRI_FOREST": "spot04",
    "SCENE_SACRED_FOREST_MEADOW": "spot05",
    "SCENE_LAKE_HYLIA": "spot06",
    "SCENE_ZORAS_DOMAIN": "spot07",
    "SCENE_ZORAS_FOUNTAIN": "spot08",
    "SCENE_GERUDO_VALLEY": "spot09",
    "SCENE_LOST_WOODS": "spot10",
    "SCENE_DESERT_COLOSSUS": "spot11",
    "SCENE_GERUDOS_FORTRESS": "spot12",
    "SCENE_HAUNTED_WASTELAND": "spot13",
    "SCENE_HYRULE_CASTLE": "spot15",
    "SCENE_DEATH_MOUNTAIN_TRAIL": "spot16",
    "SCENE_DEATH_MOUNTAIN_CRATER": "spot17",
    "SCENE_GORON_CITY": "spot18",
    "SCENE_LON_LON_RANCH": "spot20",
    "SCENE_OUTSIDE_GANONS_CASTLE": "ganon_tou",
    "SCENE_TEST01": "test01",
    "SCENE_BESITU": "besitu",
    "SCENE_DEPTH_TEST": "depth_test",
    "SCENE_SYOTES": "syotes",
    "SCENE_SYOTES2": "syotes2",
    "SCENE_SUTARU": "sutaru",
    "SCENE_HAIRAL_NIWA2": "hairal_niwa2",
    "SCENE_SASATEST": "sasatest",
    "SCENE_TESTROOM": "testroom",
}

mmEnumCamTransition = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "0x00", "0x00"),
    # ("0x0F", "0x0F", "0x0F"),
    # ("0xFF", "0xFF", "0xFF"),
]

# see curRoom.unk_03
mmEnumRoomBehaviour = [
    ("Custom", "Custom", "Custom"),
    ("0x00", "Default", "Default"),
    ("0x01", "Dungeon Behavior (Z-Target, Sun's Song)", "Dungeon Behavior (Z-Target, Sun's Song)"),
    ("0x02", "Disable Backflips/Sidehops", "Disable Backflips/Sidehops"),
    ("0x03", "Disable Color Dither", "Disable Color Dither"),
    ("0x04", "(?) Horse Camera Related", "(?) Horse Camera Related"),
    ("0x05", "Disable Darker Screen Effect (NL/Spins)", "Disable Darker Screen Effect (NL/Spins)"),
]

mmEnumExitIndex = [
    ("Custom", "Custom", "Custom"),
    ("Default", "Default", "Default"),
]

mmEnumSceneSetupPreset = [
    ("Custom", "Custom", "Custom"),
    ("All Scene Setups", "All Scene Setups", "All Scene Setups"),
    ("All Non-Cutscene Scene Setups", "All Non-Cutscene Scene Setups", "All Non-Cutscene Scene Setups"),
]

mmEnumDrawConfig = [
    ("Custom", "Custom", "Custom"),
    ("SDC_DEFAULT", "Default", "Default"),
    ("SDC_HYRULE_FIELD", "Hyrule Field (Spot00)", "Spot00"),
    ("SDC_KAKARIKO_VILLAGE", "Kakariko Village (Spot01)", "Spot01"),
    ("SDC_ZORAS_RIVER", "Zora's River (Spot03)", "Spot03"),
    ("SDC_KOKIRI_FOREST", "Kokiri Forest (Spot04)", "Spot04"),
    ("SDC_LAKE_HYLIA", "Lake Hylia (Spot06)", "Spot06"),
    ("SDC_ZORAS_DOMAIN", "Zora's Domain (Spot07)", "Spot07"),
    ("SDC_ZORAS_FOUNTAIN", "Zora's Fountain (Spot08)", "Spot08"),
    ("SDC_GERUDO_VALLEY", "Gerudo Valley (Spot09)", "Spot09"),
    ("SDC_LOST_WOODS", "Lost Woods (Spot10)", "Spot10"),
    ("SDC_DESERT_COLOSSUS", "Desert Colossus (Spot11)", "Spot11"),
    ("SDC_GERUDOS_FORTRESS", "Gerudo's Fortress (Spot12)", "Spot12"),
    ("SDC_HAUNTED_WASTELAND", "Haunted Wasteland (Spot13)", "Spot13"),
    ("SDC_HYRULE_CASTLE", "Hyrule Castle (Spot15)", "Spot15"),
    ("SDC_DEATH_MOUNTAIN_TRAIL", "Death Mountain Trail (Spot16)", "Spot16"),
    ("SDC_DEATH_MOUNTAIN_CRATER", "Death Mountain Crater (Spot17)", "Spot17"),
    ("SDC_GORON_CITY", "Goron City (Spot18)", "Spot18"),
    ("SDC_LON_LON_RANCH", "Lon Lon Ranch (Spot20)", "Spot20"),
    ("SDC_FIRE_TEMPLE", "Fire Temple (Hidan)", "Hidan"),
    ("SDC_DEKU_TREE", "Inside the Deku Tree (Ydan)", "Ydan"),
    ("SDC_DODONGOS_CAVERN", "Dodongo's Cavern (Ddan)", "Ddan"),
    ("SDC_JABU_JABU", "Inside Jabu Jabu's Belly (Bdan)", "Bdan"),
    ("SDC_FOREST_TEMPLE", "Forest Temple (Bmori1)", "Bmori1"),
    ("SDC_WATER_TEMPLE", "Water Temple (Mizusin)", "Mizusin"),
    ("SDC_SHADOW_TEMPLE_AND_WELL", "Shadow Temple (Hakadan)", "Hakadan"),
    ("SDC_SPIRIT_TEMPLE", "Spirit Temple (Jyasinzou)", "Jyasinzou"),
    ("SDC_INSIDE_GANONS_CASTLE", "Inside Ganon's Castle (Ganontika)", "Ganontika"),
    ("SDC_GERUDO_TRAINING_GROUND", "Gerudo Training Ground (Men)", "Men"),
    ("SDC_DEKU_TREE_BOSS", "Gohma's Lair (Ydan Boss)", "Ydan Boss"),
    ("SDC_WATER_TEMPLE_BOSS", "Morpha's Lair (Mizusin Bs)", "Mizusin Bs"),
    ("SDC_TEMPLE_OF_TIME", "Temple of Time (Tokinoma)", "Tokinoma"),
    ("SDC_GROTTOS", "Grottos (Kakusiana)", "Kakusiana"),
    ("SDC_CHAMBER_OF_THE_SAGES", "Chamber of the Sages (Kenjyanoma)", "Kenjyanoma"),
    ("SDC_GREAT_FAIRYS_FOUNTAIN", "Great Fairy Fountain", "Great Fairy Fountain"),
    ("SDC_SHOOTING_GALLERY", "Shooting Gallery (Syatekijyou)", "Syatekijyou"),
    ("SDC_CASTLE_COURTYARD_GUARDS", "Castle Hedge Maze (Day) (Hairal Niwa)", "Hairal Niwa"),
    ("SDC_OUTSIDE_GANONS_CASTLE", "Ganon's Castle Exterior (Ganon Tou)", "Ganon Tou"),
    ("SDC_ICE_CAVERN", "Ice Cavern (Ice Doukuto)", "Ice Doukuto"),
    (
        "SDC_GANONS_TOWER_COLLAPSE_EXTERIOR",
        "Ganondorf's Death Scene (Tower Escape Exterior) (Ganon Final)",
        "Ganon Final",
    ),
    ("SDC_FAIRYS_FOUNTAIN", "Fairy Fountain", "Fairy Fountain"),
    ("SDC_THIEVES_HIDEOUT", "Thieves' Hideout (Gerudoway)", "Gerudoway"),
    ("SDC_BOMBCHU_BOWLING_ALLEY", "Bombchu Bowling Alley (Bowling)", "Bowling"),
    ("SDC_ROYAL_FAMILYS_TOMB", "Royal Family's Tomb (Hakaana Ouke)", "Hakaana Ouke"),
    ("SDC_LAKESIDE_LABORATORY", "Lakeside Laboratory (Hylia Labo)", "Hylia Labo"),
    ("SDC_LON_LON_BUILDINGS", "Lon Lon Ranch House & Tower (Souko)", "Souko"),
    ("SDC_MARKET_GUARD_HOUSE", "Guard House (Miharigoya)", "Miharigoya"),
    ("SDC_POTION_SHOP_GRANNY", "Granny's Potion Shop (Mahouya)", "Mahouya"),
    ("SDC_CALM_WATER", "Calm Water", "Calm Water"),
    ("SDC_GRAVE_EXIT_LIGHT_SHINING", "Grave Exit Light Shining", "Grave Exit Light Shining"),
    ("SDC_BESITU", "Ganondorf Test Room (Besitu)", "Besitu"),
    ("SDC_FISHING_POND", "Fishing Pond (Turibori)", "Turibori"),
    ("SDC_GANONS_TOWER_COLLAPSE_INTERIOR", "Ganon's Tower (Collapsing) (Ganon Sonogo)", "Ganon Sonogo"),
    ("SDC_INSIDE_GANONS_CASTLE_COLLAPSE", "Inside Ganon's Castle (Collapsing) (Ganontika Sonogo)", "Ganontika Sonogo"),
]

mmSceneNameToID = {val: key for key, val in mmSceneIDToName.items()}
