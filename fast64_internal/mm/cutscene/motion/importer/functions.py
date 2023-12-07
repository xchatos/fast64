import bpy

from .classes import MMCSMotionImport


def importCutsceneData(filePath: str, sceneData: str):
    """Initialises and imports the cutscene data from either a file or the scene data"""
    # NOTE: ``sceneData`` is the data read when importing a scene
    csMotionImport = MMCSMotionImport(filePath, sceneData)
    return csMotionImport.setCutsceneData(bpy.context.scene.mmCSNumber)
