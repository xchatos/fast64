from ....mm_collision import mmCollisionToC
from ....mm_level_classes import MMScene


# Writes the collision data for a scene
def getSceneCollision(outScene: MMScene):
    # @TODO: delete this function and rename ``mmCollisionToC`` into ``getSceneCollision``
    # when the ``mm_collision.py`` code is cleaned up
    return mmCollisionToC(outScene.collision)
