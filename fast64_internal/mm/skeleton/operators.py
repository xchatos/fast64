from bpy.types import Armature, Operator, Mesh
from bpy.ops import object
from bpy.utils import register_class, unregister_class
from bpy.path import abspath
from mathutils import Matrix
from ...f3d.f3d_gbi import DLFormat
from ...utility import PluginError, raisePluginError
from ..mm_utility import getStartBone, getNextBone, getMMScale
from .exporter import mmConvertArmatureToC
from .importer import mmImportSkeletonC
from .properties import MMSkeletonImportSettings, MMSkeletonExportSettings


# Copy data from console into python file
class MM_SaveRestPose(Operator):
    # set bl_ properties
    bl_idname = "object.mm_save_rest_pose"
    bl_label = "Save Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # path: StringProperty(name="Path", subtype="FILE_PATH")
    def execute(self, context):
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")

        if len(context.selected_objects) == 0:
            raise PluginError("Armature not selected.")
        armatureObj = context.active_object
        if type(armatureObj.data) is not Armature:
            raise PluginError("Armature not selected.")

        try:
            data = "restPoseData = [\n"
            startBoneName = getStartBone(armatureObj)
            boneStack = [startBoneName]

            firstBone = True
            while len(boneStack) > 0:
                bone, boneStack = getNextBone(boneStack, armatureObj)
                poseBone = armatureObj.pose.bones[bone.name]
                if firstBone:
                    data += str(poseBone.matrix_basis.decompose()[0][:]) + ", "
                    firstBone = False
                data += str((poseBone.matrix_basis.decompose()[1]).to_euler()[:]) + ", "

            data += "\n]"

            print(data)

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


class MM_ImportSkeleton(Operator):
    # set bl_ properties
    bl_idname = "object.mm_import_skeleton"
    bl_label = "Import Skeleton"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")

        try:
            importSettings: MMSkeletonImportSettings = context.scene.fast64.mm.skeletonImportSettings
            decompPath = abspath(context.scene.mmDecompPath)

            mmImportSkeletonC(decompPath, importSettings)

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


class MM_ExportSkeleton(Operator):
    # set bl_ properties
    bl_idname = "object.mm_export_skeleton"
    bl_label = "Export Skeleton"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    # Called on demand (i.e. button press, menu item)
    # Can also be called from operator search menu (Spacebar)
    def execute(self, context):
        armatureObj = None
        if context.mode != "OBJECT":
            object.mode_set(mode="OBJECT")
        if len(context.selected_objects) == 0:
            raise PluginError("Armature not selected.")
        armatureObj = context.active_object
        if type(armatureObj.data) is not Armature:
            raise PluginError("Armature not selected.")

        if len(armatureObj.children) == 0 or not isinstance(armatureObj.children[0].data, Mesh):
            raise PluginError("Armature does not have any mesh children, or " + "has a non-mesh child.")

        obj = armatureObj.children[0]
        finalTransform = Matrix.Scale(getMMScale(armatureObj.mmActorScale), 4)

        # Rotation must be applied before exporting skeleton.
        # For some reason this does not work if done on the duplicate generated later, so we have to do it before then.
        object.select_all(action="DESELECT")
        armatureObj.select_set(True)
        object.transform_apply(location=False, rotation=True, scale=True, properties=False)
        object.select_all(action="DESELECT")

        try:
            exportSettings: MMSkeletonExportSettings = context.scene.fast64.mm.skeletonExportSettings

            saveTextures = context.scene.saveTextures
            drawLayer = armatureObj.mmDrawLayer

            mmConvertArmatureToC(armatureObj, finalTransform, DLFormat.Static, saveTextures, drawLayer, exportSettings)

            self.report({"INFO"}, "Success!")
            return {"FINISHED"}

        except Exception as e:
            if context.mode != "OBJECT":
                object.mode_set(mode="OBJECT")
            raisePluginError(self, e)
            return {"CANCELLED"}  # must return a set


mm_skeleton_classes = (
    MM_SaveRestPose,
    MM_ImportSkeleton,
    MM_ExportSkeleton,
)


def mm_skeleton_ops_register():
    for cls in mm_skeleton_classes:
        register_class(cls)


def mm_skeleton_ops_unregister():
    for cls in reversed(mm_skeleton_classes):
        unregister_class(cls)
