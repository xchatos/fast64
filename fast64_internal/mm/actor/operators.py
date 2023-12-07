import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class
from ...utility import PluginError
from ..mm_constants import mmData


class MM_SearchActorIDEnumOperator(Operator):
    bl_idname = "object.mm_search_actor_id_enum_operator"
    bl_label = "Select Actor ID"
    bl_property = "actorID"
    bl_options = {"REGISTER", "UNDO"}

    actorID: EnumProperty(items=mmData.actorData.mmEnumActorID, default="ACTOR_PLAYER")
    actorUser: StringProperty(default="Actor")
    objName: StringProperty()

    def execute(self, context):
        obj = bpy.data.objects[self.objName]
        if self.actorUser == "Transition Actor":
            obj.mmTransitionActorProperty.actor.actorID = self.actorID
        elif self.actorUser == "Actor":
            obj.mmActorProperty.actorID = self.actorID
        elif self.actorUser == "Entrance":
            obj.mmEntranceProperty.actor.actorID = self.actorID
        else:
            raise PluginError("Invalid actor user for search: " + str(self.actorUser))

        context.region.tag_redraw()
        self.report({"INFO"}, "Selected: " + self.actorID)
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}


classes = (MM_SearchActorIDEnumOperator,)


def mm_actor_ops_register():
    for cls in classes:
        register_class(cls)


def mm_actor_ops_unregister():
    for cls in reversed(classes):
        unregister_class(cls)
