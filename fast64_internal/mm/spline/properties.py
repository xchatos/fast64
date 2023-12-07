from bpy.types import PropertyGroup, Object, UILayout
from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty
from bpy.utils import register_class, unregister_class
from ...utility import prop_split
from ..mm_utility import drawEnumWithCustom
from ..mm_collision_classes import mmEnumCameraCrawlspaceSType
from ..actor.properties import MMActorHeaderProperty
from ..scene.properties import MMAlternateSceneHeaderProperty


mmSplineEnum = [("Path", "Path", "Path"), ("Crawlspace", "Crawlspace", "Crawlspace")]


class MMSplineProperty(PropertyGroup):
    splineType: EnumProperty(items=mmSplineEnum, default="Path")
    index: IntProperty(min=0)  # only used for crawlspace, not path
    headerSettings: PointerProperty(type=MMActorHeaderProperty)
    camSType: EnumProperty(items=mmEnumCameraCrawlspaceSType, default="CAM_SET_CRAWLSPACE")
    camSTypeCustom: StringProperty(default="CAM_SET_CRAWLSPACE")

    def draw_props(self, layout: UILayout, altSceneProp: MMAlternateSceneHeaderProperty, objName: str):
        prop_split(layout, self, "splineType", "Type")
        if self.splineType == "Path":
            headerProp: MMActorHeaderProperty = self.headerSettings
            headerProp.draw_props(layout, "Curve", altSceneProp, objName)
        elif self.splineType == "Crawlspace":
            layout.label(text="This counts as a camera for index purposes.", icon="INFO")
            prop_split(layout, self, "index", "Index")
            drawEnumWithCustom(layout, self, "camSType", "Camera S Type", "")


mm_spline_classes = (MMSplineProperty,)


def mm_spline_props_register():
    for cls in mm_spline_classes:
        register_class(cls)

    Object.mmSplineProperty = PointerProperty(type=MMSplineProperty)


def mm_spline_props_unregister():
    for cls in reversed(mm_spline_classes):
        unregister_class(cls)

    del Object.mmSplineProperty
