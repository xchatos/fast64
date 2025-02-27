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
    ("0x02", "Termina Field", "Termina Field"),
    ("0x03", "Chase", "Chase"),
    ("0x04", "Majora's Theme", "Majora's Theme"),
    ("0x05", "Clock Tower", "Clock Tower"),
    ("0x06", "Stone Tower Temple", "Stone Tower Temple"),
    ("0x07", "Stone Tower Temple Upside-down", "Stone Tower Temple Upside-down"),
    ("0x08", "Missed Event 1", "Missed Event 1"),
    ("0x09", "Missed Event 2", "Missed Event 2"),
    ("0x0A", "Happy Mask Saleman's Theme", "Happy Mask Saleman's Theme"),
    ("0x0B", "Song Of Healing", "Song Of Healing"),
    ("0x0C", "Southern Swamp", "Southern Swamp"),
    ("0x0D", "Ghost Attack", "Ghost Attack"),
    ("0x0E", "Boat Cruise", "Boat Cruise"),
    ("0x0F", "Sharp's Curse", "Sharp's Curse"),
    ("0x10", "Great Bay Coast", "Great Bay Coast"),
    ("0x11", "Ikana Valley", "Ikana Valley"),
    ("0x12", "Deku Palace", "Deku Palace"),
    ("0x13", "Mountain Village", "Mountain Village"),
    ("0x14", "Pirates' Fortress", "Pirates' Fortress"),
    ("0x15", "Clock Town, First Day", "Clock Town, First Day"),
    ("0x16", "Clock Town, Second Day", "Clock Town, Second Day"),
    ("0x17", "Clock Town, Third Day", "Clock Town, Third Day"),
    ("0x18", "File Select", "File Select"),
    ("0x19", "Event Clear", "Event Clear"),
    ("0x1A", "Battle", "Battle"),
    ("0x1B", "Boss Battle", "Boss Battle"),
    ("0x1C", "Woodfall Temple", "Woodfall Temple"),
    ("0x1D", "Loads one of sequences 0x15, 0x16, or 0x17", "Loads one of sequences 0x15, 0x16, or 0x17"),
    ("0x1E", "Opening", "Opening"),
    ("0x1F", "House", "House"),
    ("0x20", "Game Over", "Game Over"),
    ("0x21", "Boss Clear", "Boss Clear"),
    ("0x22", "Item Catch", "Item Catch"),
    ("0x23", "Points to Clock Town, Second Day", "Points to Clock Town, Second Day"),
    ("0x24", "Get A Heart Container!", "Get A Heart Container!"),
    ("0x25", "Mini Game", "Mini Game"),
    ("0x26", "Goron Race", "Goron Race"),
    ("0x27", "Music Box House", "Music Box House"),
    ("0x28", "Fairy's Fountain - File Select", "Fairy's Fountain - File Select"),
    ("0x29", "Zelda's Theme", "Zelda's Theme"),
    ("0x2A", "Rosa Sisters", "Rosa Sisters"),
    ("0x2B", "Open Treasure Box", "Open Treasure Box"),
    ("0x2C", "Marine Research Laboratory", "Marine Research Laboratory"),
    ("0x2D", "Giants' Theme", "Giants' Theme"),
    ("0x2E", "Guru-Guru's Song", "Guru-Guru's Song"),
    ("0x2F", "Romani Ranch", "Romani Ranch"),
    ("0x30", "Goron Village", "Goron Village"),
    ("0x31", "Mayor's Meeting", "Mayor's Meeting"),
    ("0x32", "Ocarina “Epona's Song”", "Ocarina “Epona's Song”"),
    ("0x33", "Ocarina “Sun's Song”", "Ocarina “Sun's Song”"),
    ("0x34", "Ocarina “Song Of Time”", "Ocarina “Song Of Time”"),
    ("0x35", "Ocarina “Song Of Storms”", "Ocarina “Song Of Storms”"),
    ("0x36", "Zora Hall" , "Zora Hall" ),
    ("0x37", "Get A Mask!", "Get A Mask!"),
    ("0x38", "Middle Boss Battle", "Middle Boss Battle"),
    ("0x39", "Small Item Catch", "Small Item Catch"),
    ("0x3A", "Astral Observatory", "Astral Observatory"),
    ("0x3B", "Cavern - Grottos", "Cavern - Grottos"),
    ("0x3C", "Milk Bar", "Milk Bar"),
    ("0x3D", "Enter Zelda - leftover from OoT", "Enter Zelda - leftover from OoT"),
    ("0x3E", "Woods Of Mystery - Saria's Song", "Woods Of Mystery - Saria's Song"),
    ("0x3F", "Goron Race Goal", "Goron Race Goal"),
    ("0x40", "Horse Race", "Horse Race"),
    ("0x41", "Horse Race Goal", "Horse Race Goal"),
    ("0x42", "Gorman Track", "Gorman Track"),
    ("0x43", "Magic Hags' Potion Shop", "Magic Hags' Potion Shop"),
    ("0x44", "Shop", "Shop"),
    ("0x45", "Owl", "Owl"),
    ("0x46", "Shooting Gallery", "Shooting Gallery"),
    ("0x47", "Ocarina “Song Of Soaring”", "Ocarina “Song Of Soaring”"),
    ("0x48", "Ocarina “Song Of Healing”", "Ocarina “Song Of Healing”"),
    ("0x49", "Ocarina “Inverted Song Of Time”", "Ocarina “Inverted Song Of Time”"),
    ("0x4A", "Ocarina “Song Of Double Time”", "Ocarina “Song Of Double Time”"),
    ("0x4B", "Sonata of Awakening", "Sonata of Awakening"),
    ("0x4C", "Goron Lullaby", "Goron Lullaby"),
    ("0x4D", "New Wave Bossa Nova - saxophone and vocals", "New Wave Bossa Nova - saxophone and vocals"),
    ("0x4E", "Elegy Of Emptiness", "Elegy Of Emptiness"),
    ("0x4F", "Oath To Order", "Oath To Order"),
    ("0x50", "Swordsman's School", "Swordsman's School"),
    ("0x51", "Ocarina “Goron Lullaby Intro”", "Ocarina “Goron Lullaby Intro”"),
    ("0x52", "Get The Ocarina!", "Get The Ocarina!"),
    ("0x53", "Bremen March", "Bremen March"),
    ("0x54", "Ballad Of The Wind Fish - Milk Bar quartet", "Ballad Of The Wind Fish - Milk Bar quartet"),
    ("0x55", "Song Of Soaring", "Song Of Soaring"),
    ("0x56", "Points to Milk Bar sequence", "Points to Milk Bar sequence"),
    ("0x57", "Last Day", "Last Day"),
    ("0x58", "Mikau - looping part of the song", "Mikau - looping part of the song"),
    ("0x59", "Mikau - Last chord", "Mikau - Last chord"),
    ("0x5A", "Frog Song - conducting the frogs with Don Gero's Mask", "Frog Song - conducting the frogs with Don Gero's Mask"),
    ("0x5B", "Ocarina “Sonata Of Awakening”", "Ocarina “Sonata Of Awakening”"),
    ("0x5C", "Ocarina “Goron Lullaby”", "Ocarina “Goron Lullaby”"),
    ("0x5D", "Ocarina “New Wave Bossa Nova”", "Ocarina “New Wave Bossa Nova”"),
    ("0x5E", "Ocarina “Elegy of Emptiness”", "Ocarina “Elegy of Emptiness”"),
    ("0x5F", "Ocarina “Oath To Order”", "Ocarina “Oath To Order”"),
    ("0x60", "Majora Boss Room. Points to Last Day sequence", "Majora Boss Room. Points to Last Day sequence"),
    ("0x61", "Points to Ocarina “Goron Lullaby Intro”", "Points to Ocarina “Goron Lullaby Intro”"),
    ("0x62", "Bass & Guitar Session", "Bass & Guitar Session"),
    ("0x63", "Piano Solo", "Piano Solo"),
    ("0x64", "The Indigo-Go's", "The Indigo-Go's"),
    ("0x65", "Snowhead Temple", "Snowhead Temple"),
    ("0x66", "Great Bay Temple", "Great Bay Temple" ),
    ("0x67", "New Wave Bossa Nova - saxophone only", "New Wave Bossa Nova - saxophone only"),
    ("0x68", "New Wave Bossa Nova - vocals only", "New Wave Bossa Nova - vocals only"),
    ("0x69", "Majora's Wrath Battle", "Majora's Wrath Battle"),
    ("0x6A", "Majora's Incarnate Battle", "Majora's Incarnate Battle"),
    ("0x6B", "Majora's Mask Battle", "Majora's Mask Battle"),
    ("0x6C", "Bass Practice", "Bass Practice"),
    ("0x6D", "Drums Practice", "Drums Practice"),
    ("0x6E", "Piano Practice", "Piano Practice"),
    ("0x6F", "Ikana Castle", "Ikana Castle"),
    ("0x70", "Calling The Four Giants", "Calling The Four Giants"),
    ("0x71", "Kamaro's Dance", "Kamaro's Dance"),
    ("0x72", "Cremia's Carriage", "Cremia's Carriage"),
    ("0x73", "Keaton's Quiz", "Keaton's Quiz"),
    ("0x74", "The End / Credits", "The End / Credits"),
    ("0x75", "Similar to Opening Loop", "Similar to Opening Loop"),
    ("0x76", "Title Theme", "Title Theme"),
    ("0x77", "Woodfall Rises", "Woodfall Rises"),
    ("0x78", "Southern Swamp Clears", "Southern Swamp Clears"),
    ("0x79", "Snowhead Clear", "Snowhead Clear"),
    ("0x7B", "To The Moon", "To The Moon"),
    ("0x7C", "The Giants' Exit", "The Giants' Exit"),
    ("0x7D", "Tatl & Tael", "Tatl & Tael"),
    ("0x7E", "Moon's Destruction", "Moon's Destruction"),
    ("0x7F", "The End / Credits - second half", "The End / Credits - second half"),
    ("0xFFFF", "Disable Music", "Disable Music"),
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
    ("SCENE_20SICHITAI2", "Southern Swamp (Clear)", "Z2_20SICHITAI2"),
    ("SCENE_KAKUSIANA", "Lone Peak Shrine & Grottos", "KAKUSIANA"),
    ("SCENE_SPOT00", "Cutscene Scene", "SPOT00"),
    ("SCENE_WITCH_SHOP", "Magic Hags' Potion Shop", "Z2_WITCH_SHOP"),
    ("SCENE_LAST_BS", "Majora's Lair", "Z2_LAST_BS"),
    ("SCENE_HAKASHITA", "Beneath the Graveyard", "Z2_HAKASHITA"),
    ("SCENE_AYASHIISHOP", "Curiosity Shop", "Z2_AYASHIISHOP"),
    ("SCENE_OMOYA", "Mama's House (Ranch House in PAL) & Barn", "Z2_OMOYA"),
    ("SCENE_BOWLING", "Honey & Darling's Shop", "Z2_BOWLING"),
    ("SCENE_SONCHONOIE", "The Mayor's Residence", "Z2_SONCHONOIE"),
    ("SCENE_IKANA", "Ikana Canyon", "Z2_IKANA"),
    ("SCENE_KAIZOKU", "Pirates' Fortress", "Z2_KAIZOKU"),
    ("SCENE_MILK_BAR", "Milk Bar", "Z2_MILK_BAR"),
    ("SCENE_INISIE_N", "Stone Tower Temple", "Z2_INISIE_N"),
    ("SCENE_TAKARAYA", "Treasure Chest Shop", "Z2_TAKARAYA"),
    ("SCENE_INISIE_R", "Inverted Stone Tower Temple", "Z2_INISIE_R"),
    ("SCENE_OKUJOU", "Clock Tower Rooftop", "Z2_OKUJOU"),
    ("SCENE_OPENINGDAN", "Before Clock Town", "Z2_OPENINGDAN"),
    ("SCENE_MITURIN", "Woodfall Temple", "Z2_MITURIN"),
    ("SCENE_13HUBUKINOMITI", "Path to Mountain Village", "Z2_13HUBUKINOMITI"),
    ("SCENE_CASTLE", "Ancient Castle of Ikana", "Z2_CASTLE"),
    ("SCENE_DEKUTES", "Deku Scrub Playground", "Z2_DEKUTES"),
    ("SCENE_MITURIN_BS", "Odolwa's Lair", "Z2_MITURIN_BS"),
    ("SCENE_SYATEKI_MIZU", "Town Shooting Gallery", "Z2_SYATEKI_MIZU"),
    ("SCENE_HAKUGIN", "Snowhead Temple", "Z2_HAKUGIN"),
    ("SCENE_ROMANYMAE", "Milk Road", "Z2_ROMANYMAE"),
    ("SCENE_PIRATE", "Pirates' Fortress Interior", "Z2_PIRATE"),
    ("SCENE_SYATEKI_MORI", "Swamp Shooting Gallery", "Z2_SYATEKI_MORI"),
    ("SCENE_SINKAI", "Pinnacle Rock", "Z2_SINKAI"),
    ("SCENE_YOUSEI_IZUMI", "Fairy's Fountain", "Z2_YOUSEI_IZUMI"),
    ("SCENE_KINSTA1", "Swamp Spider House", "Z2_KINSTA1"),
    ("SCENE_KINDAN2", "Oceanside Spider House", "Z2_KINDAN2"),
    ("SCENE_TENMON_DAI", "Astral Observatory", "Z2_TENMON_DAI"),
    ("SCENE_LAST_DEKU", "Moon Deku Trial", "Z2_LAST_DEKU"),
    ("SCENE_22DEKUCITY", "Deku Palace", "Z2_22DEKUCITY"),
    ("SCENE_KAJIYA", "Mountain Smithy", "Z2_KAJIYA"),
    ("SCENE_00KEIKOKU", "Termina Field", "Z2_00KEIKOKU"),
    ("SCENE_POSTHOUSE", "Post Office", "Z2_POSTHOUSE"),
    ("SCENE_LABO", "Marine Research Lab", "Z2_LABO"),
    ("SCENE_DANPEI2TEST", "Beneath the Graveyard (Day 3) and Dampe's House", "Z2_DANPEI2TEST"),
    ("SCENE_16GORON_HOUSE", "Goron Shrine", "Z2_16GORON_HOUSE"),
    ("SCENE_33ZORACITY", "Zora Hall", "Z2_33ZORACITY"),
    ("SCENE_8ITEMSHOP", "Trading Post", "Z2_8ITEMSHOP"),
    ("SCENE_F01", "Romani Ranch", "Z2_F01"),
    ("SCENE_INISIE_BS", "Twinmold's Lair", "Z2_INISIE_BS"),
    ("SCENE_30GYOSON", "Great Bay Coast", "Z2_30GYOSON"),
    ("SCENE_31MISAKI", "Zora Cape", "Z2_31MISAKI"),
    ("SCENE_TAKARAKUJI", "Lottery Shop", "Z2_TAKARAKUJI"),
    ("SCENE_TORIDE", "Pirates' Fortress Moat", "Z2_TORIDE"),
    ("SCENE_FISHERMAN", "Fisherman's Hut", "Z2_FISHERMAN"),
    ("SCENE_GORONSHOP", "Goron Shop", "Z2_GORONSHOP"),
    ("SCENE_DEKU_KING", "Deku King's Chamber", "Z2_DEKU_KING"),
    ("SCENE_LAST_GORON", "Moon Goron Trial", "Z2_LAST_GORON"),
    ("SCENE_24KEMONOMITI", "Road to Southern Swamp", "Z2_24KEMONOMITI"),
    ("SCENE_F01_B", "Doggy Racetrack", "Z2_F01_B"),
    ("SCENE_F01C", "Cucco Shack", "Z2_F01C"),
    ("SCENE_BOTI", "Ikana Graveyard", "Z2_BOTI"),
    ("SCENE_HAKUGIN_BS", "Goht's Lair", "Z2_HAKUGIN_BS"),
    ("SCENE_20SICHITAI", "Southern Swamp (poison)", "Z2_20SICHITAI"),
    ("SCENE_21MITURINMAE", "Woodfall", "Z2_21MITURINMAE"),
    ("SCENE_LAST_ZORA", "Moon Zora Trial", "Z2_LAST_ZORA"),
    ("SCENE_11GORONNOSATO2", "Goron Village (spring)", "Z2_11GORONNOSATO2"),
    ("SCENE_SEA", "Great Bay Temple", "Z2_SEA"),
    ("SCENE_35TAKI", "Waterfall Rapids", "Z2_35TAKI"),
    ("SCENE_REDEAD", "Beneath the Well", "Z2_REDEAD"),
    ("SCENE_BANDROOM", "Zora Hall Rooms", "Z2_BANDROOM"),
    ("SCENE_11GORONNOSATO", "Goron Village (winter)", "Z2_11GORONNOSATO"),
    ("SCENE_GORON_HAKA", "Goron Graveyard", "Z2_GORON_HAKA"),
    ("SCENE_SECOM", "Sakon's Hideout", "Z2_SECOM"),
    ("SCENE_10YUKIYAMANOMURA", "Mountain Village (winter)", "Z2_10YUKIYAMANOMURA"),
    ("SCENE_TOUGITES", "Ghost Hut", "Z2_TOUGITES"),
    ("SCENE_DANPEI", "Deku Shrine", "Z2_DANPEI"),
    ("SCENE_IKANAMAE", "Road to Ikana", "Z2_IKANAMAE"),
    ("SCENE_DOUJOU", "Swordsman's School", "Z2_DOUJOU"),
    ("SCENE_MUSICHOUSE", "Music Box House", "Z2_MUSICHOUSE"),
    ("SCENE_IKNINSIDE", "Igos du Ikana's Lair", "Z2_IKNINSIDE"),
    ("SCENE_MAP_SHOP", "Tourist Information", "Z2_MAP_SHOP"),
    ("SCENE_F40", "Stone Tower", "Z2_F40"),
    ("SCENE_F41", "Inverted Stone Tower", "Z2_F41"),
    ("SCENE_10YUKIYAMANOMURA2", "Mountain Village (spring)", "Z2_10YUKIYAMANOMURA2"),
    ("SCENE_14YUKIDAMANOMITI", "Path to Snowhead", "Z2_14YUKIDAMANOMITI"),
    ("SCENE_12HAKUGINMAE", "Snowhead", "Z2_12HAKUGINMAE"),
    ("SCENE_17SETUGEN", "Path to Goron Village (winter)", "Z2_17SETUGEN"),
    ("SCENE_17SETUGEN2", "Path to Goron Village (spring)", "Z2_17SETUGEN2"),
    ("SCENE_SEA_BS", "Gyorg's Lair", "Z2_SEA_BS"),
    ("SCENE_RANDOM", "Secret Shrine", "Z2_RANDOM"),
    ("SCENE_YADOYA", "Stock Pot Inn", "Z2_YADOYA"),
    ("SCENE_KONPEKI_ENT", "Great Bay Cutscene", "Z2_KONPEKI_ENT"),
    ("SCENE_INSIDETOWER", "Clock Tower Interior", "Z2_INSIDETOWER"),
    ("SCENE_26SARUNOMORI", "Woods of Mystery", "Z2_26SARUNOMORI"),
    ("SCENE_LOST_WOODS", "Lost Woods (Intro)", "Z2_LOST_WOODS"),
    ("SCENE_LAST_LINK", "Moon Link Trial", "Z2_LAST_LINK"),
    ("SCENE_SOUGEN", "The Moon", "Z2_SOUGEN"),
    ("SCENE_BOMYA", "Bomb Shop", "Z2_BOMYA"),
    ("SCENE_KYOJINNOMA", "Giants' Chamber", "Z2_KYOJINNOMA"),
    ("SCENE_KOEPONARACE", "Gorman Track", "Z2_KOEPONARACE"),
    ("SCENE_GORONRACE", "Goron Racetrack", "Z2_GORONRACE"),
    ("SCENE_TOWN", "East Clock Town", "Z2_TOWN"),
    ("SCENE_ICHIBA", "West Clock Town", "Z2_ICHIBA"),
    ("SCENE_BACKTOWN", "North Clock Town", "Z2_BACKTOWN"),
    ("SCENE_CLOCKTOWER", "South Clock Town", "Z2_CLOCKTOWER"),
    ("SCENE_ALLEY", "Laundry Pool", "Z2_ALLEY"),
]

mmSceneIDToName = {
    "SCENE_20SICHITAI2": "Z2_20SICHITAI2",
    "SCENE_KAKUSIANA": "KAKUSIANA",
    "SCENE_SPOT00": "SPOT00",
    "SCENE_WITCH_SHOP": "Z2_WITCH_SHOP",
    "SCENE_LAST_BS": "Z2_LAST_BS",
    "SCENE_HAKASHITA": "Z2_HAKASHITA",
    "SCENE_AYASHIISHOP": "Z2_AYASHIISHOP",
    "SCENE_OMOYA": "Z2_OMOYA",
    "SCENE_BOWLING": "Z2_BOWLING",
    "SCENE_SONCHONOIE": "Z2_SONCHONOIE",
    "SCENE_IKANA": "Z2_IKANA",
    "SCENE_KAIZOKU": "Z2_KAIZOKU",
    "SCENE_MILK_BAR": "Z2_MILK_BAR",
    "SCENE_INISIE_N": "Z2_INISIE_N",
    "SCENE_TAKARAYA": "Z2_TAKARAYA",
    "SCENE_INISIE_R": "Z2_INISIE_R",
    "SCENE_OKUJOU": "Z2_OKUJOU",
    "SCENE_OPENINGDAN": "Z2_OPENINGDAN",
    "SCENE_MITURIN": "Z2_MITURIN",
    "SCENE_13HUBUKINOMITI": "Z2_13HUBUKINOMITI",
    "SCENE_CASTLE": "Z2_CASTLE",
    "SCENE_DEKUTES": "Z2_DEKUTES",
    "SCENE_MITURIN_BS": "Z2_MITURIN_BS",
    "SCENE_SYATEKI_MIZU": "Z2_SYATEKI_MIZU",
    "SCENE_HAKUGIN": "Z2_HAKUGIN",
    "SCENE_ROMANYMAE": "Z2_ROMANYMAE",
    "SCENE_PIRATE": "Z2_PIRATE",
    "SCENE_SYATEKI_MORI": "Z2_SYATEKI_MORI",
    "SCENE_SINKAI": "Z2_SINKAI",
    "SCENE_YOUSEI_IZUMI": "Z2_YOUSEI_IZUMI",
    "SCENE_KINSTA1": "Z2_KINSTA1",
    "SCENE_KINDAN2": "Z2_KINDAN2",
    "SCENE_TENMON_DAI": "Z2_TENMON_DAI",
    "SCENE_LAST_DEKU": "Z2_LAST_DEKU",
    "SCENE_22DEKUCITY": "Z2_22DEKUCITY",
    "SCENE_KAJIYA": "Z2_KAJIYA",
    "SCENE_00KEIKOKU": "Z2_00KEIKOKU",
    "SCENE_POSTHOUSE": "Z2_POSTHOUSE",
    "SCENE_LABO": "Z2_LABO",
    "SCENE_DANPEI2TEST": "Z2_DANPEI2TEST",
    "SCENE_16GORON_HOUSE": "Z2_16GORON_HOUSE",
    "SCENE_33ZORACITY": "Z2_33ZORACITY",
    "SCENE_8ITEMSHOP": "Z2_8ITEMSHOP",
    "SCENE_F01": "Z2_F01",
    "SCENE_INISIE_BS": "Z2_INISIE_BS",
    "SCENE_30GYOSON": "Z2_30GYOSON",
    "SCENE_31MISAKI": "Z2_31MISAKI",
    "SCENE_TAKARAKUJI": "Z2_TAKARAKUJI",
    "SCENE_TORIDE": "Z2_TORIDE",
    "SCENE_FISHERMAN": "Z2_FISHERMAN",
    "SCENE_GORONSHOP": "Z2_GORONSHOP",
    "SCENE_DEKU_KING": "Z2_DEKU_KING",
    "SCENE_LAST_GORON": "Z2_LAST_GORON",
    "SCENE_24KEMONOMITI": "Z2_24KEMONOMITI",
    "SCENE_F01_B": "Z2_F01_B",
    "SCENE_F01C": "Z2_F01C",
    "SCENE_BOTI": "Z2_BOTI",
    "SCENE_HAKUGIN_BS": "Z2_HAKUGIN_BS",
    "SCENE_20SICHITAI": "Z2_20SICHITAI",
    "SCENE_21MITURINMAE": "Z2_21MITURINMAE",
    "SCENE_LAST_ZORA": "Z2_LAST_ZORA",
    "SCENE_11GORONNOSATO2": "Z2_11GORONNOSATO2",
    "SCENE_SEA": "Z2_SEA",
    "SCENE_35TAKI": "Z2_35TAKI",
    "SCENE_REDEAD": "Z2_REDEAD",
    "SCENE_BANDROOM": "Z2_BANDROOM",
    "SCENE_11GORONNOSATO": "Z2_11GORONNOSATO",
    "SCENE_GORON_HAKA": "Z2_GORON_HAKA",
    "SCENE_SECOM": "Z2_SECOM",
    "SCENE_10YUKIYAMANOMURA": "Z2_10YUKIYAMANOMURA",
    "SCENE_TOUGITES": "Z2_TOUGITES",
    "SCENE_DANPEI": "Z2_DANPEI",
    "SCENE_IKANAMAE": "Z2_IKANAMAE",
    "SCENE_DOUJOU": "Z2_DOUJOU",
    "SCENE_MUSICHOUSE": "Z2_MUSICHOUSE",
    "SCENE_IKNINSIDE": "Z2_IKNINSIDE",
    "SCENE_MAP_SHOP": "Z2_MAP_SHOP",
    "SCENE_F40": "Z2_F40",
    "SCENE_F41": "Z2_F41",
    "SCENE_10YUKIYAMANOMURA2": "Z2_10YUKIYAMANOMURA2",
    "SCENE_14YUKIDAMANOMITI": "Z2_14YUKIDAMANOMITI",
    "SCENE_12HAKUGINMAE": "Z2_12HAKUGINMAE",
    "SCENE_17SETUGEN": "Z2_17SETUGEN",
    "SCENE_17SETUGEN2": "Z2_17SETUGEN2",
    "SCENE_SEA_BS": "Z2_SEA_BS",
    "SCENE_RANDOM": "Z2_RANDOM",
    "SCENE_YADOYA": "Z2_YADOYA",
    "SCENE_KONPEKI_ENT": "Z2_KONPEKI_ENT",
    "SCENE_INSIDETOWER": "Z2_INSIDETOWER",
    "SCENE_26SARUNOMORI": "Z2_26SARUNOMORI",
    "SCENE_LOST_WOODS": "Z2_LOST_WOODS",
    "SCENE_LAST_LINK": "Z2_LAST_LINK",
    "SCENE_SOUGEN": "Z2_SOUGEN",
    "SCENE_BOMYA": "Z2_BOMYA",
    "SCENE_KYOJINNOMA": "Z2_KYOJINNOMA",
    "SCENE_KOEPONARACE": "Z2_KOEPONARACE",
    "SCENE_GORONRACE": "Z2_GORONRACE",
    "SCENE_TOWN": "Z2_TOWN",
    "SCENE_ICHIBA": "Z2_ICHIBA",
    "SCENE_BACKTOWN": "Z2_BACKTOWN",
    "SCENE_CLOCKTOWER": "Z2_CLOCKTOWER",
    "SCENE_ALLEY": "Z2_ALLEY",
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
