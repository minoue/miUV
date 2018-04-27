from maya import cmds
from maya import OpenMaya
from maya import mel


def flipUVs(args):
    cmds.polyEditUV(scale=True, scaleU=-1, pivotU=0.5)


def scaleUVs():
    pass


def gridUVs():
    sel = OpenMaya.MSelectionList()
    dagPath = OpenMaya.MDagPath()
    components = OpenMaya.MObject()
    OpenMaya.MGlobal.getActiveSelectionList(sel)
    sel.getDagPath(0, dagPath, components)

    connVerts = OpenMaya.MIntArray()
    connEdges = OpenMaya.MIntArray()

    itVerts = OpenMaya.MItMeshVertex(dagPath, components)
    while not itVerts.isDone():
        itVerts.getConnectedVertices(connVerts)
        itVerts.getConnectedEdges(connEdges)
        print connVerts, connEdges
        itVerts.next()


def transferAttributesOptions(*args):
    mel.eval("performTransferAttributes 1")


if __name__ == "__main__":
    gridUVs()
