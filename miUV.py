from functools import partial
import maya.cmds as cmds
import maya.mel as mel
import commands
reload(commands)
import os


class MiUV(object):
    def __init__(self):
        self.windowName = "CustomUvEditor"

        if cmds.window(self.windowName, q=True, exists=True) is True:
            cmds.deleteUI(self.windowName)
        else:
            pass

        self.currentDir = os.path.dirname(__file__)
        self.iconDir = os.path.join(self.currentDir, "icons")
        self.homeDir = os.path.expanduser("~")
        self.uvTexturePath = os.path.normpath(os.path.join(
            self.currentDir, "images/uvTexture.jpg"))
        print self.uvTexturePath

    def createUI(self):
        myWindow = cmds.window(
            self.windowName,
            h=800,
            w=1000,
            menuBar=True,
            s=True)

        mainLayout = cmds.formLayout(numberOfDivisions=100)

        selectionLayout = cmds.columnLayout(adj=True, h=45)
        cmds.text(label="Selection Constraint")
        self.selectionModeRadioButton = cmds.radioButtonGrp(
            labelArray4=['None', 'Shell', 'Border', 'Internal'],
            numberOfRadioButtons=4,
            select=1,
            cw4=[100, 100, 100, 100],
            on1=partial(self.changeSelectionConstraint, 1),
            on2=partial(self.changeSelectionConstraint, 2),
            on3=partial(self.changeSelectionConstraint, 3),
            on4=partial(self.changeSelectionConstraint, 4))
        cmds.setParent('..')  # selectionLayout

        shaderLayout = cmds.formLayout()
        uvRepeatSlider = cmds.attrFieldSliderGrp(
            label="Repeat",
            min=0.0,
            max=20.0,
            parent=shaderLayout)
        if cmds.objExists("uvShaderPlace2dTexture"):
            cmds.attrFieldSliderGrp(
                uvRepeatSlider,
                edit=True,
                at='uvShaderPlace2dTexture.repeatU')
        else:
            pass
        uvShaderButton = cmds.button(
            label="Create UV shader",
            command=partial(
                commands.createUVshader,
                self.uvTexturePath,
                uvRepeatSlider))
        uvShaderAssignButton = cmds.button(
            label="Assgin UV shader",
            command=partial(
                commands.assignUVshader))
        cmds.setParent('..')

        cmds.formLayout(
            shaderLayout,
            edit=True,
            attachForm=[
                (uvShaderButton, 'top', 2),
                (uvShaderButton, 'left', 2),
                (uvShaderAssignButton, 'top', 2),
                (uvRepeatSlider, 'bottom', 2),
                (uvRepeatSlider, 'left', 2),
                (uvRepeatSlider, 'right', 2)
            ],
            attachControl=[(uvShaderAssignButton, 'left', 2, uvShaderButton)])

        #### LEFT LAYOUT ####
        leftLayout = cmds.columnLayout(adj=True, w=120)
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(40, 40))
        cmds.iconTextButton(
            image="%s/upLeft.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u -1 -v 1;')")
        cmds.iconTextButton(
            image="%s/up.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u 0 -v 1;')")
        cmds.iconTextButton(
            image="%s/upRight.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u 1 -v 1;')")
        cmds.iconTextButton(
            image="%s/left.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u -1 -v 0;')")
        cmds.iconTextButton()
        cmds.iconTextButton(
            image="%s/right.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u 1 -v 0;')")
        cmds.iconTextButton(
            image="%s/bottomLeft.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u -1 -v -1;')")
        cmds.iconTextButton(
            image="%s/bottom.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u 0 -v -1;')")
        cmds.iconTextButton(
            image="%s/bottomRight.png" % self.iconDir,
            commandRepeatable=True,
            command="mel.eval('polyEditUV -u 1 -v -1;')")
        cmds.setParent('..')  # gridLayout
        cmds.button(
            label="BonusTool AutoUnwrap",
            command="mel.eval('bonusToolsMenu;bt_autoUnwrapUVTool;')",
            enable=False)
        cmds.button(
            label="UV Centric",
            command="cmds.UVCentricUVLinkingEditor()")
        cmds.button(label="Zebruv Tool", enable=False)
        cmds.button(label="UV Set Editor", command="cmds.UVSetEditor()")
        cmds.separator(h=20)
        cmds.text(label="Transfer UVs")
        uvSpaceTransferRadioButton = cmds.radioButtonGrp(
            labelArray2=["World", "Comp"],
            numberOfRadioButtons=2,
            select=2,
            cw2=[60, 60])
        cmds.button(
            label="TRANSFER UVs",
            command=partial(
                self.radioButtonCommand,
                uvSpaceTransferRadioButton,
                commands.transferUVs))
        cmds.text(label="*Select source mesh \nfirst, then targets")
        cmds.separator(h=20)
        cmds.text(label="Symmetrize UVs")
        uvSymRadioButton = cmds.radioButtonGrp(
            labelArray3=["X", "Y", "Z"],
            numberOfRadioButtons=3,
            select=1,
            cw3=[40, 40, 40])
        cmds.text(label="*Select target \nvertices")
        cmds.button(
            label="MIRROR UVs",
            command=partial(
                self.radioButtonCommand,
                uvSymRadioButton,
                commands.mirroringUVs))
        cmds.separator(h=20)
        cmds.button(
            label="Fix UV radio",
            command=partial(commands.fixUVscale))
        cmds.button(
            label="Copy UVs to map1",
            command=partial(commands.copyUVsToMap1))
        cmds.button(
            label="Flip UVs by world",
            command=partial(commands.flipUVsByWorld))
        cmds.button(
            label="Delete History",
            command="cmds.DeleteHistory()")
        cmds.separator(h=20)
        cmds.text(label="Repeat UVs")
        self.uMax = cmds.textField(h=25, text="type number of U here")
        cmds.button(
            label="UV horizontal repeat",
            enable=True,
            command=self.repeatUVs)
        cmds.separator(h=20)
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(40, 40))
        cmds.iconTextButton(
            image="polyPlanProj.png",
            imageOverlayLabel="___X",
            olc=[1, 1, 0],
            command="cmds.polyPlanarProjection(md='x', ibd=True, kir=True)",
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyPlanProj.png",
            imageOverlayLabel="___Y",
            olc=[1, 1, 0],
            command="cmds.polyPlanarProjection(md='y', ibd=True, kir=True)",
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyPlanProj.png",
            imageOverlayLabel="___Z",
            olc=[1, 1, 0],
            command="cmds.polyPlanarProjection(md='z', ibd=True, kir=True)",
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyCylProj.png",
            imageOverlayLabel="___X",
            olc=[1, 1, 0],
            command=(
                "cmds.polyProjection(ch=1, kir=True, "
                "type='cylindrical', ibd=True, sf=True, rx=90)"),
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyCylProj.png",
            imageOverlayLabel="___Y",
            olc=[1, 1, 0],
            command=(
                "cmds.polyProjection(ch=1, kir=True, "
                "type='cylindrical', ibd=True, sf=True, ry=90)"),
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyCylProj.png",
            imageOverlayLabel="___Z",
            olc=[1, 1, 0],
            command=(
                "cmds.polyProjection(ch=1, kir=True, "
                "type='cylindrical', ibd=True, sf=True, rz=90)"),
            commandRepeatable=True)
        cmds.iconTextButton(
            image="polyAutoProj.png",
            imageOverlayLabel="Auto",
            olc=[1, 1, 0],
            commandRepeatable=True,
            command="mel.eval('performPolyAutoProj 0;')")
        cmds.iconTextButton(
            image="polyAutoProj.png",
            imageOverlayLabel="Cam",
            olc=[1, 1, 0],
            commandRepeatable=True,
            command="cmds.polyProjection(type='planar', md='p')")
        cmds.setParent('..')  # gridLayout
        cmds.setParent('..')  # leftLayout

        ##### BOTTOM LAYOUT #####
        bottomLayout = cmds.rowColumnLayout(
            numberOfColumns=6,
            h=45,
            columnWidth=[
                (1, 500),
                (2, 40),
                (3, 60),
                (4, 60),
                (5, 60),
                (6, 60)])
        cmds.text(label="QuickSnapShot", align="left")
        cmds.text(label="Browes", align="left")
        cmds.text(label="Size", align="left")
        cmds.text(label="Tile Num", align="left")
        cmds.text(label="format", align="left")
        cmds.text(label="")
        self.uvImagePath = cmds.textField(h=2)
        initialPath = os.path.join(self.homeDir, "testImage.tif")
        cmds.textField(self.uvImagePath, edit=True, text=initialPath)
        cmds.symbolButton(
            w=25,
            h=25,
            image="menuIconFile.png",
            command=self.browseDirectoryPath)
        self.uvImageResolution = cmds.optionMenuGrp(enable=True)
        cmds.menuItem(label="8k")
        cmds.menuItem(label="4k")
        cmds.menuItem(label="2k")
        cmds.menuItem(label="1k")
        cmds.menuItem(label="512")
        self.uvImageTileNumber = cmds.optionMenuGrp(h=25, enable=True)
        for i in range(100):
            tileNumber = "1" + str(i + 1).zfill(3)
            cmds.menuItem(label=tileNumber)
        self.uvImageFormat = cmds.optionMenuGrp(enable=True)
        cmds.menuItem(label="tif")
        cmds.menuItem(label="jpg")
        cmds.menuItem(label="iff")
        cmds.menuItem(label="sgi")
        cmds.menuItem(label="pic")
        cmds.menuItem(label="als")
        cmds.menuItem(label="gif")
        cmds.menuItem(label="rla")
        cmds.button(
            label="Export",
            h=30,
            command=self.takeUvSnapshot)
        cmds.setParent('..')

        ##### TEXTURE WINDOW LAYOUT #####
        textureLayout = cmds.paneLayout(configuration='single')
        pane = cmds.paneLayout(configuration="vertical2")
        cmds.paneLayout(pane, e=True, paneSize=(1, 0, 0))
        cmds.modelPanel(cam="perspShape", tearOff=False)
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')  # mainLayout

        ### UNPARENT CURRENT UV TEXTURE EDITOR AND RE-PARENT TO MY EIDTOR ###
        texturePanel = cmds.getPanel(scriptType='polyTexturePlacementPanel')[0]
        cmds.scriptedPanel(texturePanel, edit=True, unParent=True)
        mel.eval("fillEmptyPanes;")
        cmds.scriptedPanel(texturePanel, edit=True, parent=pane)

        #FORM LAYOUT
        cmds.formLayout(
            mainLayout,
            e=True,
            attachForm=[
                (selectionLayout, 'top', 2),
                (shaderLayout, 'top', 2),
                (shaderLayout, 'right', 2),
                (shaderLayout, 'right', 2),
                (leftLayout, 'left', 2),
                (leftLayout, 'top', 2),
                (leftLayout, 'bottom', 2),
                (textureLayout, 'left', 2),
                (textureLayout, 'top', 2),
                (textureLayout, 'right', 2),
                (textureLayout, 'bottom', 2),
                (bottomLayout, 'bottom', 2),
                (bottomLayout, 'left', 2)],
            attachControl=[
                (selectionLayout, 'left', 2, leftLayout),
                (leftLayout, 'bottom', 2, bottomLayout),
                (shaderLayout, 'left', 2, selectionLayout),
                (textureLayout, 'top', 2, selectionLayout),
                (textureLayout, 'bottom', 2, bottomLayout),
                (textureLayout, 'left', 2, leftLayout)])

        # SHOW WINDOW
        cmds.showWindow(myWindow)

    def radioButtonCommand(self, radioButton, function, *args):
        value = cmds.radioButtonGrp(
            radioButton,
            q=True,
            select=True)
        function(value)

    def repeatUVs(self, *args):
        value = cmds.textField(self.uMax, q=True, text=True)
        commands.uvHorizontalRepeat(value)

    def selectUVshellBorder(self):
        mode = cmds.radioButtonGrp(
            self.selectionModeRadioButton,
            q=True,
            select=True)
        try:
            sel = cmds.ls(sl=True, fl=True)[0]
            nodeType = cmds.nodeType(sel)
            if nodeType == "mesh":
                if mode == 3:
                    cmds.SelectUVBorder()
                elif mode == 4:
                    cmds.SelectUVShell()
                    shellUVs = cmds.ls(sl=True, fl=True)
                    cmds.SelectUVBorder()
                    border = cmds.ls(sl=True, fl=True)
                    cmds.select(border, toggle=True)
                    internalUVs = list(set(shellUVs) - set(border))
                    cmds.select(internalUVs, r=True)
        except:
            pass

    def changeSelectionConstraint(self, *args):
        mode = cmds.radioButtonGrp(
            self.selectionModeRadioButton,
            q=True,
            select=True)
        if mode == 1:
            cmds.polySelectConstraint(disable=True)
        elif mode == 2:
            cmds.polySelectConstraint(disable=True)
            cmds.polySelectConstraint(shell=True)
        elif mode == 3:
            cmds.polySelectConstraint(disable=True)
        elif mode == 4:
            cmds.polySelectConstraint(disable=True)

    def takeUvSnapshot(self, *args):
        fileName = cmds.textField(self.uvImagePath, q=True, text=True)
        resolution = cmds.optionMenuGrp(
            self.uvImageResolution,
            q=True,
            value=True)
        imageFormat = cmds.optionMenuGrp(
            self.uvImageFormat,
            q=True, value=True)
        tileNumber = cmds.optionMenuGrp(
            self.uvImageTileNumber,
            q=True,
            value=True)
        if (tileNumber[3] == "0" or tileNumber[3] == 0):
            uMin = 9.0
            vMin = float(int(tileNumber[2]) - 1)
        else:
            uMin = float(int(tileNumber[3]) - 1)
            vMin = float(tileNumber[2])
        uMax = float(uMin + 1.0)
        vMax = float(vMin + 1.0)

        if resolution == "8k":
            xRes = 8192
            yRes = 8192
        elif resolution == "4k":
            xRes = 4096
            yRes = 4096
        elif resolution == "2k":
            xRes = 2048
            yRes = 2048
        elif resolution == "1k":
            xRes = 1024
            yRes = 1024
        elif resolution == "512":
            xRes = 512
            yRes = 512

        cmds.uvSnapshot(name=fileName,
                        aa=True,
                        fileFormat=imageFormat,
                        xResolution=xRes,
                        yResolution=yRes,
                        overwrite=True,
                        redColor=255,
                        greenColor=255,
                        blueColor=255,
                        uMax=uMax,
                        uMin=uMin,
                        vMax=vMax,
                        vMin=vMin)

    def browseDirectoryPath(self, *args):
        basicFilter = "*All(*.*);;tif(*.tif);;jpg(*.jpg);;exr(*.exr);;tx(*.tx)"
        self.returnPath = cmds.fileDialog2(
            fileFilter=basicFilter,
            ds=2,
            startingDirectory=self.homeDir)[0]
        cmds.textField(self.uvImagePath, e=True, text=self.returnPath)


def main():
    uvwin = MiUV()
    uvwin.createUI()
    cmds.scriptJob(
        event=["SelectionChanged", uvwin.selectUVshellBorder],
        parent=uvwin.windowName)

if __name__ == '__main__':
    main()
