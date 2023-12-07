import bpy
from bpy.utils import register_class, unregister_class

from .scene.operators import mm_scene_ops_register, mm_scene_ops_unregister
from .scene.properties import MMBootupSceneOptions, mm_scene_props_register, mm_scene_props_unregister
from .scene.panels import mm_scene_panels_register, mm_scene_panels_unregister

from .props_panel_main import mm_obj_panel_register, mm_obj_panel_unregister, mm_obj_register, mm_obj_unregister
from .skeleton.properties import MMSkeletonImportSettings, MMSkeletonExportSettings
from .mm_utility import mm_utility_register, mm_utility_unregister, setAllActorsVisibility
from .file_settings import mm_file_register, mm_file_unregister
from .collision.properties import MMCollisionExportSettings

from .room.operators import mm_room_ops_register, mm_room_ops_unregister
from .room.properties import mm_room_props_register, mm_room_props_unregister

from .actor.operators import mm_actor_ops_register, mm_actor_ops_unregister
from .actor.properties import mm_actor_props_register, mm_actor_props_unregister

from .f3d.operators import mm_f3d_ops_register, mm_f3d_ops_unregister
from .f3d.properties import MMDLExportSettings, MMDLImportSettings, mm_f3d_props_register, mm_f3d_props_unregister
from .f3d.panels import mm_f3d_panels_register, mm_f3d_panels_unregister

from .collision.operators import mm_collision_ops_register, mm_collision_ops_unregister
from .collision.properties import mm_collision_props_register, mm_collision_props_unregister
from .collision.panels import mm_collision_panels_register, mm_collision_panels_unregister

from .animation.operators import mm_anim_ops_register, mm_anim_ops_unregister
from .animation.panels import mm_anim_panels_register, mm_anim_panels_unregister
from .animation.properties import (
    MMAnimExportSettingsProperty,
    MMAnimImportSettingsProperty,
    mm_anim_props_register,
    mm_anim_props_unregister,
)

from .cutscene.operators import mm_cutscene_ops_register, mm_cutscene_ops_unregister
from .cutscene.properties import mm_cutscene_props_register, mm_cutscene_props_unregister
from .cutscene.panels import mm_cutscene_panels_register, mm_cutscene_panels_unregister
from .cutscene.preview import mm_cutscene_preview_register, mm_cutscene_preview_unregister

from .cutscene.motion.operators import mm_csMotion_ops_register, mm_csMotion_ops_unregister
from .cutscene.motion.properties import mm_csMotion_props_register, mm_csMotion_props_unregister
from .cutscene.motion.panels import mm_csMotion_panels_register, mm_csMotion_panels_unregister
from .cutscene.motion.preview import mm_csMotion_preview_register, mm_csMotion_preview_unregister

from .skeleton.operators import mm_skeleton_ops_register, mm_skeleton_ops_unregister
from .skeleton.properties import mm_skeleton_props_register, mm_skeleton_props_unregister
from .skeleton.panels import mm_skeleton_panels_register, mm_skeleton_panels_unregister

from .spline.properties import mm_spline_props_register, mm_spline_props_unregister
from .spline.panels import mm_spline_panels_register, mm_spline_panels_unregister

from .tools import (
    mm_operator_panel_register,
    mm_operator_panel_unregister,
    mm_operator_register,
    mm_operator_unregister,
)


class MM_Properties(bpy.types.PropertyGroup):
    """Global MM Scene Properties found under scene.fast64.mm"""

    version: bpy.props.IntProperty(name="MM_Properties Version", default=0)
    hackerFeaturesEnabled: bpy.props.BoolProperty(name="Enable HackerMM Features")
    headerTabAffectsVisibility: bpy.props.BoolProperty(
        default=False, name="Header Sets Actor Visibility", update=setAllActorsVisibility
    )
    bootupSceneOptions: bpy.props.PointerProperty(type=MMBootupSceneOptions)
    DLExportSettings: bpy.props.PointerProperty(type=MMDLExportSettings)
    DLImportSettings: bpy.props.PointerProperty(type=MMDLImportSettings)
    skeletonExportSettings: bpy.props.PointerProperty(type=MMSkeletonExportSettings)
    skeletonImportSettings: bpy.props.PointerProperty(type=MMSkeletonImportSettings)
    animExportSettings: bpy.props.PointerProperty(type=MMAnimExportSettingsProperty)
    animImportSettings: bpy.props.PointerProperty(type=MMAnimImportSettingsProperty)
    collisionExportSettings: bpy.props.PointerProperty(type=MMCollisionExportSettings)


mm_classes = (MM_Properties,)


def mm_panel_register():
    mm_operator_panel_register()
    mm_f3d_panels_register()
    mm_collision_panels_register()
    mm_obj_panel_register()
    mm_scene_panels_register()
    mm_spline_panels_register()
    mm_anim_panels_register()
    mm_skeleton_panels_register()
    mm_cutscene_panels_register()


def mm_panel_unregister():
    mm_operator_panel_unregister()
    mm_collision_panels_unregister()
    mm_obj_panel_unregister()
    mm_scene_panels_unregister()
    mm_spline_panels_unregister()
    mm_f3d_panels_unregister()
    mm_anim_panels_unregister()
    mm_skeleton_panels_unregister()
    #mm_cutscene_panels_unregister()


def mm_register(registerPanels):
    mm_operator_register()
    mm_utility_register()
    mm_collision_ops_register()  # register first, so panel goes above mat panel
    mm_collision_props_register()
    mm_cutscene_props_register()
    mm_scene_ops_register()
    mm_scene_props_register()
    mm_room_ops_register()
    mm_room_props_register()
    mm_actor_ops_register()
    mm_actor_props_register()
    mm_obj_register()
    mm_spline_props_register()
    mm_f3d_props_register()
    mm_anim_ops_register()
    mm_skeleton_ops_register()
    mm_skeleton_props_register()
    mm_cutscene_ops_register()
    mm_f3d_ops_register()
    mm_file_register()
    mm_anim_props_register()

    mm_csMotion_ops_register()
    mm_csMotion_props_register()
    mm_csMotion_panels_register()
    mm_csMotion_preview_register()
    mm_cutscene_preview_register()

    for cls in mm_classes:
        register_class(cls)

    if registerPanels:
        mm_panel_register()


def mm_unregister(unregisterPanels):
    for cls in reversed(mm_classes):
        unregister_class(cls)

    mm_operator_unregister()
    mm_utility_unregister()
    mm_collision_ops_unregister()  # register first, so panel goes above mat panel
    mm_collision_props_unregister()
    mm_obj_unregister()
    mm_cutscene_props_unregister()
    mm_scene_ops_unregister()
    mm_scene_props_unregister()
    mm_room_ops_unregister()
    mm_room_props_unregister()
    mm_actor_ops_unregister()
    mm_actor_props_unregister()
    mm_spline_props_unregister()
    mm_f3d_props_unregister()
    mm_anim_ops_unregister()
    mm_skeleton_ops_unregister()
    mm_skeleton_props_unregister()
    mm_cutscene_ops_unregister()
    mm_f3d_ops_unregister()
    mm_file_unregister()
    mm_anim_props_unregister()

    mm_cutscene_preview_unregister()
    mm_csMotion_preview_unregister()
    mm_csMotion_panels_unregister()
    #mm_csMotion_props_unregister()
    #mm_csMotion_ops_unregister()

    if unregisterPanels:
        mm_panel_unregister()
