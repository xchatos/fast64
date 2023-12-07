from .....utility import CData, indent
from ....mm_spline import MMPath
from ....mm_level_classes import MMScene


def getPathPointData(path: MMPath, headerIndex: int, pathIndex: int):
    pathData = CData()
    pathName = f"Vec3s {path.pathName(headerIndex, pathIndex)}"

    # .h
    pathData.header = f"extern {pathName}[];\n"

    # .c
    pathData.source = (
        f"{pathName}[]"
        + " = {\n"
        + "\n".join(
            indent + "{ " + ", ".join(f"{round(curPoint):5}" for curPoint in point) + " }," for point in path.points
        )
        + "\n};\n\n"
    )

    return pathData


def getPathData(outScene: MMScene, headerIndex: int):
    pathData = CData()
    pathListData = CData()
    listName = f"Path {outScene.pathListName(headerIndex)}[{len(outScene.pathList)}]"

    # .h
    pathListData.header = f"extern {listName};\n"

    # .c
    pathListData.source = listName + " = {\n"

    # Parse in alphabetical order of names
    sortedPathList = sorted(outScene.pathList, key=lambda x: x.objName.lower())
    for i, curPath in enumerate(sortedPathList):
        pathName = curPath.pathName(headerIndex, i)
        pathListData.source += indent + "{ " + f"ARRAY_COUNTU({pathName}), {pathName}" + " },\n"
        pathData.append(getPathPointData(curPath, headerIndex, i))

    pathListData.source += "};\n\n"
    pathData.append(pathListData)

    return pathData
