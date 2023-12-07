from dataclasses import dataclass


@dataclass
class Mm_BaseElement:
    id: str
    key: str
    name: str
    index: int


@dataclass
class Mm_Data:
    """Contains data related to Mm, like actors or objects"""

    def __init__(self):
        from .mm_enum_data import Mm_EnumData
        from .mm_object_data import Mm_ObjectData
        from .mm_actor_data import Mm_ActorData

        self.enumData = Mm_EnumData()
        self.objectData = Mm_ObjectData()
        self.actorData = Mm_ActorData()
