from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
    # If obj is not given and the selection is set to False, error early
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # If no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    currentTime = cmds.currentTime(query=True)
    print("set keyframe at time:%d" % currentTime)

    for attr in attrs:
        # Construct the full name of attribute with its object
        attrFull = '%s.%s' % (obj, attr)

        # Get the keyframes of the attributes of the object
        keyframes = cmds.keyframe(attrFull, query=True)

        # If there is no keyframe, then continue
        if not keyframes:
            continue

        previousKeyframes = []
        for frame in keyframes:
            if frame < currentTime:
                previousKeyframes.append(frame)

        # A simple way to do as the same as above
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
            previousKeyframe = max(previousKeyframes)
        else:
            previousKeyframe = None

        # A simple way to do as the same as above
        nextframe = min(laterKeyframes) if laterKeyframes else None

        if not previousKeyframe or not nextframe:
            continue

        previousValue = cmds.getAttr(attrFull, time=previousKeyframe)
        nextValue = cmds.getAttr(attrFull, time=nextframe)

        difference = nextValue - previousValue
        weightDifference = difference * percentage / 100.0
        currentValue = previousValue + weightDifference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)
        cmds.setAttr(attrFull, currentValue)

class TweenWindow(object):

    windowName = "TweenerWindow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)

    def close(self, *args):
        cmds.deleteUI(self.windowName)
