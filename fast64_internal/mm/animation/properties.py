from bpy.types import Object, PropertyGroup, UILayout, Context
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty, BoolProperty, StringProperty, IntProperty
from ...f3d.flipbook import mmFlipbookAnimUpdate
from ...utility import prop_split


# The update callbacks are for manually setting texture with visualize operator.
# They don't run from animation updates, see flipbookAnimHandler in flipbook.py
def mmUpdateLinkEyes(self, context: Context):
    index = self.eyes
    mmFlipbookAnimUpdate(self, context.object, "8", index)


def mmUpdateLinkMouth(self, context: Context):
    index = self.mouth
    mmFlipbookAnimUpdate(self, context.object, "9", index)


class MMAnimExportSettingsProperty(PropertyGroup):
    isCustomFilename: BoolProperty(
        name="Use Custom Filename", description="Override filename instead of basing it off of the Blender name"
    )
    filename: StringProperty(name="Filename")
    isCustom: BoolProperty(
        name="Use Custom Path", description="Determines whether or not to export to an explicitly specified folder"
    )
    customPath: StringProperty(name="Folder", subtype="FILE_PATH")
    folderName: StringProperty(name="Animation Folder", default="object_geldb")
    isLink: BoolProperty(name="Is Link", default=False)

    def draw_props(self, layout: UILayout):
        layout.label(text="Exports active animation on selected object.", icon="INFO")
        layout.prop(self, "isCustomFilename")
        if self.isCustomFilename:
            prop_split(layout, self, "filename", "Filename")
        if self.isCustom:
            prop_split(layout, self, "customPath", "Folder")
        elif not self.isLink:
            prop_split(layout, self, "folderName", "Object")
        layout.prop(self, "isLink")
        layout.prop(self, "isCustom")


class MMAnimImportSettingsProperty(PropertyGroup):
    isCustom: BoolProperty(name="Use Custom Path")
    customPath: StringProperty(name="Folder", subtype="FILE_PATH")
    folderName: StringProperty(name="Animation Folder", default="object_geldb")
    isLink: BoolProperty(name="Is Link", default=False)
    animName: StringProperty(name="Anim Name", default="gGerudoRedSpinAttackAnim")

    def draw_props(self, layout: UILayout):
        prop_split(layout, self, "animName", "Anim Header Name")
        if self.isCustom:
            prop_split(layout, self, "customPath", "File")
        elif not self.isLink:
            prop_split(layout, self, "folderName", "Object")
        layout.prop(self, "isLink")
        layout.prop(self, "isCustom")


class MMLinkTextureAnimProperty(PropertyGroup):
    eyes: IntProperty(min=0, max=15, default=0, name="Eyes", update=mmUpdateLinkEyes)
    mouth: IntProperty(min=0, max=15, default=0, name="Mouth", update=mmUpdateLinkMouth)

    def draw_props(self, layout: UILayout):
        prop_split(layout, self, "eyes", "Eyes")
        prop_split(layout, self, "mouth", "Mouth")


classes = (
    MMAnimExportSettingsProperty,
    MMAnimImportSettingsProperty,
    MMLinkTextureAnimProperty,
)


def mm_anim_props_register():
    for cls in classes:
        register_class(cls)

    Object.mmLinkTextureAnim = PointerProperty(type=MMLinkTextureAnimProperty)


def mm_anim_props_unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    del Object.mmLinkTextureAnim
