import maya.cmds as cmds
import maya.mel as mel


def transferUVs(space, *args):
    if space == 2:
        value = 4
    elif space == 1:
        value = 0
    # space: 0=world, 1=model, 3=UV, 4=component
    # uvset: 0=No uvSet, 1=Single uvSet, 2=all uvSet
    sel = cmds.ls(sl=True)
    source = sel[0]
    target = sel[1:]
    for s in target:
        cmds.transferAttributes(
            source,
            s,
            transferUVs=1,
            sampleSpace=value)


def mirroringUVs(mirroringSpace, *args):
    print mirroringSpace
    if mirroringSpace == 1:
        xValue = -1.0
        yValue = 1.0
        zValue = 1.0
    elif mirroringSpace == 2:
        xValue = 1.0
        yValue = -1.0
        zValue = 1.0
    elif mirroringSpace == 3:
        xValue = 1.0
        yValue = 1.0
        zValue = -1.0
    cmds.transferAttributes(
        transferPositions=0,
        transferNormals=0,
        transferUVs=1,  # single uvset
        transferColors=0,
        sampleSpace=0,  # world space
        searchMethod=3,
        searchScaleX=xValue,
        searchScaleY=yValue,
        searchScaleZ=zValue,
        flipUVs=1)


def fixUVscale(*args):
    try:
        if not cmds.pluginInfo("rainUVPrescale", q=True, l=True):
            cmds.loadPlugin('rainUVPrescale.py')
    except:
        pass
    mel.eval('rainUVPrescale;')
    cmds.polyMultiLayoutUV(
        lm=1,
        sc=1,
        rbf=1,
        fr=0,
        ps=0.1,
        l=2)


def uvHorizontalRepeat(num, *args):
    uMax = float(num)
    vNum = 0.0
    uMaxCounter = 0.0
    sel = cmds.ls(sl=True, fl=True)
    for count, i in enumerate(sel):
        if count < uMax:
            cmds.select(i, r=True)
            mel.eval("PolySelectConvert 4")
            cmds.polyEditUV(u=count - uMaxCounter, v=vNum)
            if count / uMax - 1.0 == 1.0 + vNum:
                vNum += 1
                uMaxCounter += uMax + 1
        elif count >= uMax:
            cmds.select(i, r=True)
            mel.eval("PolySelectConvert 4")
            cmds.polyEditUV(u=count - uMax - uMaxCounter, v=vNum + 1)
            if (count + 1) / uMax == 2.0 + vNum:
                vNum += 1
                uMaxCounter += uMax


def copyUVsToMap1(*args):
    sel = cmds.ls(sl=True, fl=True)
    for obj in sel:
        cmds.polyCopyUV(obj, uvSetNameInput="", uvSetName="map1", ch=1)


def flipUVsByWorld(*args):
    sel = cmds.ls(sl=True, fl=True)
    for obj in sel:
        cmds.polyFlipUV(obj, local=False)


def createUVshader(texturePath, slider, *args):
    print slider
    uvShader = cmds.shadingNode(
        'blinn',
        asShader=True,
        name="uvTextureShader")
    uvShaderSG = cmds.sets(
        renderable=True,
        noSurfaceShader=True,
        empty=True,
        name="uvTextureShaderSG")
    cmds.connectAttr(uvShader + ".outColor", uvShaderSG + ".surfaceShader")

    uvTextureFile = cmds.shadingNode(
        "file",
        asTexture=True,
        name="uvTextureImage")
    uvPlace2DTexture = cmds.shadingNode(
        'place2dTexture',
        asUtility=True,
        name="uvShaderPlace2dTexture")
    cmds.connectAttr(
        uvPlace2DTexture + ".outUV", uvTextureFile + ".uv")
    cmds.connectAttr(
        uvPlace2DTexture + ".outUvFilterSize", uvTextureFile + ".uvFilterSize")
    cmds.setAttr(
        uvTextureFile + ".fileTextureName", texturePath, type="string")
    cmds.connectAttr(uvTextureFile + ".outColor", uvShader + ".color")
    cmds.connectAttr(uvPlace2DTexture + ".repeatU", uvPlace2DTexture + ".repeatV")
    cmds.setAttr(uvPlace2DTexture + ".repeatU", 4)
    cmds.setAttr(uvShader + ".specularColor", 0.1, 0.1, 0.1, type="double3")

    # Connect UV repeats to the slider
    cmds.attrFieldSliderGrp(slider, edit=True, at='uvShaderPlace2dTexture.repeatU')


def assignUVshader(*args):
    sel = cmds.ls(sl=True, fl=True)
    if not sel == []:
        cmds.select(sel, r=True)
        cmds.sets(e=True, forceElement="uvTextureShaderSG")
