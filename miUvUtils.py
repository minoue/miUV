from maya import cmds
from maya import OpenMaya
from maya import mel


def flipUVs(args):
    cmds.polyEditUV(scale=True, scaleU=-1, pivotU=0.5)

    
def flipUVsByLocal(*args):
    sel = cmds.ls(sl=True, fl=True, long=True)
    u = 0.0
    for i in sel:
        uv = cmds.polyEditUV(i, relative=False, q=True, uValue=True)
        u += uv[0]
    uAve = u / len(sel)
    u_tile = int(str(uAve)[0])
    flipAxis = u_tile + 0.5
    cmds.polyEditUV(relative=False, pivotU=flipAxis, scaleU=-1)    

    
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
